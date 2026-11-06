from io import BytesIO

import pytest
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

from core.audit import audit_docx, summarize
from core.rules import load_rules


def make_doc():
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.left_margin, section.right_margin = Cm(4), Cm(3)
    section.top_margin, section.bottom_margin = Cm(3), Cm(3)
    doc.add_paragraph("Teks sintetis")
    stream = BytesIO()
    doc.save(stream)
    return stream.getvalue()


@pytest.mark.parametrize("code", ["PPKI-LAY-003", "PPKI-LAY-008", "PPKI-LAY-009", "PPKI-LAY-010", "PPKI-LAY-011"])
def test_page_rules_pass_and_traceability(code):
    data = make_doc()
    findings = audit_docx(data, load_rules(), "S1")
    item = next(item for item in findings if item["rule_code"] == code)
    assert item["status"] == "pass"
    assert item["severity"] == "Error"
    assert item["pdf_page"] == 161
    assert item["source_section"]
    assert Document(BytesIO(data)).paragraphs[0].text == "Teks sintetis"


@pytest.mark.parametrize("code,attribute,value", [("PPKI-LAY-003", "page_width", 20), ("PPKI-LAY-008", "left_margin", 3), ("PPKI-LAY-009", "right_margin", 4), ("PPKI-LAY-010", "top_margin", 4), ("PPKI-LAY-011", "bottom_margin", 4)])
def test_page_rules_fail(code, attribute, value):
    doc = Document(BytesIO(make_doc()))
    setattr(doc.sections[0], attribute, Cm(value))
    stream = BytesIO()
    doc.save(stream)
    item = next(item for item in audit_docx(stream.getvalue(), load_rules(), "S1") if item["rule_code"] == code)
    assert item["status"] == "fail"


def test_multiple_sections_and_font_review():
    doc = Document(BytesIO(make_doc()))
    doc.add_section()
    doc.sections[1].left_margin = Cm(2)
    stream = BytesIO()
    doc.save(stream)
    results = audit_docx(stream.getvalue(), load_rules(), "S1")
    left = [item for item in results if item["rule_code"] == "PPKI-LAY-008"]
    assert [item["status"] for item in left] == ["pass", "fail"]
    assert next(item for item in results if item["rule_code"] == "PPKI-LAY-005")["status"] == "needs_review"
    assert summarize(results)["diperiksa"] == 5


def test_unknown_applicability_and_unsupported():
    rules = load_rules()
    result = audit_docx(make_doc(), rules, "S2")
    unknown = next(rule for rule in rules if rule["applies_to"] == "Skripsi FKH")
    assert next(item for item in result if item["rule_code"] == unknown["rule_code"])["status"] == "needs_review"
    assert next(item for item in result if item["rule_code"] == "PPKI-LAY-017")["status"] == "needs_review"
    assert next(item for item in result if item["rule_code"] == "PPKI-LAY-019")["status"] == "needs_review"


def test_corrupt_docx():
    with pytest.raises(ValueError, match="DOCX tidak dapat dibuka"):
        audit_docx(b"invalid", load_rules(), "S1")


def test_changed_snapshot_mapping_is_not_used():
    rules = load_rules()
    next(rule for rule in rules if rule["rule_code"] == "PPKI-LAY-008")["expected_value_pattern"] = "5 cm"
    item = next(item for item in audit_docx(make_doc(), rules, "S1") if item["rule_code"] == "PPKI-LAY-008")
    assert item["status"] == "not_supported"


def font_audit(document):
    stream = BytesIO()
    document.save(stream)
    data = stream.getvalue()
    items = [item for item in audit_docx(data, load_rules(), "S1") if item["rule_code"] == "PPKI-LAY-005"]
    assert stream.getvalue() == data
    return items


@pytest.mark.parametrize("name,size,expected", [
    ("Times New Roman", 12, "Times New Roman / 12 pt"),
    ("Arial", 12, "Arial / 12 pt"),
    ("Times New Roman", 11, "Times New Roman / 11 pt"),
    (None, None, "tidak diketahui / ukuran tidak diketahui"),
])
def test_font_declarations_remain_review_when_context_uncertain(name, size, expected):
    doc = Document()
    paragraph = doc.add_paragraph(style="Body Text")
    run = paragraph.add_run("Teks sintetis")
    if name is not None:
        run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    item = font_audit(doc)[0]
    assert item["actual"] == expected
    assert item["status"] == "needs_review"
    assert item["location"] == "paragraf:1"
    assert item["expected"] == "Times New Roman 12 pt"
    assert item["severity"] == "Error" and item["pdf_page"] == 161


def test_font_style_inheritance_and_direct_override():
    doc = Document()
    base = doc.styles["Body Text"]
    base.font.name = "Times New Roman"
    base.font.size = Pt(12)
    doc.styles["Body Text 2"].base_style = base
    paragraph = doc.add_paragraph(style="Body Text 2")
    # Inspect inheritance independently; the derived style is not treated as a body candidate.
    from core.audit import declared_font
    run = paragraph.add_run("Teks sintetis")
    assert declared_font(run, paragraph) == ("Times New Roman", 12)
    run.font.size = Pt(11)
    assert declared_font(run, paragraph) == ("Times New Roman", 11)
    paragraph.style = base
    assert font_audit(doc)[0]["actual"] == "Times New Roman / 11 pt"


def test_special_styles_and_summary_do_not_claim_pass():
    doc = Document()
    doc.add_heading("Judul", 1)
    doc.add_paragraph("Caption", style="Caption")
    doc.add_paragraph("Isi kandidat", style="Body Text")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Isi tabel"
    items = font_audit(doc)
    assert len(items) == 3
    assert all(item["status"] == "needs_review" for item in items)
    assert items[0]["actual"] == items[1]["actual"] == "Tidak diperiksa"
    assert summarize(items)["perlu_review"] == 1
    assert summarize(items)["diperiksa"] == 1


@pytest.mark.parametrize("name,size,confirmed,status", [
    ("Times New Roman", 12, True, "pass"),
    ("Arial", 12, True, "fail"),
    ("Times New Roman", 11, True, "fail"),
    (None, None, True, "needs_review"),
    ("Times New Roman", 12, False, "needs_review"),
])
def test_confirmed_font_audit(name, size, confirmed, status):
    doc = Document()
    run = doc.add_paragraph(style="Body Text").add_run("Synthetic text")
    if name:
        run.font.name = name
    if size:
        run.font.size = Pt(size)
    data = BytesIO()
    doc.save(data)
    findings = audit_docx(data.getvalue(), load_rules(), "S1", "BodyText", confirmed)
    item = next(f for f in findings if f["rule_code"] == "PPKI-LAY-005")
    assert item["status"] == status
    assert item["location"] == "paragraf:1"
    assert item["severity"] == "Error" and item["source_section"]


def test_confirmed_inherited_font_and_fail_over_review():
    doc = Document()
    style = doc.styles["Body Text"]
    style.font.name, style.font.size = "Times New Roman", Pt(12)
    doc.add_paragraph("Inherited text", style=style)
    bad = doc.add_paragraph(style=style).add_run("Wrong")
    bad.font.name = "Arial"
    doc.add_paragraph("é", style=style)
    stream = BytesIO()
    doc.save(stream)
    findings = audit_docx(stream.getvalue(), load_rules(), "S1", "BodyText", True)
    items = [f for f in findings if f["rule_code"] == "PPKI-LAY-005"]
    assert [f["status"] for f in items] == ["pass", "fail", "needs_review"]
    assert summarize(items)["tidak_sesuai"] == 1


def test_theme_font_requires_review():
    from docx.oxml.ns import qn
    doc = Document()
    run = doc.add_paragraph(style="Body Text").add_run("Text")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run._r.rPr.rFonts.set(qn("w:asciiTheme"), "majorHAnsi")
    stream = BytesIO()
    doc.save(stream)
    item = next(f for f in audit_docx(stream.getvalue(), load_rules(), "S1", "BodyText", True) if f["rule_code"] == "PPKI-LAY-005")
    assert item["status"] == "needs_review"


@pytest.mark.parametrize("code,attribute,good,bad", [
    ("PPKI-LAY-017", "line_spacing", 1.0, 1.5),
    ("PPKI-LAY-018", "first_line_indent", Cm(1), Cm(2)),
    ("PPKI-LAY-019", "alignment", WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.LEFT),
])
def test_paragraph_properties_and_dry_run(code, attribute, good, bad):
    doc = Document()
    one = doc.add_paragraph("Isi satu", style="Body Text")
    two = doc.add_paragraph("Isi dua", style="Body Text")
    doc.add_heading("Judul", 1)
    setattr(one.paragraph_format, attribute, good)
    setattr(two.paragraph_format, attribute, bad)
    stream = BytesIO()
    doc.save(stream)
    data = stream.getvalue()
    items = [f for f in audit_docx(data, load_rules(), "S1", "BodyText", True) if f["rule_code"] == code]
    assert [f["status"] for f in items] == ["pass", "fail"]
    assert items[1]["location"] == "paragraf:2"
    assert items[1]["expected"] and items[1]["severity"] == "Error" and items[1]["source_section"]
    assert "belum diterapkan" in items[1]["proposed_change"]
    assert summarize(items)["tidak_sesuai"] == 1
    assert stream.getvalue() == data


@pytest.mark.parametrize("code,attribute,value", [
    ("PPKI-LAY-017", "line_spacing", 1.0),
    ("PPKI-LAY-018", "first_line_indent", Cm(1)),
    ("PPKI-LAY-019", "alignment", WD_ALIGN_PARAGRAPH.JUSTIFY),
])
def test_paragraph_style_inheritance(code, attribute, value):
    doc = Document()
    base = doc.styles["Body Text"]
    derived = doc.styles.add_style("Test Derived Body", WD_STYLE_TYPE.PARAGRAPH)
    derived.base_style = base
    setattr(base.paragraph_format, attribute, value)
    doc.add_paragraph("Isi", style=derived)
    stream = BytesIO()
    doc.save(stream)
    item = next(f for f in audit_docx(stream.getvalue(), load_rules(), "S1", derived.style_id, True) if f["rule_code"] == code)
    assert item["status"] == "pass"


@pytest.mark.parametrize("code", ["PPKI-LAY-017", "PPKI-LAY-018", "PPKI-LAY-019"])
def test_paragraph_unknown_unconfirmed_or_outside_scope(code):
    doc = Document()
    doc.add_paragraph("Isi", style="Body Text")
    doc.add_heading("Judul", 1)
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Tabel"
    stream = BytesIO()
    doc.save(stream)
    for selected, confirmed in [("BodyText", True), ("BodyText", False), ("Other", True)]:
        items = [f for f in audit_docx(stream.getvalue(), load_rules(), "S1", selected, confirmed) if f["rule_code"] == code]
        assert len(items) == 1 and items[0]["status"] == "needs_review"
        assert "proposed_change" not in items[0]


def test_fixed_spacing_and_complex_paragraph_need_review():
    doc = Document()
    paragraph = doc.add_paragraph("Isi", style="Body Text")
    paragraph.paragraph_format.line_spacing = Pt(12)
    stream = BytesIO()
    doc.save(stream)
    item = next(f for f in audit_docx(stream.getvalue(), load_rules(), "S1", "BodyText", True) if f["rule_code"] == "PPKI-LAY-017")
    assert item["status"] == "needs_review"
