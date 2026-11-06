from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest
from docx import Document

from core.audit import audit_docx
from core.formatter import format_docx, plan_changes
from core.rules import load_rules


FIXTURES = Path(__file__).parent / "fixtures"
PAGE_CODES = {"PPKI-LAY-003", "PPKI-LAY-008", "PPKI-LAY-009", "PPKI-LAY-010", "PPKI-LAY-011"}


@pytest.mark.parametrize("filename,degree,expected_changes,expected_skips", [
    ("PPKI_T4B_01_Skripsi_S1_Dasar.docx", "S1", 5, 0),
    ("PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx", "S2", 4, 0),
    ("PPKI_T4B_03_Disertasi_S3_MultiSection.docx", "S3", 6, 5),
])
def test_representative_documents(filename, degree, expected_changes, expected_skips):
    path = FIXTURES / filename
    assert path.is_file(), f"Fixture tidak tersedia: {path}"
    data = path.read_bytes()
    digest = sha256(data).digest()
    rules = load_rules()
    before = audit_docx(data, rules, degree, None, False)
    plan = plan_changes(data, rules, degree, None, False)
    planned = {(item["rule_code"], item["location"]) for item in plan}
    skipped = [item for item in before if item["rule_code"] in PAGE_CODES and item["status"] in {"fail", "needs_review", "not_supported"} and (item["rule_code"], item["location"]) not in planned]
    result, after, changes = format_docx(data, rules, degree, None, False)
    assert len(changes) == expected_changes and len(skipped) == expected_skips
    status = {(item["rule_code"], item["location"]): item["status"] for item in after}
    assert all(status[(item["rule_code"], item["location"])] == "pass" for item in changes)
    original, output = Document(BytesIO(data)), Document(BytesIO(result))
    assert [p.text for p in original.paragraphs] == [p.text for p in output.paragraphs]
    assert len(original.tables) == len(output.tables)
    assert len(original.inline_shapes) == len(output.inline_shapes)
    with ZipFile(BytesIO(data)) as old, ZipFile(BytesIO(result)) as new:
        assert all(old.read(name) == new.read(name) for name in old.namelist() if name != "word/document.xml")
        # Formatter verifies the full document XML apart from the approved properties.
        assert old.read("word/document.xml").count(b"<w:hyperlink") == new.read("word/document.xml").count(b"<w:hyperlink")
    if degree == "S3":
        assert original.sections[2]._sectPr.xml == output.sections[2]._sectPr.xml
        assert all(item["location"] == "section:3" for item in skipped)
    assert sha256(path.read_bytes()).digest() == digest
    second, _, more = format_docx(result, rules, degree, None, False)
    assert second == result and not more
