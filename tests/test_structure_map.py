from io import BytesIO
import pytest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from streamlit.testing.v1 import AppTest

from core.ai_planner import prepare_analysis, validate_plan
from core.rules import load_rules
from core.structure import document_structure_map, safe_format_scope


def fixture():
    doc = Document()
    toc = doc.styles.add_style("TOC 1", WD_STYLE_TYPE.PARAGRAPH)
    doc.add_heading("DAFTAR ISI", 1)
    for name in ("I PENDAHULUAN", "II KAJIAN", "III METODE"):
        doc.add_paragraph(name, style=toc)
    body_locations = []
    for number, name in enumerate(("I PENDAHULUAN", "II KAJIAN", "III METODE")):
        if number == 2:
            doc.add_section(WD_SECTION.NEW_PAGE)
        else:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        heading = doc.add_heading(name, 1)
        heading.add_run()._r.append(OxmlElement("w:drawing"))
        p = doc.add_paragraph("Ini adalah paragraf sintetis yang panjang untuk menguji konteks BAB, bagian dokumen, dan format tanpa data pribadi.", style="Normal")
        p.paragraph_format.line_spacing = 2.0
        body_locations.append(len(doc.paragraphs))
    doc.add_paragraph("Tabel 1 Keterangan sintetis", style="Caption")
    table = doc.add_table(rows=1, cols=1)
    table.cell(0, 0).text = "Isi tabel sintetis"
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_paragraph("Entri sintetis.")
    output = BytesIO(); doc.save(output)
    return output.getvalue(), body_locations


def test_map_handles_roman_drawings_pagebreak_toc_and_sections():
    data, locations = fixture()
    mapping = document_structure_map(data)
    assert [c["number"] for c in mapping["chapters"]] == [1, 2, 3]
    assert all(c["boundary_status"] == "detected" for c in mapping["chapters"])
    assert len(mapping["sections"]) == 2 and mapping["section_known"]
    assert [next(e for e in mapping["elements"] if e["lokasi"] == f"paragraf:{i}")["chapter"] for i in locations] == [1, 2, 3]
    assert any(item["jenis"] == "paragraf_tabel" and item["section"] == 2 for item in mapping["elements"])
    assert mapping["caption_relations"] and mapping["caption_relations"][0]["status"] == "needs_review"
    assert document_structure_map(data) == mapping


def test_multi_section_body_candidate_but_section_boundary_is_protected():
    data, locations = fixture()
    prepared = prepare_analysis(data, load_rules(), "S1")
    rule = prepared["rules"]["PPKI-LAY-017"]
    proposal = {"paragraph_id": f"paragraf:{locations[2]}", "element_type": "body", "rule_code": rule["rule_code"], "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "body_context"}
    result = validate_plan({"proposals": [proposal]}, prepared)
    assert result[0]["status"] == "kandidat_pratinjau"
    rows = safe_format_scope(data, load_rules(), "S1", use_structure_map=True)
    doc = Document(BytesIO(data))
    index = next(i for i, p in enumerate(doc.paragraphs, 1) if p._p.pPr is not None and p._p.pPr.find(qn("w:sectPr")) is not None)
    boundary = rows[index - 1]
    assert boundary["keputusan"] == "protected" and not boundary["ai_section_safe"]


def test_landscape_and_field_objects_cannot_use_ai_evidence():
    data, locations = fixture()
    doc = Document(BytesIO(data))
    doc.sections[1].orientation = WD_ORIENT.LANDSCAPE
    p = doc.paragraphs[locations[2] - 1]
    p._p.append(OxmlElement("w:fldSimple"))
    output = BytesIO(); doc.save(output)
    rows = safe_format_scope(output.getvalue(), load_rules(), "S1", use_structure_map=True)
    row = rows[locations[2] - 1]
    assert row["keputusan"] == "protected" and not row["ai_section_safe"]


@pytest.mark.parametrize("setting", ["landscape", "columns"])
def test_individual_unsafe_sections_block_plain_paragraph(setting):
    data, locations = fixture()
    doc = Document(BytesIO(data))
    if setting == "landscape":
        doc.sections[1].orientation = WD_ORIENT.LANDSCAPE
    else:
        columns = doc.sections[1]._sectPr.find(qn("w:cols"))
        columns.set(qn("w:num"), "2")
    output = BytesIO(); doc.save(output)
    prepared = prepare_analysis(output.getvalue(), load_rules(), "S1")
    rule = prepared["rules"]["PPKI-LAY-017"]
    proposal = {"paragraph_id": f"paragraf:{locations[2]}", "element_type": "body", "rule_code": rule["rule_code"], "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "body_context"}
    outcome = validate_plan({"proposals": [proposal]}, prepared)[0]
    assert outcome["status"] == "needs_review" and "Section" in outcome["alasan"]


def test_mapped_section_already_correct_is_not_a_change():
    data, locations = fixture()
    doc = Document(BytesIO(data))
    doc.paragraphs[locations[2] - 1].paragraph_format.line_spacing = 1.0
    output = BytesIO(); doc.save(output)
    prepared = prepare_analysis(output.getvalue(), load_rules(), "S1")
    rule = prepared["rules"]["PPKI-LAY-017"]
    proposal = {"paragraph_id": f"paragraf:{locations[2]}", "element_type": "body", "rule_code": rule["rule_code"], "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "body_context"}
    result = validate_plan({"proposals": [proposal]}, prepared)[0]
    assert result["status"] == "sudah_sesuai" and result["tindakan"] == "tidak_perlu_perubahan"


def test_toc_only_does_not_establish_chapters():
    doc = Document()
    doc.add_heading("DAFTAR ISI", 1)
    toc = doc.styles.add_style("TOC 1", WD_STYLE_TYPE.PARAGRAPH)
    for text in ("I PENDAHULUAN", "II KAJIAN", "III METODE"):
        doc.add_paragraph(text, style=toc)
    output = BytesIO(); doc.save(output)
    assert not document_structure_map(output.getvalue())["chapters"]


def test_repeated_chapter_heading_toc_cannot_authorize_boundaries():
    doc = Document()
    doc.add_heading("DAFTAR ISI", 1)
    toc = doc.styles.add_style("TOC 1", WD_STYLE_TYPE.PARAGRAPH)
    for _ in range(2):
        for title in ("I PENDAHULUAN", "II KAJIAN", "III METODE"):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            doc.add_heading(title, 1)
            doc.add_paragraph("1.1 Entri daftar isi", style=toc)
    output = BytesIO(); doc.save(output)
    chapters = document_structure_map(output.getvalue())["chapters"]
    assert chapters and all(c["boundary_status"] == "needs_review" for c in chapters)


def test_incorrect_ai_and_ambiguous_body_are_rejected():
    data, locations = fixture()
    prepared = prepare_analysis(data, load_rules(), "S1")
    rule = prepared["rules"]["PPKI-LAY-017"]
    proposal = {"paragraph_id": f"paragraf:{locations[0]}", "element_type": "uncertain", "rule_code": rule["rule_code"], "action": "line_spacing", "target": rule["expected_value_pattern"], "reason": "ambiguous"}
    assert validate_plan({"proposals": [proposal]}, prepared)[0]["status"] == "needs_review"


@pytest.mark.parametrize("tag", ["w:hyperlink", "w:fldSimple", "w:drawing", "w:footnoteReference", "w:ins"])
def test_complex_paragraphs_remain_protected(tag):
    data, locations = fixture()
    doc = Document(BytesIO(data))
    paragraph = doc.paragraphs[locations[1] - 1]
    if tag in ("w:drawing", "w:footnoteReference"):
        paragraph.runs[0]._r.append(OxmlElement(tag))
    else:
        paragraph._p.append(OxmlElement(tag))
    output = BytesIO(); doc.save(output)
    row = safe_format_scope(output.getvalue(), load_rules(), "S1", use_structure_map=True)[locations[1] - 1]
    assert row["keputusan"] == "protected" and not row["ai_supported_identity"]


def test_streamlit_shows_structure_map_without_formatting():
    data, _ = fixture()
    upload = SimpleNamespace(name="synthetic.docx", getvalue=lambda: data)
    with patch("streamlit.file_uploader", return_value=upload):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=30).run()
        next(button for button in app.button if button.label == "Audit").click().run()
        assert not app.exception
        assert any(expander.label == "Peta kandidat BAB dan section" for expander in app.expander)
        assert upload.getvalue() == data
