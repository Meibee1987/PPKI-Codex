import json
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from docx import Document
from docx.shared import Pt
from streamlit.testing.v1 import AppTest

from core.ai_planner import AnalysisError, prepare_analysis, request_analysis, validate_plan
from core.rules import load_rules

ROOT = Path(__file__).resolve().parent.parent


def document():
    doc = Document()
    doc.add_heading("BAB I PENDAHULUAN", 1)
    p = doc.add_paragraph("Paragraf sintetis untuk menguji rencana format secara terbatas.", style="Body Text")
    p.runs[0].font.name = "Arial"
    p.runs[0].font.size = Pt(11)
    p.paragraph_format.line_spacing = 2
    stream = BytesIO()
    doc.save(stream)
    return stream.getvalue()


def proposal(prepared):
    rule = prepared["rules"]["PPKI-LAY-017"]
    return {"paragraph_id": "paragraf:2", "element_type": "body", "rule_code": rule["rule_code"],
            "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "body_context"}


def client_response(payload, status="completed"):
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(status=status, output_text=json.dumps(payload))
    return client


def test_valid_response_is_only_preview_and_request_is_bounded():
    data = document()
    before = bytes(data)
    prepared = prepare_analysis(data, load_rules(), "S1")
    client = client_response({"proposals": [proposal(prepared)]})
    client.responses.create.return_value.usage = SimpleNamespace(input_tokens=500, output_tokens=200, total_tokens=700)
    result = request_analysis(prepared, "model-test", 1024, client)
    plan = result["plan"]
    assert plan[0]["status"] == "kandidat_pratinjau"
    assert result["usage"] == {"input_tokens": 500, "output_tokens": 200, "total_tokens": 700}
    assert data == before
    args = client.responses.create.call_args.kwargs
    assert args["store"] is False and args["max_output_tokens"] == 1024
    assert args["text"]["format"]["strict"] is True
    assert len(prepared["request"]["paragraphs"]) <= 30


@pytest.mark.parametrize("field,value", [("paragraph_id", "paragraf:999"), ("rule_code", "PPKI-LAY-999"),
                                         ("target", "injected"), ("action", "font"),
                                         ("element_type", "uncertain"), ("reason", "ambiguous")])
def test_invalid_or_ambiguous_actions_are_review(field, value):
    prepared = prepare_analysis(document(), load_rules(), "S1")
    item = proposal(prepared)
    item[field] = value
    assert validate_plan({"proposals": [item]}, prepared)[0]["status"] == "needs_review"


@pytest.mark.parametrize("mode", ["Manual", "Confirm"])
def test_non_auto_rules_cannot_be_authorized(mode):
    rules = load_rules()
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-017")["fix_mode"] = mode
    prepared = prepare_analysis(document(), rules, "S1")
    assert validate_plan({"proposals": [proposal(prepared)]}, prepared)[0]["status"] == "needs_review"


def test_unconfirmed_scope_cannot_be_authorized():
    prepared = prepare_analysis(document(), load_rules(), "S1")
    next(c for c in prepared["local"]["paragraf:2"]["rule_decisions"] if c["rule_code"] == "PPKI-LAY-017")["safe_to_apply"] = False
    assert validate_plan({"proposals": [proposal(prepared)]}, prepared)[0]["status"] == "needs_review"


def test_duplicate_and_missing_proposals_require_review():
    prepared = prepare_analysis(document(), load_rules(), "S1")
    item = proposal(prepared)
    assert all(p["status"] == "needs_review" for p in validate_plan({"proposals": [item, item]}, prepared))
    assert validate_plan({"proposals": []}, prepared)[0]["status"] == "needs_review"


def test_sixty_review_decisions_have_specific_local_causes():
    doc = Document()
    doc.add_heading("BAB I PENDAHULUAN", 1)
    for _ in range(30):
        doc.add_paragraph("Paragraf sintetis untuk pengujian konteks yang belum pasti.", style="Normal")
    stream = BytesIO()
    doc.save(stream)
    data = stream.getvalue()
    prepared = prepare_analysis(data, load_rules(), "S2")
    proposals = []
    for location in prepared["local"]:
        for code, action in (("PPKI-LAY-005", "font"), ("PPKI-LAY-017", "line_spacing")):
            proposals.append({"paragraph_id": location, "element_type": "body", "rule_code": code,
                              "action": action, "target": prepared["rules"][code]["expected_value_pattern"], "reason": "body_context"})
    client = client_response({"proposals": proposals})
    client.responses.create.return_value.usage = SimpleNamespace(input_tokens=3000, output_tokens=3900, total_tokens=6900)
    result = request_analysis(prepared, "mock", 4096, client)
    assert len(result["plan"]) == 60
    assert all(row["status"] == "needs_review" for row in result["plan"])
    assert all("Perlindungan lokal" in row["alasan"] for row in result["plan"])
    assert any("nilai format" in row["alasan"] for row in result["plan"])
    assert result["usage"]["output_tokens"] == 3900
    assert data == stream.getvalue()


@pytest.mark.parametrize("field,value,reason", [
    ("paragraph_id", "paragraf:999", "ID paragraf"),
    ("rule_code", "invalid", "Aturan tidak didukung"),
    ("target", "invalid", "Target AI"),
    ("action", "font", "Tindakan tidak cocok"),
    ("element_type", "uncertain", "AI belum memastikan"),
    ("reason", "ambiguous", "AI meminta review"),
])
def test_review_reason_is_specific(field, value, reason):
    prepared = prepare_analysis(document(), load_rules(), "S1")
    item = proposal(prepared)
    item[field] = value
    assert reason in validate_plan({"proposals": [item]}, prepared)[0]["alasan"]


def test_incomplete_output_limit_reports_usage_and_no_plan():
    prepared = prepare_analysis(document(), load_rules(), "S1")
    client = client_response({"proposals": [proposal(prepared)]}, status="incomplete")
    client.responses.create.return_value.incomplete_details = SimpleNamespace(reason="max_output_tokens")
    client.responses.create.return_value.usage = SimpleNamespace(input_tokens=100, output_tokens=4096, total_tokens=4196)
    with pytest.raises(AnalysisError) as caught:
        request_analysis(prepared, "mock", 4096, client)
    assert caught.value.category == "output_limit"
    assert caught.value.usage["output_tokens"] == 4096


def test_schema_rejection_has_distinct_safe_error():
    prepared = prepare_analysis(document(), load_rules(), "S1")
    client = Mock()
    exc = RuntimeError("private request payload")
    exc.status_code = 400
    client.responses.create.side_effect = exc
    with pytest.raises(AnalysisError) as caught:
        request_analysis(prepared, "mock", client=client)
    assert caught.value.category == "request_rejected" and "private" not in str(caught.value)


@pytest.mark.parametrize("kind", ["timeout", "api_error", "incomplete", "refusal", "invalid_json", "invalid_schema"])
def test_api_failure_never_returns_partial_plan(kind):
    prepared = prepare_analysis(document(), load_rules(), "S1")
    client = client_response({"proposals": [proposal(prepared)]})
    if kind in ("timeout", "api_error"):
        client.responses.create.side_effect = TimeoutError("private document content") if kind == "timeout" else RuntimeError("private key")
    elif kind == "incomplete":
        client.responses.create.return_value.status = "incomplete"
    elif kind == "refusal":
        client.responses.create.return_value.output = [SimpleNamespace(content=[SimpleNamespace(type="refusal")])]
    elif kind == "invalid_json":
        client.responses.create.return_value.output_text = "{"
    else:
        client.responses.create.return_value.output_text = '{"wrong": []}'
    with pytest.raises(ValueError) as error:
        request_analysis(prepared, "model-test", client=client)
    assert "private" not in str(error.value)
    assert error.value.category == {"timeout": "timeout", "api_error": "api_error", "incomplete": "incomplete", "refusal": "refusal", "invalid_json": "parse_error", "invalid_schema": "schema_error"}[kind]


def test_usage_absent_is_not_assumed_to_be_zero():
    prepared = prepare_analysis(document(), load_rules(), "S1")
    result = request_analysis(prepared, "mock", client=client_response({"proposals": [proposal(prepared)]}))
    assert result["usage"] is None


def test_ai_body_evidence_and_word_defaults_allow_preview_only():
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    doc = Document()
    doc.add_paragraph("SAMPUL SINTETIS", style="Normal")
    doc.add_heading("BAB I PENDAHULUAN", 1)
    text = "Ini paragraf sintetis yang cukup panjang untuk menguji struktur, pewarisan style, dan batas perlindungan lokal dalam pratinjau."
    doc.add_paragraph(text, style="Normal")
    doc.add_paragraph(text, style="Normal").paragraph_format.line_spacing = 1.0
    doc.add_paragraph("Tabel 1 Caption sintetis", style="Caption")
    complex_p = doc.add_paragraph(text, style="Normal")
    complex_p._p.append(OxmlElement("w:fldSimple"))
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "isi tabel sintetis"
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    ppr_default = defaults.find(qn("w:pPrDefault"))
    ppr = ppr_default.find(qn("w:pPr"))
    if ppr is None:
        ppr = OxmlElement("w:pPr")
        ppr_default.append(ppr)
    spacing = ppr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        ppr.append(spacing)
    spacing.set(qn("w:line"), "480")
    spacing.set(qn("w:lineRule"), "auto")
    stream = BytesIO(); doc.save(stream); data = stream.getvalue()
    prepared = prepare_analysis(data, load_rules(), "S1")
    rule = prepared["rules"]["PPKI-LAY-017"]
    base = {"element_type": "body", "rule_code": "PPKI-LAY-017", "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "body_context"}
    proposals = [{**base, "paragraph_id": f"paragraf:{i}"} for i in (1, 3, 4, 5, 6)]
    result = request_analysis(prepared, "mock", client=client_response({"proposals": proposals}))
    byloc = {row["lokasi"]: row for row in result["plan"]}
    assert byloc["paragraf:3"]["status"] == "kandidat_pratinjau"
    assert "Identitas AI" in byloc["paragraf:3"]["alasan"]
    assert "sudah sesuai" in byloc["paragraf:4"]["alasan"]
    assert byloc["paragraf:4"]["status"] == "sudah_sesuai"
    assert sum(row["status"] == "needs_review" for row in result["plan"]) == 3
    assert sum(row["lokasi"] == "ID tidak dikenal" for row in result["plan"]) == 3
    assert stream.getvalue() == data


def test_ai_evidence_requires_known_format_and_strong_chapter_context():
    doc = Document()
    doc.add_heading("BAB I PENDAHULUAN", 1)
    text = "Paragraf sintetis ini cukup panjang untuk menguji keputusan AI tetapi tanpa nilai format yang dapat dipastikan secara deterministik."
    doc.add_paragraph(text, style="Normal")
    # No direct or style value, and remove document defaults to make spacing unknown.
    from docx.oxml.ns import qn
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    ppr_default = defaults.find(qn("w:pPrDefault"))
    if ppr_default is not None:
        defaults.remove(ppr_default)
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_analysis(stream.getvalue(), load_rules(), "S1")
    item = proposal(prepared)
    plan = validate_plan({"proposals": [item]}, prepared)
    assert plan[0]["status"] == "needs_review" and "belum dapat memastikan" in plan[0]["alasan"]


def test_normal_body_inherits_explicit_style_format():
    from docx.enum.style import WD_STYLE_TYPE
    doc = Document()
    doc.add_heading("BAB I PENDAHULUAN", 1)
    parent = doc.styles.add_style("ParentSynthetic", WD_STYLE_TYPE.PARAGRAPH)
    parent.paragraph_format.line_spacing = 2.0
    doc.styles["Normal"].base_style = parent
    doc.add_paragraph("Paragraf sintetis cukup panjang untuk memeriksa bahwa style dan konteks yang jelas dapat menjadi bukti tambahan bagi pratinjau AI.", style="Normal")
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_analysis(stream.getvalue(), load_rules(), "S1")
    assert validate_plan({"proposals": [proposal(prepared)]}, prepared)[0]["status"] == "kandidat_pratinjau"


def test_ai_cannot_override_unconfirmed_chapter():
    from docx.enum.text import WD_BREAK
    doc = Document()
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading("BAB I PENDAHULUAN", 1)
    p = doc.add_paragraph("Paragraf sintetis cukup panjang untuk menguji batas identitas yang bergantung pada konteks bagian dokumen yang benar-benar pasti.", style="Normal")
    p.paragraph_format.line_spacing = 2.0
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_analysis(stream.getvalue(), load_rules(), "S1")
    item = proposal(prepared)
    item["paragraph_id"] = "paragraf:3"
    decision = validate_plan({"proposals": [item]}, prepared)[0]
    assert decision["status"] == "needs_review"
    assert "BAB" in decision["alasan"]


@pytest.mark.parametrize("section_kind", ["landscape", "multiple"])
def test_ai_cannot_override_unsafe_section(section_kind):
    from docx.enum.section import WD_ORIENT, WD_SECTION
    doc = Document()
    if section_kind == "landscape":
        doc.sections[0].orientation = WD_ORIENT.LANDSCAPE
    else:
        doc.add_section(WD_SECTION.NEW_PAGE)
    doc.add_heading("BAB I PENDAHULUAN", 1)
    p = doc.add_paragraph("Paragraf sintetis ini cukup panjang untuk membuktikan bahwa bagian dokumen yang kompleks tetap memerlukan pemeriksaan manual.", style="Normal")
    p.paragraph_format.line_spacing = 2.0
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_analysis(stream.getvalue(), load_rules(), "S1")
    item = proposal(prepared)
    item["paragraph_id"] = f"paragraf:{len(doc.paragraphs)}"
    assert validate_plan({"proposals": [item]}, prepared)[0]["status"] == "needs_review"


def test_streamlit_explicit_consent_and_mocked_preview():
    data = document()
    upload = SimpleNamespace(name="synthetic.docx", getvalue=lambda: data)
    row = {"lokasi": "paragraf:2", "rule_code": "PPKI-LAY-017", "tindakan": "needs_review", "target": "Perlu pemeriksaan", "status": "needs_review", "alasan": "Perlindungan lokal: Identitas teks isi belum pasti."}
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_planner.request_analysis", return_value={"plan": [row], "usage": {"input_tokens": 100, "output_tokens": 50, "total_tokens": 150}}) as request:
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        button = next(b for b in app.button if b.label.startswith("Perbaiki Otomatis dengan AI"))
        button.click().run()
        assert not request.called and not app.exception
        app.text_input[0].set_value("model-test")
        next(c for c in app.checkbox if c.label.startswith("Saya menyetujui pengiriman")).check()
        next(b for b in app.button if b.label.startswith("Perbaiki Otomatis dengan AI")).click().run()
        assert request.call_count == 1 and not app.exception
        assert app.session_state["ai_preview"]["selected"] == 1
        assert any("Token input: 100" in caption.value for caption in app.caption)
        assert app.session_state["ai_preview"]["plan"][0]["alasan"] == row["alasan"]
        request.side_effect = AnalysisError("Batas output tercapai", "output_limit", {"input_tokens": 100, "output_tokens": 4096, "total_tokens": 4196})
        next(b for b in app.button if b.label.startswith("Perbaiki Otomatis dengan AI")).click().run()
        assert app.session_state.get("ai_preview") is None
        assert any("Batas output tercapai" in error.value for error in app.error)
        assert any("output: 4096" in caption.value for caption in app.caption)
        app.selectbox[0].select("S2").run()
        assert app.session_state.get("ai_preview") is None
