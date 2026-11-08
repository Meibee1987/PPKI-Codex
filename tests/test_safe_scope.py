from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from streamlit.testing.v1 import AppTest

from core.rules import load_rules
from core.structure import safe_format_scope

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def sample():
    doc = Document()
    doc.add_paragraph("SAMPUL DOKUMEN", style="Normal")
    doc.add_heading("BAB I PENDAHULUAN", 1)
    body = doc.add_paragraph(style="Body Text")
    run = body.add_run("This synthetic paragraph contains sufficient ordinary words for a simple body formatting audit without any private research data.")
    run.font.name = "Arial"; run.font.size = Pt(11)
    body.paragraph_format.line_spacing = 2.0
    body.paragraph_format.first_line_indent = Cm(0)
    body.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.add_heading("1.1 Subbab", 2)
    doc.add_paragraph("Tabel 1 Judul", style="Caption")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Sel tabel"
    complex_p = doc.add_paragraph("A sample paragraph containing a field which must stay protected.", style="Body Text")
    complex_p._p.append(OxmlElement("w:fldSimple"))
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_paragraph("Rujukan sintetis.", style="Body Text")
    doc.add_paragraph("")
    stream = BytesIO(); doc.save(stream)
    return stream.getvalue()


def test_scope_is_read_only_and_rule_specific():
    data = sample(); rules = load_rules()
    rows = safe_format_scope(data, rules, "S1")
    assert rows == safe_format_scope(data, rules, "S1")
    byloc = {row["lokasi"]: row for row in rows}
    assert byloc["paragraf:1"]["keputusan"] != "auto_safe"
    assert byloc["paragraf:2"]["keputusan"] == "protected"
    assert byloc["paragraf:3"]["keputusan"] == "auto_safe"
    assert set(byloc["paragraf:3"]["aturan_berubah"]) == {"PPKI-LAY-005", "PPKI-LAY-017", "PPKI-LAY-018", "PPKI-LAY-019"}
    assert byloc["paragraf:4"]["keputusan"] == "protected"
    assert byloc["paragraf:5"]["keputusan"] == "protected"
    assert byloc["tabel:1/baris:1/kolom:1/paragraf:1"]["keputusan"] == "protected"
    assert byloc["paragraf:6"]["keputusan"] == "protected"
    assert byloc["paragraf:8"]["keputusan"] == "protected"
    assert byloc["paragraf:9"]["keputusan"] == "protected"
    assert all("teks" not in row for row in rows)


def test_unknown_properties_are_not_authorized():
    doc = Document(BytesIO(sample()))
    body = doc.paragraphs[2]
    body.runs[0].font.name = None
    body.runs[0].font.size = None
    stream = BytesIO(); doc.save(stream)
    row = next(r for r in safe_format_scope(stream.getvalue(), load_rules(), "S1") if r["lokasi"] == "paragraf:3")
    assert "PPKI-LAY-005" not in row["aturan_diizinkan"]
    assert "PPKI-LAY-017" in row["aturan_diizinkan"]


def test_only_auto_rules_are_proposed_and_matching_values_do_not_change():
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2].paragraph_format.line_spacing = 1.0
    data = BytesIO(); doc.save(data)
    rules = load_rules()
    next(r for r in rules if r["rule_code"] == "PPKI-LAY-018")["fix_mode"] = "Manual"
    row = next(r for r in safe_format_scope(data.getvalue(), rules, "S1") if r["lokasi"] == "paragraf:3")
    assert "PPKI-LAY-018" not in row["aturan_diizinkan"]
    assert "PPKI-LAY-017" in row["aturan_diizinkan"]
    assert "PPKI-LAY-017" not in row["aturan_berubah"]
    manual = next(c for c in row["rule_decisions"] if c["rule_code"] == "PPKI-LAY-018")
    assert manual["eligible"] and manual["needs_change"] and not manual["safe_to_apply"]


def test_bookmarks_and_proofing_are_analysis_only_not_risky_objects():
    doc = Document(BytesIO(sample()))
    p = doc.paragraphs[2]
    for tag in ("bookmarkStart", "proofErr", "bookmarkEnd"):
        node = OxmlElement("w:" + tag)
        if tag.startswith("bookmark"):
            node.set(qn("w:id"), "1")
        p._p.append(node)
    original_xml = p._p.xml
    stream = BytesIO(); doc.save(stream); data = stream.getvalue()
    rows = safe_format_scope(data, load_rules(), "S1")
    row = next(r for r in rows if r["lokasi"] == "paragraf:3")
    assert row["keputusan"] == "auto_safe"
    assert all(c["eligible"] and c["needs_change"] and c["safe_to_apply"] for c in row["rule_decisions"])
    assert p._p.xml == original_xml
    assert Document(BytesIO(data)).paragraphs[2]._p.xml == original_xml


def test_normal_in_ambiguous_chapter_is_eligible_but_not_authorized():
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2].style = "Normal"
    doc.paragraphs[1].add_run()._r.append(OxmlElement("w:drawing"))
    # Preserve the real thesis pattern: a page boundary before a decorated heading.
    from docx.enum.text import WD_BREAK
    doc.paragraphs[1].insert_paragraph_before().add_run().add_break(WD_BREAK.PAGE)
    stream = BytesIO(); doc.save(stream)
    rows = safe_format_scope(stream.getvalue(), load_rules(), "S1")
    candidates = [r for r in rows if any(c["eligible"] for c in r["rule_decisions"])]
    assert len(candidates) == 1
    row = candidates[0]
    assert row["keputusan"] == "needs_review"
    assert all(c["eligible"] and c["needs_change"] and c["technical_safe"] and not c["safe_to_apply"] for c in row["rule_decisions"])


def test_already_compliant_is_still_safe_per_rule():
    doc = Document(BytesIO(sample()))
    p = doc.paragraphs[2]
    p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(12)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Cm(1)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    stream = BytesIO(); doc.save(stream)
    row = safe_format_scope(stream.getvalue(), load_rules(), "S1")[2]
    assert row["keputusan"] == "auto_safe" and not row["aturan_berubah"]
    assert all(c["eligible"] and c["needs_change"] is False and c["safe_to_apply"] for c in row["rule_decisions"])


def test_unicode_and_short_text_do_not_block_paragraph_properties():
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2].runs[0].text = "Kalimat sintetis dengan kafe café."
    stream = BytesIO(); doc.save(stream)
    checks = {c["rule_code"]: c for c in safe_format_scope(stream.getvalue(), load_rules(), "S1")[2]["rule_decisions"]}
    assert checks["PPKI-LAY-005"]["eligible"] and checks["PPKI-LAY-005"]["needs_change"] is None
    assert not checks["PPKI-LAY-005"]["safe_to_apply"]
    assert checks["PPKI-LAY-017"]["safe_to_apply"]


def test_caption_does_not_destroy_chapter_but_never_becomes_body():
    doc = Document(BytesIO(sample()))
    # A second candidate after the caption: keep chapter evidence across special objects.
    following = doc.paragraphs[5].insert_paragraph_before(doc.paragraphs[2].text, style="Body Text")
    following.paragraph_format.line_spacing = 2.0
    stream = BytesIO(); doc.save(stream)
    rows = safe_format_scope(stream.getvalue(), load_rules(), "S1")
    caption = next(r for r in rows if r["jenis"] == "caption_tabel")
    assert caption["keputusan"] == "protected"
    assert any(r["keputusan"] == "auto_safe" for r in rows if r["lokasi"].startswith("paragraf:") and int(r["lokasi"].split(':')[1]) > int(caption["lokasi"].split(':')[1]))


def test_unknown_xml_requires_review_and_fields_remain_protected():
    doc = Document(BytesIO(sample()))
    doc.paragraphs[2]._p.append(OxmlElement("w:customXml"))
    stream = BytesIO(); doc.save(stream)
    rows = safe_format_scope(stream.getvalue(), load_rules(), "S1")
    assert rows[2]["keputusan"] == "needs_review"
    assert all(not c["eligible"] for c in rows[2]["rule_decisions"])
    field = next(r for r in rows if r["lokasi"] == "paragraf:6")
    assert field["keputusan"] == "protected" and all(not c["safe_to_apply"] for c in field["rule_decisions"])


def test_streamlit_shows_dry_run_without_changing_existing_plan():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        app.button[0].click().run()
        assert not app.exception
        assert any("Pratinjau cakupan eksperimental" in row.value for row in app.markdown)
        assert not app.session_state["audit_t4a"]["confirmed"]
        assert MASTER.read_bytes() == data
