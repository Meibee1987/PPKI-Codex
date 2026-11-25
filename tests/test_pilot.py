from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from streamlit.testing.v1 import AppTest

from core.pilot import format_pilot, pilot_plan, pilot_summary
from core.rules import load_rules
from core.audit import certain_font


def sample():
    doc = Document()
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    ppr = defaults.find(qn("w:pPrDefault"))
    if ppr is not None:
        defaults.remove(ppr)
    doc.add_paragraph("Sampul sintetis", style="Normal")
    doc.add_heading("BAB I PENDAHULUAN", 1)
    p = doc.add_paragraph("Paragraf sintetis untuk pilot yang telah dikonfirmasi operator dan memiliki format yang perlu diperiksa.", style="Body Text")
    run = p.runs[0]; run.font.name = "Arial"; run.font.size = Pt(11); run.bold = True; run.italic = True
    p.paragraph_format.line_spacing = 2.0
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    other = doc.add_paragraph("Paragraf sintetis lain yang tidak dikonfirmasi dan tidak boleh diubah oleh pilot ini.", style="Body Text")
    other.paragraph_format.line_spacing = 2.0
    complex_p = doc.add_paragraph("Paragraf sintetis dengan field Word.", style="Body Text")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), " PAGE ")
    complex_p._p.append(field)
    doc.add_paragraph("Tabel 1 Caption sintetis", style="Caption")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Isi tabel sintetis"
    doc.sections[0].header.paragraphs[0].text = "Header sintetis"
    output = BytesIO(); doc.save(output)
    return output.getvalue()


def test_document_default_font_is_resolved_and_corrected_without_changing_defaults():
    doc = Document(BytesIO(sample()))
    run = doc.paragraphs[2].runs[0]
    run.font.name = None
    run.font.size = None
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    rpr = defaults.find(qn("w:rPrDefault")).find(qn("w:rPr"))
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is not None:
        rpr.remove(fonts)
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Arial")
    fonts.set(qn("w:hAnsi"), "Arial")
    rpr.insert(0, fonts)
    size = rpr.find(qn("w:sz"))
    if size is None:
        size = OxmlElement("w:sz"); rpr.append(size)
    size.set(qn("w:val"), "22")
    assert certain_font(run, doc.paragraphs[2]) == ("Arial", 11)
    stream = BytesIO(); doc.save(stream); original = stream.getvalue()
    result, plan = format_pilot(original, load_rules(), "S1", {3})
    font = next(r for r in plan if r["lokasi"] == "paragraf:3" and r["rule_code"] == "PPKI-LAY-005")
    assert font["eligible_for_normalization"] and font["nilai_awal"] == "known_noncompliant"
    after = Document(BytesIO(result))
    assert certain_font(after.paragraphs[2].runs[0], after.paragraphs[2]) == ("Times New Roman", 12)
    assert after.paragraphs[2].runs[0].bold and after.paragraphs[2].runs[0].italic
    with ZipFile(BytesIO(original)) as first, ZipFile(BytesIO(result)) as second:
        assert all(first.read(n) == second.read(n) for n in first.namelist() if n != "word/document.xml")
    again, _ = format_pilot(result, load_rules(), "S1", {3})
    assert again == result


def test_document_default_theme_does_not_override_explicit_uncertainty():
    doc = Document(BytesIO(sample()))
    run = doc.paragraphs[2].runs[0]
    run.font.name = None; run.font.size = None
    assert certain_font(run, doc.paragraphs[2])[0] is None


def test_direct_and_paragraph_style_take_precedence_over_document_defaults():
    doc = Document(BytesIO(sample()))
    paragraph = doc.paragraphs[2]
    run = paragraph.runs[0]
    paragraph.style.font.name = "Courier New"
    paragraph.style.font.size = Pt(10)
    assert certain_font(run, paragraph) == ("Arial", 11)
    run.font.name = None; run.font.size = None
    assert certain_font(run, paragraph) == ("Courier New", 10)


def test_character_style_inheritance_precedes_paragraph_style():
    from docx.enum.style import WD_STYLE_TYPE
    doc = Document(BytesIO(sample()))
    paragraph = doc.paragraphs[2]; run = paragraph.runs[0]
    paragraph.style.font.name = "Arial"; paragraph.style.font.size = Pt(11)
    base = doc.styles.add_style("Synthetic Character Base", WD_STYLE_TYPE.CHARACTER)
    base.font.name = "Times New Roman"; base.font.size = Pt(12)
    derived = doc.styles.add_style("Synthetic Character Derived", WD_STYLE_TYPE.CHARACTER)
    derived.base_style = base
    run.font.name = None; run.font.size = None; run.style = derived
    assert certain_font(run, paragraph) == ("Times New Roman", 12)


def test_incomplete_default_font_remains_unknown():
    doc = Document(BytesIO(sample()))
    paragraph = doc.paragraphs[2]; run = paragraph.runs[0]
    run.font.name = None; run.font.size = None
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    rpr = defaults.find(qn("w:rPrDefault")).find(qn("w:rPr"))
    fonts = rpr.find(qn("w:rFonts"))
    rpr.remove(fonts)
    fonts = OxmlElement("w:rFonts"); fonts.set(qn("w:ascii"), "Arial"); rpr.insert(0, fonts)
    assert certain_font(run, paragraph)[0] is None


def test_pilot_changes_only_confirmed_paragraph_and_normalizes_unknown():
    data = sample(); rules = load_rules()
    plan = pilot_plan(data, rules, "S1", {3})
    selected = {r["rule_code"]: r for r in plan if r["lokasi"] == "paragraf:3"}
    assert selected["PPKI-LAY-005"]["nilai_awal"] == "known_noncompliant"
    assert selected["PPKI-LAY-018"]["nilai_awal"] == "unknown_value"
    assert selected["PPKI-LAY-018"]["eligible_for_normalization"]
    result, plan = format_pilot(data, rules, "S1", {3})
    assert result != data and pilot_summary(plan)["unknown_to_normalize"] >= 1
    before = Document(BytesIO(data)); after = Document(BytesIO(result))
    assert [p.text for p in before.paragraphs] == [p.text for p in after.paragraphs]
    assert after.paragraphs[2].runs[0].bold and after.paragraphs[2].runs[0].italic
    assert after.paragraphs[2].runs[0].font.name == "Times New Roman"
    assert after.paragraphs[2].runs[0].font.size.pt == 12
    assert after.paragraphs[2].paragraph_format.line_spacing == 1.0
    assert abs(after.paragraphs[2].paragraph_format.first_line_indent.cm - 1) < .02
    assert after.paragraphs[2].alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
    assert before.paragraphs[3]._p.xml == after.paragraphs[3]._p.xml
    assert before.paragraphs[4]._p.xml == after.paragraphs[4]._p.xml
    with ZipFile(BytesIO(data)) as first, ZipFile(BytesIO(result)) as second:
        assert all(first.read(name) == second.read(name) for name in first.namelist() if name != "word/document.xml")
    again, second_plan = format_pilot(result, rules, "S1", {3})
    assert again == result and pilot_summary(second_plan)["planned"] == 0


def test_pilot_requires_confirmation_and_does_not_treat_unknown_as_failure():
    data = sample(); rules = load_rules()
    result, plan = format_pilot(data, rules, "S1", set())
    assert result == data and pilot_summary(plan)["planned"] == 0
    assert any(row["nilai_awal"] == "unknown_value" and not row["eligible_for_normalization"] for row in plan)
    assert any("belum dikonfirmasi" in row["alasan"] for row in plan)


def test_selected_heading_is_explicitly_rejected():
    data = sample()
    result, plan = format_pilot(data, load_rules(), "S1", {2})
    assert result == data
    rows = [row for row in plan if row["lokasi"] == "paragraf:2"]
    assert len(rows) == 4 and all(row["unsafe_or_ambiguous"] for row in rows)


def test_manual_confirm_and_unsafe_font_are_skipped():
    data = sample(); rules = load_rules()
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-017")["fix_mode"] = "Manual"
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-018")["fix_mode"] = "Confirm"
    doc = Document(BytesIO(data)); doc.paragraphs[2].runs[0].font.name = None
    output = BytesIO(); doc.save(output)
    plan = pilot_plan(output.getvalue(), rules, "S1", {3})
    for row in plan:
        if row["lokasi"] == "paragraf:3" and row["rule_code"] in {"PPKI-LAY-005", "PPKI-LAY-017", "PPKI-LAY-018"}:
            assert not row["eligible_for_normalization"] and row["unsafe_or_ambiguous"]


def test_integrity_failure_never_returns_a_file(monkeypatch):
    from core import pilot
    monkeypatch.setattr(pilot, "_document_structure", lambda xml, changes: xml)
    with pytest.raises(ValueError, match="struktur"):
        format_pilot(sample(), load_rules(), "S1", {3})


def test_bookmarks_are_preserved_during_pilot_reaudit():
    doc = Document(BytesIO(sample()))
    for tag in ("bookmarkStart", "bookmarkEnd"):
        node = OxmlElement("w:" + tag)
        node.set(qn("w:id"), "7")
        doc.paragraphs[2]._p.append(node)
    stream = BytesIO(); doc.save(stream)
    result, plan = format_pilot(stream.getvalue(), load_rules(), "S1", {3})
    p = Document(BytesIO(result)).paragraphs[2]
    assert p._p.xpath('./w:bookmarkStart') and p._p.xpath('./w:bookmarkEnd')
    assert any(row["rule_code"] == "PPKI-LAY-017" and row["eligible_for_normalization"] for row in plan)


def test_superscript_subscript_and_symbol_font_are_preserved():
    doc = Document(BytesIO(sample()))
    p = doc.paragraphs[2]
    p.runs[0].font.superscript = True
    symbol = p.add_run(" x")
    symbol.font.name = "Symbol"; symbol.font.size = Pt(11); symbol.font.subscript = True
    stream = BytesIO(); doc.save(stream)
    result, plan = format_pilot(stream.getvalue(), load_rules(), "S1", {3})
    after = Document(BytesIO(result)).paragraphs[2]
    assert after.runs[0].font.superscript and after.runs[1].font.subscript
    assert after.runs[1].font.name == "Symbol" and after.runs[0].font.name == "Arial"
    font = next(row for row in plan if row["lokasi"] == "paragraf:3" and row["rule_code"] == "PPKI-LAY-005")
    assert not font["eligible_for_normalization"]


@pytest.mark.parametrize("tag", ["w:hyperlink", "w:fldSimple", "w:footnoteReference", "w:drawing", "w:ins"])
def test_complex_paragraphs_never_receive_pilot_changes(tag):
    doc = Document(BytesIO(sample()))
    p = doc.paragraphs[2]
    if tag in {"w:footnoteReference", "w:drawing"}:
        p.runs[0]._r.append(OxmlElement(tag))
    else:
        p._p.append(OxmlElement(tag))
    stream = BytesIO(); doc.save(stream)
    result, plan = format_pilot(stream.getvalue(), load_rules(), "S1", {3})
    assert result == stream.getvalue()
    assert all(not row["eligible_for_normalization"] for row in plan)


def test_landscape_section_is_not_formatted():
    doc = Document(BytesIO(sample()))
    doc.sections[0].orientation = WD_ORIENT.LANDSCAPE
    stream = BytesIO(); doc.save(stream)
    result, plan = format_pilot(stream.getvalue(), load_rules(), "S1", {3})
    assert result == stream.getvalue()
    assert all(not row["eligible_for_normalization"] for row in plan)


@pytest.mark.parametrize("boundary", ["columns", "section_break"])
def test_columns_and_section_boundaries_are_not_formatted(boundary):
    doc = Document(BytesIO(sample()))
    if boundary == "columns":
        doc.sections[0]._sectPr.find(qn("w:cols")).set(qn("w:num"), "2")
    else:
        doc.paragraphs[2]._p.get_or_add_pPr().append(OxmlElement("w:sectPr"))
    stream = BytesIO(); doc.save(stream)
    result, plan = format_pilot(stream.getvalue(), load_rules(), "S1", {3})
    assert result == stream.getvalue()
    assert all(not row["eligible_for_normalization"] for row in plan)


def test_streamlit_pilot_requires_explicit_selection_and_downloads_validated_copy():
    data = sample(); upload = SimpleNamespace(name="dummy.docx", getvalue=lambda: data)
    with patch("streamlit.file_uploader", return_value=upload):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(c for c in app.checkbox if c.label == "Aktifkan pilot lokal").check().run()
        app.multiselect[0].set_value([3]).run()
        next(c for c in app.checkbox if c.label.startswith("Saya memastikan paragraf terpilih")).check().run()
        next(b for b in app.button if b.label == "Buat rencana pilot").click().run()
        assert not app.exception and app.session_state.get("pilot_plan")
        next(b for b in app.button if b.label == "Terapkan pilot pada salinan").click().run()
        assert not app.exception and len(app.get("download_button")) == 1
        assert app.session_state["pilot_result"] != data and upload.getvalue() == data
        with patch("core.pilot.format_pilot", side_effect=ValueError("Validasi gagal")):
            next(b for b in app.button if b.label == "Terapkan pilot pada salinan").click().run()
            assert not app.exception and app.error and not app.get("download_button")
            assert app.session_state.get("pilot_result") is None
