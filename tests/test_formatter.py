from io import BytesIO
from zipfile import ZipFile

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
import base64

from core.formatter import format_docx, plan_changes
from core.rules import load_rules


def sample():
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.left_margin, section.right_margin = Cm(4), Cm(3)
    section.top_margin, section.bottom_margin = Cm(3), Cm(3)
    paragraph = doc.add_paragraph("Teks penelitian", style="Body Text")
    paragraph.paragraph_format.line_spacing = 1.5
    paragraph.paragraph_format.first_line_indent = Cm(2)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    other = doc.add_paragraph("Heading", style="Heading 1")
    other.paragraph_format.line_spacing = 1.5
    complex_p = doc.add_paragraph("Catatan", style="Body Text")
    complex_p.paragraph_format.line_spacing = 1.5
    complex_p._p.append(OxmlElement("w:hyperlink"))
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Isi tabel"
    stream = BytesIO()
    doc.save(stream)
    return stream.getvalue()


def test_format_copy_audit_and_idempotence():
    data = sample()
    rules = load_rules()
    output, findings, changes = format_docx(data, rules, "S1", "BodyText", True)
    assert {item["rule_code"] for item in changes} == {"PPKI-LAY-017", "PPKI-LAY-018", "PPKI-LAY-019"}
    before, after = Document(BytesIO(data)), Document(BytesIO(output))
    p = after.paragraphs[0]
    assert p.paragraph_format.line_spacing == 1.0
    assert abs(p.paragraph_format.first_line_indent.cm - 1) < 0.02
    assert p.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
    assert [p.text for p in before.paragraphs] == [p.text for p in after.paragraphs]
    assert before.tables[0].cell(0, 0).text == after.tables[0].cell(0, 0).text
    assert before.paragraphs[1]._p.xml == after.paragraphs[1]._p.xml
    assert before.paragraphs[2]._p.xml == after.paragraphs[2]._p.xml
    assert all(next(f for f in findings if f["rule_code"] == c["rule_code"] and f["location"] == c["location"])["status"] == "pass" for c in changes)
    with ZipFile(BytesIO(data)) as a, ZipFile(BytesIO(output)) as b:
        assert all(a.read(n) == b.read(n) for n in a.namelist() if n != "word/document.xml")
    second, _, changes_again = format_docx(output, rules, "S1", "BodyText", True)
    assert changes_again == [] and second == output


def test_requires_confirmation_and_skips_manual_or_confirm():
    rules = load_rules()
    assert not plan_changes(sample(), rules, "S1", "BodyText", False)
    original = sample()
    untouched, _, changes = format_docx(original, rules, "S1", "BodyText", False)
    assert untouched == original and not changes
    for rule in rules:
        if rule["rule_code"] == "PPKI-LAY-017":
            rule["fix_mode"] = "Manual"
        if rule["rule_code"] == "PPKI-LAY-018":
            rule["fix_mode"] = "Confirm"
    _, _, changes = format_docx(sample(), rules, "S1", "BodyText", True)
    assert [item["rule_code"] for item in changes] == ["PPKI-LAY-019"]


def test_validation_failure_rejects_output(monkeypatch):
    from core import formatter
    monkeypatch.setattr(formatter, "_document_structure", lambda xml, changes: xml)
    with pytest.raises(ValueError, match="struktur dokumen berubah"):
        format_docx(sample(), load_rules(), "S1", "BodyText", True)


def page_sample():
    doc = Document()
    doc.add_paragraph("Teks utama")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Tabel"
    doc.sections[0].header.paragraphs[0].text = "Header"
    doc.sections[0].footer.paragraphs[0].text = "Footer"
    image = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/a5sAAAAASUVORK5CYII=")
    doc.add_picture(BytesIO(image))
    doc.add_section()
    one, two = doc.sections[0], doc.sections[1]
    one.page_width, one.page_height = Cm(20), Cm(28)
    one.left_margin, one.right_margin = Cm(2), Cm(2)
    one.top_margin, one.bottom_margin = Cm(2), Cm(2)
    two.page_width, two.page_height = Cm(21), Cm(29.7)
    two.left_margin, two.right_margin = Cm(4), Cm(3)
    two.top_margin, two.bottom_margin = Cm(3), Cm(3)
    stream = BytesIO()
    doc.save(stream)
    return stream.getvalue()


def test_page_format_all_rules_two_sections_preserve_contents_and_idempotence():
    data = page_sample()
    rules = load_rules()
    output, after, changes = format_docx(data, rules, "S1", None, False)
    assert len(changes) == 5
    assert {item["rule_code"] for item in changes} == {"PPKI-LAY-003", "PPKI-LAY-008", "PPKI-LAY-009", "PPKI-LAY-010", "PPKI-LAY-011"}
    assert all(item["location"] == "section:1" for item in changes)
    before_doc, after_doc = Document(BytesIO(data)), Document(BytesIO(output))
    assert before_doc.sections[1]._sectPr.xml == after_doc.sections[1]._sectPr.xml
    assert [p.text for p in before_doc.paragraphs] == [p.text for p in after_doc.paragraphs]
    assert before_doc.tables[0].cell(0, 0).text == after_doc.tables[0].cell(0, 0).text
    assert after_doc.sections[0].header.paragraphs[0].text == "Header"
    assert after_doc.sections[0].footer.paragraphs[0].text == "Footer"
    assert len(before_doc.inline_shapes) == len(after_doc.inline_shapes) == 1
    assert all(next(f for f in after if f["rule_code"] == c["rule_code"] and f["location"] == c["location"])["status"] == "pass" for c in changes)
    with ZipFile(BytesIO(data)) as a, ZipFile(BytesIO(output)) as b:
        assert all(a.read(name) == b.read(name) for name in a.namelist() if name != "word/document.xml")
    second, _, again = format_docx(output, rules, "S1", None, False)
    assert not again and second == output


def test_landscape_section_skipped_and_manual_rule_skipped():
    doc = Document(BytesIO(page_sample()))
    doc.sections[0].orientation = WD_ORIENT.LANDSCAPE
    stream = BytesIO(); doc.save(stream)
    assert not [c for c in plan_changes(stream.getvalue(), load_rules(), "S1", None, False) if c["location"] == "section:1"]
    rules = load_rules()
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-008")["fix_mode"] = "Manual"
    assert "PPKI-LAY-008" not in {c["rule_code"] for c in plan_changes(page_sample(), rules, "S1", None, False)}


@pytest.mark.parametrize("num,explicit_columns,expected", [(None, 0, True), ("1", 1, True), (None, 1, True), ("2", 0, False), ("2", 2, False), ("1", 2, False), ("invalid", 0, False)])
def test_effective_columns(num, explicit_columns, expected):
    from core.formatter import section_is_safe
    doc = Document()
    section = doc.sections[0]
    columns = section._sectPr.find(qn("w:cols"))
    if num is not None:
        columns.set(qn("w:num"), num)
    for _ in range(explicit_columns):
        columns.append(OxmlElement("w:col"))
    assert section_is_safe(section) is expected


def test_s1_fixture_page_plan_and_specific_skip_reasons():
    from pathlib import Path
    from core.audit import audit_docx
    from core.formatter import skipped_changes
    data = (Path(__file__).parent / "fixtures" / "PPKI_T4B_01_Skripsi_S1_Dasar.docx").read_bytes()
    rules = load_rules()
    plan = plan_changes(data, rules, "S1", None, False)
    assert {item["rule_code"] for item in plan} == {"PPKI-LAY-003", "PPKI-LAY-008", "PPKI-LAY-009", "PPKI-LAY-010", "PPKI-LAY-011"}
    result, after, changes = format_docx(data, rules, "S1", None, False)
    assert len(changes) == 5 and Document(BytesIO(result))
    assert all(next(f for f in after if f["rule_code"] == item["rule_code"] and f["location"] == item["location"])["status"] == "pass" for item in changes)
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-008")["fix_mode"] = "Manual"
    findings = audit_docx(data, rules, "S1", None, False)
    plan = plan_changes(data, rules, "S1", None, False)
    skipped = skipped_changes(data, rules, "S1", findings, plan, None, False)
    assert "fix_mode=Manual" in next(item for item in skipped if item["rule_code"] == "PPKI-LAY-008")["alasan_dilewati"]


def test_single_explicit_column_s1_is_formatted():
    from pathlib import Path
    data = (Path(__file__).parent / "fixtures" / "PPKI_T4B_01_Skripsi_S1_Dasar.docx").read_bytes()
    doc = Document(BytesIO(data))
    columns = doc.sections[0]._sectPr.find(qn("w:cols"))
    columns.set(qn("w:num"), "1")
    columns.append(OxmlElement("w:col"))
    buffer = BytesIO(); doc.save(buffer)
    output, after, changes = format_docx(buffer.getvalue(), load_rules(), "S1", None, False)
    assert len(changes) == 5 and Document(BytesIO(output))


def test_s1_streamlit_page_audit_without_style_confirmation():
    from pathlib import Path
    from types import SimpleNamespace
    from unittest.mock import patch
    from streamlit.testing.v1 import AppTest
    path = Path(__file__).parent / "fixtures" / "PPKI_T4B_01_Skripsi_S1_Dasar.docx"
    data = path.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=path.name, getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py").run()
        app.button[0].click().run()
        assert not app.exception
        assert len(app.session_state["audit_t4a"]["plan"]) == 5
        next(button for button in app.button if button.label == "Terapkan Perbaikan").click().run()
        assert not app.exception
        assert len(app.session_state["output_t4a"]["changes"]) == 5
        assert len(app.get("download_button")) == 2


def test_skipped_reason_for_landscape_and_multiple_columns():
    from core.audit import audit_docx
    from core.formatter import skipped_changes
    rules = load_rules()
    doc = Document(BytesIO(page_sample()))
    doc.sections[0].orientation = WD_ORIENT.LANDSCAPE
    columns = doc.sections[1]._sectPr.find(qn("w:cols"))
    columns.set(qn("w:num"), "2")
    doc.sections[1].left_margin = Cm(2)
    stream = BytesIO(); doc.save(stream); data = stream.getvalue()
    findings = audit_docx(data, rules, "S1", None, False)
    plan = plan_changes(data, rules, "S1", None, False)
    skipped = skipped_changes(data, rules, "S1", findings, plan, None, False)
    assert "landscape" in next(i for i in skipped if i["location"] == "section:1")["alasan_dilewati"]
    assert "2 kolom" in next(i for i in skipped if i["location"] == "section:2")["alasan_dilewati"]
