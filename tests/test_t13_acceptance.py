from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from docx import Document
from streamlit.testing.v1 import AppTest

from core.audit import audit_docx, summarize
from core.formatter import format_docx
from core.rules import load_rules


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"


@pytest.mark.parametrize("filename,degree", [
    ("PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx", "S1"),
    ("PPKI_T4B_01_Skripsi_S1_Dasar.docx", "S1"),
    ("PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx", "S2"),
    ("PPKI_T4B_03_Disertasi_S3_MultiSection.docx", "S3"),
])
def test_acceptance_ui_and_integrity(filename, degree):
    path = FIXTURES / filename
    data, rules = path.read_bytes(), load_rules()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=filename, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        app.selectbox[0].select(degree).run()
        app.button[0].click().run()
        assert not app.exception
        snapshot = app.session_state["audit_t4a"]
        assert snapshot["before"] == summarize(audit_docx(data, rules, degree))
        assert snapshot["plan"]
        assert all(item.get("alasan_dilewati") for item in snapshot["skipped"])
        next(button for button in app.button if button.label == "Terapkan Perbaikan Otomatis").click().run()
        assert not app.exception
        assert not app.error
        assert len(app.get("download_button")) == 2
        result = app.session_state["output_t4a"]
        assert len(result["changes"]) == len(snapshot["plan"])
        assert all(item["status"] == "pass" for item in result["report"])
        output = result["data"]
        assert result["after"] == summarize(audit_docx(output, rules, degree))
    original, formatted = Document(BytesIO(data)), Document(BytesIO(output))
    assert [p.text for p in original.paragraphs] == [p.text for p in formatted.paragraphs]
    assert [t._tbl.xml for t in original.tables] == [t._tbl.xml for t in formatted.tables]
    with ZipFile(BytesIO(data)) as old, ZipFile(BytesIO(output)) as new:
        assert set(old.namelist()) == set(new.namelist())
        assert all(old.read(name) == new.read(name) for name in old.namelist() if name != "word/document.xml")
    second, _, changes = format_docx(output, rules, degree, None, False)
    assert second == output and not changes
    assert path.read_bytes() == data
