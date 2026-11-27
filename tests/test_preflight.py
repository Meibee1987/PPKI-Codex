from hashlib import sha256
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from streamlit.testing.v1 import AppTest

from core.formatter import candidate_changes, format_docx, format_margins, plan_changes
from core.preflight import image_preflight
from core.rules import load_rules
from scripts.t13_fixtures import synthetic_png

ROOT = Path(__file__).resolve().parent.parent
S2 = ROOT / "tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx"


def saved(document):
    stream = BytesIO()
    document.save(stream)
    return stream.getvalue()


def sample(width=14.2, context="body"):
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.left_margin, section.right_margin = Cm(2), Cm(2)
    section.top_margin, section.bottom_margin = Cm(2), Cm(2)
    if context == "table":
        paragraph = document.add_table(rows=1, cols=1).cell(0, 0).paragraphs[0]
    elif context == "header":
        paragraph = section.header.paragraphs[0]
    else:
        paragraph = document.add_paragraph()
    if width is not None:
        paragraph.add_run().add_picture(BytesIO(synthetic_png()), width=Cm(width))
    return document


def planned(data):
    return candidate_changes(data, load_rules(), "S2", None, False)


@pytest.mark.parametrize("width,status,overflow", [(14.2, "NEEDS_REVIEW", True), (13.9, "PASS", False)])
def test_planned_margin_width_and_readonly_repeated(width, status, overflow, tmp_path):
    path = tmp_path / "input.docx"
    path.write_bytes(saved(sample(width)))
    data = path.read_bytes(); digest = sha256(data).hexdigest()
    plan = planned(data)
    report = image_preflight(data, plan)
    assert report == image_preflight(data, plan)
    assert report["status"] == status
    row = report["images"][0]
    assert row["section"] == 1 and row["location"] == "paragraf:1"
    assert row["image_width_cm"] == pytest.approx(width, abs=0.001)
    assert row["text_width_before_cm"] == pytest.approx(17, abs=0.002)
    assert row["text_width_after_cm"] == pytest.approx(14, abs=0.002)
    assert row["difference_cm"] == pytest.approx(width - 14, abs=0.002)
    assert row["potential_width_overflow"] is overflow
    assert sha256(path.read_bytes()).hexdigest() == digest
    assert image_preflight(data)["status"] == "PASS"  # current 17cm field, no invented correction


def test_no_images_is_not_applicable():
    report = image_preflight(saved(sample(None)))
    assert report["status"] == "NOT_APPLICABLE"
    assert report["images_checked"] == report["images_needing_review"] == 0
    assert not report["images"] and not report["review_sections"]


@pytest.mark.parametrize("special", ["gutter", "mirror", "columns", "continuous", "table", "anchor", "header", "indent", "mixed", "chars", "missing_extent", "legacy", "rotation"])
def test_ambiguous_context_never_claims_safe_width(special):
    document = sample(1, "table" if special == "table" else "header" if special == "header" else "body")
    section = document.sections[0]
    paragraph = document.paragraphs[0] if document.paragraphs else None
    if special == "gutter": section.gutter = Cm(1)
    elif special == "mirror": document.settings.element.append(OxmlElement("w:mirrorMargins"))
    elif special == "columns": section._sectPr.find(qn("w:cols")).set(qn("w:num"), "2")
    elif special == "continuous": section.start_type = 0
    elif special == "anchor": document.inline_shapes[0]._inline.tag = qn("wp:anchor")
    elif special == "indent": paragraph.paragraph_format.first_line_indent = Cm(1)
    elif special == "mixed": paragraph.add_run("text before image")
    elif special == "chars":
        ind = OxmlElement("w:ind"); ind.set(qn("w:leftChars"), "100"); paragraph._p.get_or_add_pPr().append(ind)
    elif special == "missing_extent":
        obj = document.inline_shapes[0]._inline; obj.remove(obj.find(qn("wp:extent")))
    elif special == "rotation":
        next(document.inline_shapes[0]._inline.iter(qn("a:xfrm"))).set("rot", "5400000")
    elif special == "legacy":
        obj = document.inline_shapes[0]._inline; obj.getparent().remove(obj); paragraph.add_run()._r.append(OxmlElement("w:pict"))
    data = saved(document)
    report = image_preflight(data, planned(data))
    assert report["status"] == "NEEDS_REVIEW"
    assert report["images_checked"] == report["images_needing_review"] == 1
    assert report["images"][0]["reason"]
    assert report["images"][0]["available_width_cm"] is None
    assert report["images"][0]["potential_width_overflow"] is None


def test_positive_indents_reduce_available_width_and_negative_needs_review():
    doc = sample(13.9)
    doc.paragraphs[0].paragraph_format.left_indent = Cm(1)
    data = saved(doc); row = image_preflight(data, planned(data))["images"][0]
    assert row["available_width_cm"] == pytest.approx(13, abs=0.002)
    assert row["potential_width_overflow"]
    doc.paragraphs[0].paragraph_format.left_indent = Cm(-1)
    data = saved(doc)
    assert image_preflight(data, planned(data))["status"] == "NEEDS_REVIEW"


def test_section_break_mapping_and_only_risky_section_is_held():
    doc = sample(14.2)
    doc.add_section()
    doc.add_paragraph().add_run().add_picture(BytesIO(synthetic_png()), width=Cm(1))
    data = saved(doc); report = image_preflight(data, planned(data))
    assert [r["section"] for r in report["images"]] == [1, 2]
    assert report["review_sections"] == [1]
    plan = plan_changes(data, load_rules(), "S2", None, False)
    assert not any(r["location"] == "section:1" and r["rule_code"] in {"PPKI-LAY-008", "PPKI-LAY-009"} for r in plan)
    assert any(r["location"] == "section:2" and r["rule_code"] == "PPKI-LAY-008" for r in plan)
    assert any(r["location"] == "section:1" and r["rule_code"] == "PPKI-LAY-010" for r in plan)


def test_guard_default_and_explicit_review_preserve_package_and_images():
    data = S2.read_bytes(); rules = load_rules()
    output, report = format_margins(data, rules, "S2")
    assert {r["rule_code"] for r in report if r["status"] == "applied"} == {"PPKI-LAY-010", "PPKI-LAY-011"}
    assert all("PREFLIGHT" in r["alasan"] for r in report if r["status"] == "uncertain")
    reviewed, rows = format_margins(data, rules, "S2", image_reviewed_sections={1})
    assert len([r for r in rows if r["status"] == "applied"]) == 4
    assert image_preflight(reviewed)["status"] == "NEEDS_REVIEW"  # approval does not turn warning into PASS
    for result in (output, reviewed):
        with ZipFile(BytesIO(data)) as before, ZipFile(BytesIO(result)) as after:
            assert all(before.read(n) == after.read(n) for n in before.namelist() if n != "word/document.xml")
        assert Document(BytesIO(result)).inline_shapes[0].width == Document(BytesIO(data)).inline_shapes[0].width
    assert S2.read_bytes() == data
    general, _, operations = format_docx(data, rules, "S2", None, False)
    assert general == output
    assert {r["rule_code"] for r in operations} == {"PPKI-LAY-010", "PPKI-LAY-011"}


def test_s2_planned_geometry_matches_existing_margin_handler_output():
    data = S2.read_bytes()
    prediction = image_preflight(data, planned(data))["sections"][0]
    output, _ = format_margins(data, load_rules(), "S2", image_reviewed_sections={1})
    actual = image_preflight(output)["sections"][0]
    assert prediction["planned_cm"] == actual["current_cm"]


def test_streamlit_preflight_visible_review_and_no_paid_api():
    data = S2.read_bytes(); upload = SimpleNamespace(name="s2.docx", getvalue=lambda: data)
    with patch("streamlit.file_uploader", return_value=upload), patch("core.ai_beta.request_classifications") as ai:
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        assert not app.exception
        assert app.session_state["margin_preflight"]["images_needing_review"] == 1
        assert any("NEEDS_REVIEW" in item.value for item in app.warning)
        next(b for b in app.button if b.label == "Perbaiki margin deterministik").click().run()
        assert not app.exception and not app.error
        assert len([r for r in app.session_state["margin_result"]["rows"] if r["status"] == "applied"]) == 2
        review = next(c for c in app.checkbox if "risiko gambar section 1" in c.label and "rencana margin" in c.label)
        review.check().run()
        assert "margin_result" not in app.session_state
        next(b for b in app.button if b.label == "Perbaiki margin deterministik").click().run()
        assert len([r for r in app.session_state["margin_result"]["rows"] if r["status"] == "applied"]) == 4
        assert app.session_state["margin_preflight"]["status"] == "NEEDS_REVIEW"
        assert not ai.called and upload.getvalue() == data
        # A different document must not retain the old warning or consent.
        safe = saved(sample(13.9))
        with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="safe.docx", getvalue=lambda: safe)):
            app.run()
            assert app.session_state["margin_preflight"]["status"] == "PASS"
            assert "margin_result" not in app.session_state
            assert not any("risiko gambar section" in c.label for c in app.checkbox)


def test_streamlit_general_plan_review_is_independent_and_revocable():
    data = S2.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="s2.docx", getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        next(b for b in app.button if b.label == "Audit").click().run()
        assert len(app.session_state["audit_t4a"]["plan"]) == 2
        c = next(c for c in app.checkbox if "risiko gambar section 1" in c.label and "rencana umum" in c.label)
        c.check().run()
        assert len(app.session_state["audit_t4a"]["plan"]) == 4
        next(b for b in app.button if b.label == "Terapkan Perbaikan Otomatis").click().run()
        assert not app.exception and not app.error
        assert len(app.session_state["output_t4a"]["changes"]) == 4
        c = next(c for c in app.checkbox if "risiko gambar section 1" in c.label and "rencana umum" in c.label)
        c.uncheck().run()
        assert "output_t4a" not in app.session_state
        assert len(app.session_state["audit_t4a"]["plan"]) == 2


def test_explicit_image_review_cannot_bypass_gutter_guard():
    doc = sample(14.2)
    doc.sections[0].gutter = Cm(1)
    data = saved(doc)
    output, rows = format_margins(data, load_rules(), "S2", image_reviewed_sections={1})
    assert output == data
    assert not any(r["status"] == "applied" for r in rows)


def test_t14_validation_still_precedes_preflight():
    with pytest.raises(ValueError, match="DOCX"):
        image_preflight(b"not a docx")


def test_streamlit_review_does_not_transfer_to_other_document_with_same_geometry():
    document = sample(14.2)
    first = saved(document)
    document.core_properties.title = "Different test document, same geometry"
    second = saved(document)
    assert first != second
    assert image_preflight(first, planned(first)) == image_preflight(second, planned(second))
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="one.docx", getvalue=lambda: first)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        c = next(c for c in app.checkbox if "risiko gambar section 1" in c.label)
        c.check().run()
        assert next(c for c in app.checkbox if "risiko gambar section 1" in c.label).value
        with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="two.docx", getvalue=lambda: second)):
            app.run()
            assert not app.exception
            assert not next(c for c in app.checkbox if "risiko gambar section 1" in c.label).value
