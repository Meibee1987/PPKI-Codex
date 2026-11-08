from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from streamlit.testing.v1 import AppTest

from core.audit import audit_docx, page_number_structure
from core.rules import load_rules


def document_with_fields():
    doc = Document()
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:fmt"), "lowerRoman"); pg.set(qn("w:start"), "1")
    doc.sections[0]._sectPr.append(pg)
    footer = doc.sections[0].footer.paragraphs[0]
    field = OxmlElement("w:fldSimple"); field.set(qn("w:instr"), " PAGE ")
    footer._p.append(field)
    doc.add_section()
    second = doc.sections[1]._sectPr
    pg = second.find(qn("w:pgNumType"))
    if pg is not None:
        second.remove(pg)
    pg = OxmlElement("w:pgNumType"); pg.set(qn("w:fmt"), "decimal")
    second.append(pg)
    stream = BytesIO(); doc.save(stream)
    return stream.getvalue()


def test_explicit_format_restart_and_inherited_footer_are_review_only():
    data = document_with_fields()
    sections = page_number_structure(data)
    assert len(sections) == 2
    assert (sections[0]["format_nomor"], sections[0]["restart"]) == ("lowerRoman", "1")
    assert (sections[1]["format_nomor"], sections[1]["restart"]) == ("decimal", "Tidak eksplisit")
    assert "PAGE ditemukan" in sections[0]["field_PAGE"]
    assert "diwariskan" in sections[1]["field_PAGE"] and "PAGE ditemukan" in sections[1]["field_PAGE"]
    assert all(section["status"] == "needs_review" for section in sections)
    findings = audit_docx(data, load_rules(), "S1")
    for code in ("PPKI-LAY-023", "PPKI-LAY-024"):
        assert next(item for item in findings if item["rule_code"] == code)["status"] == "not_supported"


def test_numpages_is_not_page_field_and_missing_defaults_are_unknown():
    doc = Document()
    field = OxmlElement("w:fldSimple"); field.set(qn("w:instr"), " NUMPAGES ")
    doc.sections[0].footer.paragraphs[0]._p.append(field)
    other = OxmlElement("w:fldSimple"); other.set(qn("w:instr"), " IF PAGE = 1 ")
    doc.sections[0].footer.paragraphs[0]._p.append(other)
    stream = BytesIO(); doc.save(stream)
    result = page_number_structure(stream.getvalue())[0]
    assert result["format_nomor"] == result["restart"] == "Tidak eksplisit"
    assert "PAGE tidak terdeteksi" in result["field_PAGE"]
    assert result["status"] == "needs_review"


def test_invalid_input_fails_cleanly():
    with pytest.raises(ValueError, match="tidak dapat dibaca"):
        page_number_structure(b"invalid")


def test_dummy_master_read_only_and_unsupported():
    path = Path(__file__).parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
    data = path.read_bytes(); result = page_number_structure(data)
    assert len(result) == 6
    assert result[0]["format_nomor"] == "lowerRoman" and result[0]["restart"] == "1"
    assert result[1]["format_nomor"] == "decimal"
    assert all(item["status"] == "needs_review" for item in result)
    assert path.read_bytes() == data


def test_streamlit_shows_structural_diagnostic_and_unsupported():
    data = document_with_fields()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name="dummy.docx", getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=15).run()
        app.button[0].click().run()
        assert not app.exception
        findings = app.dataframe[1].value
        assert findings[findings["rule_code"] == "PPKI-LAY-023"].iloc[0]["status"] == "not_supported"
        structures = app.dataframe[2].value
        assert len(structures) == 2 and set(structures["status"]) == {"needs_review"}
