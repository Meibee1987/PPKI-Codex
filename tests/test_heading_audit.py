from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from streamlit.testing.v1 import AppTest

from core.audit import audit_docx, heading_candidates
from core.rules import load_rules


def make_heading(title, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    doc = Document()
    para = doc.add_paragraph(style="Heading 1")
    run = para.add_run(title)
    run.bold = bold
    para.alignment = alignment
    stream = BytesIO(); doc.save(stream)
    return stream.getvalue()


@pytest.mark.parametrize("code,title,bold,alignment,expected", [
    ("PPKI-HDG-003", "BAB I PENDAHULUAN", True, WD_ALIGN_PARAGRAPH.CENTER, "pass"),
    ("PPKI-HDG-003", "BAB I Pendahuluan", True, WD_ALIGN_PARAGRAPH.CENTER, "fail"),
    ("PPKI-HDG-004", "BAB I PENDAHULUAN", True, WD_ALIGN_PARAGRAPH.CENTER, "pass"),
    ("PPKI-HDG-004", "BAB I PENDAHULUAN", False, WD_ALIGN_PARAGRAPH.CENTER, "fail"),
    ("PPKI-HDG-004", "BAB I PENDAHULUAN", None, WD_ALIGN_PARAGRAPH.CENTER, "needs_review"),
    ("PPKI-HDG-006", "BAB I PENDAHULUAN", True, WD_ALIGN_PARAGRAPH.CENTER, "pass"),
    ("PPKI-HDG-006", "BAB I PENDAHULUAN", True, WD_ALIGN_PARAGRAPH.LEFT, "fail"),
])
def test_heading_objective_rules(code, title, bold, alignment, expected):
    data = make_heading(title, bold, alignment)
    findings = audit_docx(data, load_rules(), "S1", heading_confirmed={1})
    item = next(f for f in findings if f["rule_code"] == code)
    assert item["status"] == expected
    assert item["location"] == "paragraf:1" and item["expected"] and item["severity"] and item["source_section"]


def test_unconfirmed_and_unsupported_not_claimed_as_pass():
    findings = audit_docx(make_heading("BAB I PENDAHULUAN"), load_rules(), "S2")
    assert next(i for i in findings if i["rule_code"] == "PPKI-HDG-003")["status"] == "needs_review"
    assert next(i for i in findings if i["rule_code"] == "PPKI-HDG-008")["status"] == "not_supported"
    assert next(i for i in findings if i["rule_code"] == "PPKI-HDG-007")["status"] == "not_supported"


def test_context_and_complex_heading_need_review():
    doc = Document()
    doc.add_heading("ABSTRAK", level=1)
    heading = doc.add_heading("BAB I PENDAHULUAN", level=1)
    heading._p.append(OxmlElement("w:hyperlink"))
    doc.add_paragraph("BAB II METODE", style="Normal")
    doc.add_heading("Subbab", level=2)
    doc.add_heading("Sub-subbab", level=3)
    buffer = BytesIO(); doc.save(buffer); data = buffer.getvalue()
    findings = audit_docx(data, load_rules(), "S3", heading_confirmed={1, 2})
    results = [i for i in findings if i["rule_code"] == "PPKI-HDG-003"]
    assert len(results) == 1 and results[0]["location"] == "paragraf:2" and results[0]["status"] == "needs_review"
    assert buffer.getvalue() == data


def test_rules_modified_or_unknown_applicability_not_executed():
    data = make_heading("BAB I PENDAHULUAN")
    rules = load_rules()
    next(r for r in rules if r["rule_code"] == "PPKI-HDG-003")["expected_value_pattern"] = "other"
    next(r for r in rules if r["rule_code"] == "PPKI-HDG-004")["applies_to"] = "Skripsi FKH"
    findings = audit_docx(data, rules, "S1", heading_confirmed={1})
    assert next(i for i in findings if i["rule_code"] == "PPKI-HDG-003")["status"] == "not_supported"
    assert next(i for i in findings if i["rule_code"] == "PPKI-HDG-004")["status"] == "needs_review"


def test_streamlit_heading_candidates_and_confirmation():
    doc = Document(BytesIO(make_heading("BAB I PENDAHULUAN")))
    doc.add_heading("Subbab", level=2); doc.add_heading("Sub-subbab", level=3)
    buffer = BytesIO(); doc.save(buffer); data = buffer.getvalue()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="heading.docx", getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=15).run()
        assert not app.exception
        assert any("Kandidat judul BAB (Heading 1): 1" in x.value for x in app.markdown)
        app.checkbox[1].check(); app.button[0].click().run()
        assert not app.exception
        findings = app.dataframe[1].value
        assert findings[findings["rule_code"] == "PPKI-HDG-003"].iloc[0]["status"] == "pass"


def test_heading_confirmation_persists_for_formatter_reaudit():
    data = make_heading("BAB I PENDAHULUAN")
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="heading.docx", getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=15).run()
        app.checkbox[1].check(); app.button[0].click().run()
        assert app.session_state["audit_t4a"]["heading_confirmed"]
        before = app.session_state["audit_t4a"]["before"]
        next(button for button in app.button if button.label == "Terapkan Perbaikan Otomatis").click().run()
        assert not app.exception
        after = app.session_state["output_t4a"]["after"]
        assert after["sesuai"] > before["sesuai"]
        assert after["perlu_review"] == before["perlu_review"]


def test_master_candidates_and_per_candidate_confirmation():
    path = Path(__file__).parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
    data = path.read_bytes()
    candidates = heading_candidates(data)
    assert [index for index, _ in candidates] == [40, 60, 75]
    assert all(text.startswith("BAB ") for _, text in candidates)
    findings = audit_docx(data, load_rules(), "S1", heading_confirmed={40})
    for code in ("PPKI-HDG-003", "PPKI-HDG-004", "PPKI-HDG-006"):
        items = [item for item in findings if item["rule_code"] == code]
        assert [item["location"] for item in items] == ["paragraf:40", "paragraf:60", "paragraf:75"]
        assert all(item["status"] == "needs_review" for item in items[1:])
        assert all("belum dikonfirmasi" in item["message"] for item in items[1:])
    assert path.read_bytes() == data


def test_master_streamlit_checkboxes_are_independent_of_body_style():
    path = Path(__file__).parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
    data = path.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=path.name, getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=15).run()
        assert app.selectbox[1].value is None
        assert len(app.checkbox) >= 5
        assert [c.label.split(":", 1)[0] for c in app.checkbox[1:4]] == ["Paragraf 40", "Paragraf 60", "Paragraf 75"]
        app.checkbox[1].check(); app.button[0].click().run()
        assert not app.exception
        assert app.session_state["audit_t4a"]["heading_confirmed"] == {40}
        findings = app.dataframe[1].value
        hdg = findings[findings["rule_code"] == "PPKI-HDG-003"]
        assert hdg[hdg["location"] == "paragraf:60"].iloc[0]["status"] == "needs_review"
        assert hdg[hdg["location"] == "paragraf:40"].iloc[0]["status"] != "needs_review"
