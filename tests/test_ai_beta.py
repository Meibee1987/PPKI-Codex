from io import BytesIO
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch
import json

import pytest
from docx import Document
from docx.oxml import OxmlElement
from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from streamlit.testing.v1 import AppTest

from core.ai_beta import prepare_beta, request_classifications, request_batches, validate_classifications, format_beta, evaluation_sample, evaluation_estimate, evaluation_stratified, import_evaluation_labels, comparison_counts, semantic_evidence
from core.ai_planner import AnalysisError
from core.rules import load_rules
from test_pilot import sample


class MockClient:
    def __init__(self, prepared, role="body"):
        self.responses = self
        self.prepared = prepared
        self.role = role

    def create(self, **kwargs):
        assert kwargs["store"] is False
        rows = [{"id": location, "role": self.role, "reason": "synthetic"} for location in self.prepared["selected"]]
        return SimpleNamespace(status="completed", output_text=json.dumps({"classifications": rows}), output=[], usage=None)


def test_mock_beta_changes_copy_and_preserves_special_parts():
    original = sample()
    rules = load_rules()
    prepared = prepare_beta(original, rules, "S1")
    assert "paragraf:3" in prepared["selected"]
    decisions, _ = request_classifications(prepared, "mock", 1024, MockClient(prepared))
    result = format_beta(original, rules, "S1", prepared, decisions)
    assert result["summary"]["planned"] > 0
    assert result["summary"]["unknown_to_normalize"] > 0
    applied = [row for row in result["operations"] if row["status"] == "applied"]
    assert len(applied) == result["summary"]["planned"]
    assert all(row["sebelum"] != row["sesudah"] for row in applied)
    assert all(row["status"] == "protected" for row in result["operations"] if row["lokasi"] == "paragraf:2")
    before, after = Document(BytesIO(original)), Document(BytesIO(result["data"]))
    assert [p.text for p in before.paragraphs] == [p.text for p in after.paragraphs]
    assert after.paragraphs[2].runs[0].bold and after.paragraphs[2].runs[0].italic
    assert after.paragraphs[2].runs[0].font.name == "Times New Roman"
    assert before.paragraphs[4]._p.xml == after.paragraphs[4]._p.xml
    assert before.tables[0]._tbl.xml == after.tables[0]._tbl.xml
    again_prepared = prepare_beta(result["data"], rules, "S1")
    again_decisions, _ = request_classifications(again_prepared, "mock", 1024, MockClient(again_prepared))
    again = format_beta(result["data"], rules, "S1", again_prepared, again_decisions)
    assert again["summary"]["planned"] == 0


def test_quote_and_unmarked_uncertain_are_not_changed():
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2].runs[0].text = '"Kutipan sintetis yang secara eksplisit ditandai dan harus dilindungi dari perubahan."'
    stream = BytesIO(); doc.save(stream)
    original = stream.getvalue(); rules = load_rules()
    prepared = prepare_beta(original, rules, "S1")
    assert next(x for x in prepared["local"] if x["lokasi"] == "paragraf:3")["status"] == "protected"
    decisions, _ = request_classifications(prepared, "mock", 1024, MockClient(prepared, "uncertain"))
    result = format_beta(original, rules, "S1", prepared, decisions)
    assert result["data"] == original


def test_invalid_ids_rules_and_protected_override_rejected():
    data = sample(); rules = load_rules(); prepared = prepare_beta(data, rules, "S1")
    with pytest.raises(ValueError):
        validate_classifications({"classifications": [{"id": "paragraf:9999", "role": "body", "reason": "x", "rule_code": "fake"}]}, prepared)
    decisions, _ = request_classifications(prepared, "mock", 1024, MockClient(prepared))
    next(x for x in decisions if x["lokasi"] == "paragraf:2")["status"] = "auto_candidate"
    with pytest.raises(ValueError):
        format_beta(data, rules, "S1", prepared, decisions)


def test_api_error_does_not_produce_partial_decisions():
    prepared = prepare_beta(sample(), load_rules(), "S1")
    class Broken:
        responses = None
        def __init__(self): self.responses = self
        def create(self, **kwargs): raise TimeoutError("private")
    with pytest.raises(AnalysisError, match="tidak ada perubahan"):
        request_classifications(prepared, "mock", 1024, Broken())


@pytest.mark.parametrize("payload", ["not json", '{"classifications": []}'])
def test_invalid_ai_response_cancels_batch(payload):
    prepared = prepare_beta(sample(), load_rules(), "S1")
    class Invalid:
        responses = None
        def __init__(self): self.responses = self
        def create(self, **kwargs):
            return SimpleNamespace(status="completed", output_text=payload, output=[], usage=None)
    with pytest.raises(AnalysisError, match="tidak valid"):
        request_classifications(prepared, "mock", 1024, Invalid())


@pytest.mark.parametrize("tag", ["w:hyperlink", "w:fldSimple", "w:drawing", "w:ins"])
def test_complex_content_cannot_be_selected_by_ai(tag):
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2]._p.append(OxmlElement(tag))
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_beta(stream.getvalue(), load_rules(), "S1")
    assert "paragraf:3" not in prepared["selected"]


def test_landscape_is_not_ai_candidate():
    doc = Document(BytesIO(sample())); doc.sections[0].orientation = WD_ORIENT.LANDSCAPE
    stream = BytesIO(); doc.save(stream)
    assert "paragraf:3" not in prepare_beta(stream.getvalue(), load_rules(), "S1")["selected"]


def test_failed_integrity_cancels_beta(monkeypatch):
    from core import pilot
    data = sample(); rules = load_rules(); prepared = prepare_beta(data, rules, "S1")
    decisions, _ = request_classifications(prepared, "mock", 1024, MockClient(prepared))
    monkeypatch.setattr(pilot, "_document_structure", lambda xml, changes: xml)
    with pytest.raises(ValueError, match="struktur"):
        format_beta(data, rules, "S1", prepared, decisions)


def test_streamlit_beta_consent_and_download():
    data = sample(); upload = SimpleNamespace(name="dummy.docx", getvalue=lambda: data)
    def mocked(prepared, model, tokens, client=None):
        return request_classifications(prepared, "mock", 1024, MockClient(prepared))
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_beta.request_classifications", side_effect=mocked):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(b for b in app.button if b.label.endswith("Beta")).click().run()
        assert not app.exception and not app.get("download_button")
        next(c for c in app.checkbox if c.label.startswith("Saya menyetujui pengiriman teks")).check().run()
        next(b for b in app.button if b.label.endswith("Beta")).click().run()
        assert not app.exception and len(app.get("download_button")) == 2, ([x.value for x in app.error], [x.value for x in app.warning])
        assert app.session_state["beta_result"]["data"] != data and upload.getvalue() == data
        with patch("core.pilot._document_structure", side_effect=lambda xml, changes: xml):
            next(b for b in app.button if b.label.endswith("Beta")).click().run()
            assert not app.exception and app.error
            assert len(app.get("download_button")) == 1
            assert all(row["status"] == "failed" for row in app.session_state["beta_failure"])
            assert app.session_state.get("beta_result") is None


class BatchClient:
    def __init__(self, fail_at=None, invalid_at=None):
        self.responses = self
        self.calls = []
        self.fail_at = fail_at
        self.invalid_at = invalid_at

    def create(self, **kwargs):
        rows = json.loads(kwargs["input"])["paragraphs"]
        self.calls.append(rows)
        if len(self.calls) == self.fail_at:
            raise TimeoutError("private")
        classifications = [{"id": r["id"], "role": "body", "reason": "mock"} for r in rows]
        if len(self.calls) == self.invalid_at:
            classifications[0]["id"] = "invalid"
        return SimpleNamespace(status="completed", output_text=json.dumps({"classifications": classifications}), output=[],
                               usage=SimpleNamespace(input_tokens=100, output_tokens=50, total_tokens=150))


def test_198_candidates_processed_once_and_context_preserved():
    prepared = prepare_beta(sample(), load_rules(), "S1", all_candidates=True)
    source = prepared["request"]["paragraphs"][0]
    rows = [{**source, "id": f"paragraf:{i}", "chapter": i // 40 + 1} for i in range(1, 199)]
    prepared["request"]["paragraphs"] = rows
    prepared["selected"] = {r["id"]: {} for r in rows}
    prepared["local"] = [{"lokasi": r["id"], "status": "uncertain", "alasan": "x"} for r in rows]
    client = BatchClient()
    result = request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=client)
    flattened = [r for batch in client.calls for r in batch]
    assert len(client.calls) == 7 and len(flattened) == 198
    assert len({r["id"] for r in flattened}) == 198 and flattened == rows
    assert result["unprocessed"] == 0 and result["input_tokens"] == 700 and result["output_tokens"] == 350
    assert all(x["status"] == "body_verified" for x in result["decisions"])
    partial = request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=BatchClient(fail_at=2))
    assert partial["unprocessed"] == 168
    assert sum(x["status"] == "body_verified" for x in partial["decisions"]) == 30


def test_batch_budget_failure_and_invalid_response():
    prepared = prepare_beta(sample(), load_rules(), "S1", all_candidates=True)
    client = BatchClient()
    result = request_batches(prepared, "mock", 1024, budget=0.000001, input_price=1, output_price=1, client=client)
    assert not client.calls and result["unprocessed"] == len(prepared["selected"])
    client = BatchClient(fail_at=1)
    result = request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=client)
    assert result["unprocessed"] == len(prepared["selected"])
    with pytest.raises(AnalysisError):
        request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=BatchClient(invalid_at=1))


def test_synthetic_labeled_special_content_stays_out_of_verified_body():
    doc = Document(BytesIO(sample()))
    quotation = doc.add_paragraph("Teks kutipan panjang sintetis tanpa tanda eksplisit dan memerlukan pemeriksaan manusia.", style="Body Text")
    quotation.paragraph_format.left_indent = Cm(1)
    doc.paragraphs[3]._p.addprevious(quotation._p)
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_beta(stream.getvalue(), load_rules(), "S1", all_candidates=True)
    result = request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=BatchClient())
    statuses = {x["lokasi"]: x["status"] for x in result["decisions"]}
    assert statuses["paragraf:3"] == "body_verified"
    assert statuses["paragraf:2"] == "protected"  # heading
    assert statuses["paragraf:7"] == "protected"  # caption
    assert statuses["paragraf:4"] in {"uncertain", "protected"}


def test_labeled_front_matter_references_and_appendix_do_not_become_body():
    doc = Document()
    doc.add_heading("DAFTAR ISI", 1)
    doc.add_paragraph("BAB I PENDAHULUAN ........... 1")
    doc.add_heading("BAB I PENDAHULUAN", 1)
    doc.add_paragraph("Ini adalah paragraf isi sintetis yang cukup panjang untuk memeriksa klasifikasi dan operasi pada dokumen.", style="Body Text")
    doc.add_paragraph("Gambar 1. Gambar sintetis", style="Caption")
    field = doc.add_paragraph("Konten field sintetis dalam paragraf.", style="Body Text")
    field._p.append(OxmlElement("w:fldSimple"))
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_paragraph("Referensi sintetis, 2024.", style="Normal")
    doc.add_heading("LAMPIRAN", 1)
    doc.add_paragraph("Isi lampiran sintetis.", style="Normal")
    stream = BytesIO(); doc.save(stream)
    prepared = prepare_beta(stream.getvalue(), load_rules(), "S1", all_candidates=True)
    result = request_batches(prepared, "mock", 1024, budget=100, input_price=1, output_price=1, client=BatchClient())
    statuses = {x["lokasi"]: x["status"] for x in result["decisions"]}
    for number in (1, 2, 3, 5, 6, 7, 8, 9, 10):
        assert statuses[f"paragraf:{number}"] != "body_verified"


def test_evaluation_sample_spreads_chapters_and_keeps_unique_ids():
    prepared = prepare_beta(sample(), load_rules(), "S1", all_candidates=True)
    source = prepared["request"]["paragraphs"][0]
    rows = [{**source, "id": f"paragraf:{i}", "chapter": (i - 1) // 5 + 1} for i in range(1, 26)]
    prepared["request"]["paragraphs"] = rows
    prepared["selected"] = {r["id"]: {} for r in rows}
    prepared["local"] = [{"lokasi": r["id"], "status": "uncertain", "alasan": "x"} for r in rows]
    subset = evaluation_sample(prepared)
    assert len(subset["selected"]) == 15
    assert {r["chapter"] for r in subset["request"]["paragraphs"]} == {1, 2, 3, 4, 5}
    assert len({r["id"] for r in subset["request"]["paragraphs"]}) == 15
    estimated, cost = evaluation_estimate(subset, 1024, 1, 2)
    assert estimated > 0 and cost == (estimated + 2048) / 1000000
    decisions, usage = request_classifications(subset, "mock", 1024, BatchClient(), include_reason=True)
    assert all(x["ai_role"] == "body" and x["ai_reason"] == "mock" for x in decisions)
    assert usage["total_tokens"] == 150
    prepared["local"][0]["status"] = "protected"
    with pytest.raises(ValueError):
        evaluation_sample(prepared)


def test_evaluation_app_requires_consent_and_never_formats():
    data = sample(); upload = SimpleNamespace(name="dummy.docx", getvalue=lambda: data)
    def mocked(prepared, model, tokens, **kwargs):
        return request_classifications(prepared, "mock", 1024, BatchClient(), include_reason=True)
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_beta.request_classifications", side_effect=mocked) as request, patch("core.ai_beta.format_beta") as formatter:
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(b for b in app.button if b.label == "Siapkan sampel evaluasi").click().run()
        assert any(box.label.startswith("Penilaian operator paragraf:") for box in app.selectbox)
        next(b for b in app.button if b.label == "Kirim sampel evaluasi AI").click().run()
        assert not request.called and not formatter.called
        next(c for c in app.checkbox if c.label.startswith("Saya menyetujui pengiriman sampel evaluasi")).check().run()
        next(b for b in app.button if b.label == "Kirim sampel evaluasi AI").click().run()
        assert not app.exception and request.call_count == 1 and not formatter.called
        assert upload.getvalue() == data and app.session_state["evaluation_result"]["usage"]["total_tokens"] == 150
        with patch("core.ai_beta.request_classifications", side_effect=AnalysisError("Evaluasi gagal", "api_error")):
            next(b for b in app.button if b.label == "Kirim sampel evaluasi AI").click().run()
            assert app.error and not formatter.called and app.session_state.get("evaluation_result") is None
            assert upload.getvalue() == data


def test_stratified_evaluation_never_grants_formatter_permission():
    doc = Document(BytesIO(sample()))
    quotation = doc.add_paragraph("Sampel sintetis dengan indentasi kiri untuk evaluasi tanpa izin pemformatan.", style="Body Text")
    quotation.paragraph_format.left_indent = Cm(1)
    doc.paragraphs[3]._p.addprevious(quotation._p)
    stream = BytesIO(); doc.save(stream)
    original = stream.getvalue(); rules = load_rules()
    prepared = evaluation_stratified(original, rules, "S1")
    assert len(prepared["selected"]) <= 20
    assert {r["sample_group"] for r in prepared["request"]["paragraphs"]} >= {"eligible", "special"}
    result, _ = request_classifications(prepared, "mock", 1024, BatchClient(), include_reason=True)
    assert all(x["status"] != "auto_candidate" for x in result)
    assert any(x["status"] == "protected" and x["ai_role"] == "body" for x in result)
    with pytest.raises(ValueError, match="evaluasi"):
        format_beta(original, rules, "S1", prepared, result)
    assert stream.getvalue() == original


def test_semantic_citation_proposition_and_list_are_distinct():
    doc = Document()
    body = doc.add_paragraph("Penelitian sebelumnya (Sari, 2022) menunjukkan hasil berbeda.")
    proposition = doc.add_paragraph("P1: proposisi sintetis.")
    continuation = doc.add_paragraph("Penjelasan daftar sintetis.")
    continuation.paragraph_format.left_indent = Cm(1)
    assert semantic_evidence(body) == "citation_only"
    assert semantic_evidence(proposition) == "proposition"
    assert semantic_evidence(continuation, proposition) == "list_continuation"
    ordinary_indent = doc.add_paragraph("Teks isi berindentasi tidak otomatis kutipan.")
    ordinary_indent.paragraph_format.left_indent = Cm(1)
    assert semantic_evidence(ordinary_indent, body) == "unknown"


def test_proposition_and_list_continuation_never_become_auto_candidates():
    doc = Document(BytesIO(sample()))
    para = doc.paragraphs[2]
    para.runs[0].text = "P1: proposisi sintetis yang tidak boleh diperlakukan sebagai teks isi biasa."
    following = doc.paragraphs[3]
    following.paragraph_format.left_indent = Cm(1)
    stream = BytesIO(); doc.save(stream)
    data = stream.getvalue(); rules = load_rules(); prepared = prepare_beta(data, rules, "S1", all_candidates=True)
    local = {entry["lokasi"]: entry for entry in prepared["local"]}
    assert local["paragraf:3"]["status"] == "protected" and "paragraf:3" not in prepared["selected"]
    assert local["paragraf:4"]["status"] == "protected" and "paragraf:4" not in prepared["selected"]
    assert stream.getvalue() == data


def test_evaluation_keeps_ai_raw_and_downgrades_uncertain_citation():
    prepared = {"evaluation_only": True, "selected": {"paragraf:1": {}, "paragraf:2": {}}, "local": [
        {"lokasi": "paragraf:1", "status": "uncertain", "alasan": "x", "evidence": "citation_only"},
        {"lokasi": "paragraf:2", "status": "protected", "alasan": "x", "evidence": "proposition"}]}
    result = validate_classifications({"classifications": [
        {"id": "paragraf:1", "role": "quote", "reason": "mock"},
        {"id": "paragraf:2", "role": "body", "reason": "mock"}]}, prepared, include_reason=True)
    assert [r["ai_role"] for r in result] == ["quote", "body"]
    assert [r["effective_role"] for r in result] == ["uncertain", "special"]
    assert result[1]["status"] == "protected"


def test_production_uses_same_conservative_decisions_as_evaluation():
    entries = [
        {"lokasi": "paragraf:1", "status": "protected", "alasan": "khusus", "evidence": "proposition"},
        {"lokasi": "paragraf:2", "status": "protected", "alasan": "khusus", "evidence": "list_continuation"},
    ] + [{"lokasi": f"paragraf:{i}", "status": "uncertain", "alasan": "lain", "evidence": "citation_only"} for i in (3, 4, 5)] + [
        {"lokasi": f"paragraf:{i}", "status": "uncertain", "alasan": "Indentasi khusus perlu review", "evidence": "unknown"} for i in (6, 7)]
    payload = {"classifications": [{"id": e["lokasi"], "role": "quote" if e["evidence"] == "citation_only" else "body", "reason": "mock"} for e in entries]}
    base = {"selected": {e["lokasi"]: {} for e in entries}, "local": entries}
    evaluation = validate_classifications(payload, {**base, "evaluation_only": True}, include_reason=True)
    production = validate_classifications(payload, base)
    assert [e["effective_role"] for e in evaluation] == ["special", "special"] + ["uncertain"] * 5
    assert [e["status"] for e in production] == ["protected", "protected"] + ["uncertain"] * 5


def test_csv_import_rejects_wrong_ids_duplicates_and_metadata():
    prepared = {"evaluation_only": True, "request": {"paragraphs": [
        {"id": "paragraf:1", "chapter": 1, "sample_group": "eligible"},
        {"id": "paragraf:2", "chapter": 2, "sample_group": "indent"}]}}
    header = "id_paragraf,bab,kelompok_sampel,prediksi_AI,label_acuan_formatting\n"
    data = header + "paragraf:1,1,eligible,body,teks_isi\nparagraf:2,2,indent,body,bagian_khusus\n"
    labels = import_evaluation_labels(data.encode(), prepared)
    assert comparison_counts({k: v["label"] for k, v in labels.items()}, {k: v["prediction"] for k, v in labels.items()}) == {"tp": 1, "fp": 1}
    for bad in (data.replace("paragraf:2", "paragraf:1"), data.replace(",2,indent", ",3,indent"), data.replace("bagian_khusus", "unknown")):
        with pytest.raises(ValueError):
            import_evaluation_labels(bad.encode(), prepared)


def test_streamlit_csv_import_does_not_request_ai_or_format():
    data = sample(); doc_upload = SimpleNamespace(name="dummy.docx", getvalue=lambda: data)
    prepared = evaluation_stratified(data, load_rules(), "S1")
    csv_text = "id_paragraf,bab,kelompok_sampel,prediksi_AI,label_acuan_formatting\n"
    for row in prepared["request"]["paragraphs"]:
        chapter = row["chapter"] if row["chapter"] is not None else "bagian_awal"
        csv_text += f"{row['id']},{chapter},{row['sample_group']},body,teks_isi\n"
    csv_upload = SimpleNamespace(name="labels.csv", getvalue=lambda: csv_text.encode())
    def uploader(label, **kwargs):
        return csv_upload if label.startswith("Impor CSV") else doc_upload
    with patch("streamlit.file_uploader", side_effect=uploader), patch("core.ai_beta.request_classifications") as request, patch("core.ai_beta.format_beta") as formatter:
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(b for b in app.button if b.label == "Siapkan sampel evaluasi").click().run()
        next(b for b in app.button if b.label == "Impor label CSV").click().run()
        assert not app.exception and not app.error
        assert all(box.value == "teks_isi" for box in app.selectbox if box.label.startswith("Penilaian operator"))
        assert not request.called and not formatter.called and doc_upload.getvalue() == data


def test_master_beta_result_rerun_and_stale_state_are_safe():
    path = Path(__file__).resolve().parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
    data = path.read_bytes(); upload = SimpleNamespace(name="master.docx", getvalue=lambda: data)
    client = BatchClient()
    def mocked(prepared, model, tokens, client=None):
        return request_classifications(prepared, "mock", 1024, client=client_for_test)
    client_for_test = client
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_beta.request_classifications", side_effect=mocked) as request:
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=120).run()
        next(c for c in app.checkbox if c.label.startswith("Saya menyetujui pengiriman teks")).check().run()
        next(b for b in app.button if b.label.endswith("Beta")).click().run()
        assert not app.exception and not app.error
        assert len(client.calls) == 1 and len(client.calls[0]) == 23
        assert app.session_state["beta_result"]["summary"]["planned"] == 3
        assert len(app.get("download_button")) == 2 and request.call_count == 1
        app.run()
        assert not app.exception and len(app.get("download_button")) == 2 and request.call_count == 1
        stale = dict(app.session_state["beta_result"]); stale.pop("operations")
        app.session_state["beta_result"] = stale
        app.run()
        assert not app.exception and app.error and not app.get("download_button")
        assert app.session_state.get("beta_result") is None and request.call_count == 1
        next(b for b in app.button if b.label.endswith("Beta")).click().run()
        assert not app.exception and request.call_count == 2 and len(app.get("download_button")) == 2
        next(t for t in app.text_input if t.label == "Model OpenAI yang tersedia pada akun API").set_value("model-berbeda").run()
        assert not app.exception and not app.get("download_button")
        assert app.session_state.get("beta_result") is None and request.call_count == 2


def test_incomplete_operation_report_never_produces_download():
    data = sample(); upload = SimpleNamespace(name="dummy.docx", getvalue=lambda: data)
    def mocked(prepared, model, tokens, client=None):
        return request_classifications(prepared, "mock", 1024, MockClient(prepared))
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_beta.request_classifications", side_effect=mocked), patch("core.ai_beta.operation_report", return_value=[]):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(c for c in app.checkbox if c.label.startswith("Saya menyetujui pengiriman teks")).check().run()
        next(b for b in app.button if b.label.endswith("Beta")).click().run()
        assert not app.exception and app.error and not app.get("download_button")
        assert app.session_state.get("beta_result") is None

