from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import pytest
from streamlit.testing.v1 import AppTest

from core.audit import validate_docx_input

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
MASTER = FIX / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"
S1 = FIX / "PPKI_T4B_01_Skripsi_S1_Dasar.docx"


def package(extra=(), count=0):
    stream = BytesIO()
    with ZipFile(stream, "w", ZIP_DEFLATED) as archive:
        for name in ("[Content_Types].xml", "_rels/.rels", "word/document.xml"):
            archive.writestr(name, "<x/>")
        for name, data in extra:
            archive.writestr(name, data)
        for i in range(count):
            archive.writestr(f"extra/{i}", "x")
    return stream.getvalue()


@pytest.mark.parametrize("data,name,reason", [
    (b"", "empty.docx", "kosong"),
    (b"not a zip", "broken.docx", "tidak valid"),
    (b"bad", "wrong.pdf", "ekstensi"),
    (package()[:50], "truncated.docx", "tidak valid"),
    (package([( "../evil", b"x")]), "path.docx", "tidak aman"),
    (package([( "word/vbaProject.bin", b"x")]), "macro.docx", "macro"),
    (package([( "word/activeX/a.xml", b"x")]), "active.docx", "ActiveX"),
    (package([( "huge", b"0" * 2_000_000)]), "bomb.docx", "kompresi"),
    (package(count=2000), "entries.docx", "banyak entri"),
])
def test_invalid_upload(data, name, reason):
    with pytest.raises(ValueError, match=reason):
        validate_docx_input(data, name)


def test_duplicates_missing_invalid_xml_and_size():
    with pytest.warns(UserWarning):
        duplicate = package([("word/document.xml", b"<x/>")])
    for data, match in [(duplicate, "duplikat"), (b"PK\x05\x06" + bytes(18), "tidak lengkap"), (package([( "word/other", b"x")]), "batas")]:
        with pytest.raises(ValueError, match=match):
            validate_docx_input(data, "test.docx", max_bytes=10 if match == "batas" else 20 * 1024 * 1024)
    invalid = BytesIO()
    with ZipFile(invalid, "w") as archive:
        for name in ("[Content_Types].xml", "_rels/.rels", "word/document.xml"):
            archive.writestr(name, "<broken")
    with pytest.raises(ValueError, match="tidak valid"):
        validate_docx_input(invalid.getvalue(), "test.docx")


def test_encrypted_flag_rejected():
    data = bytearray(package())
    offset = data.find(b"PK\x01\x02")
    data[offset + 8] |= 1
    with pytest.raises(ValueError, match="terenkripsi"):
        validate_docx_input(bytes(data), "encrypted.docx")


def test_uncompressed_total_and_symlink_rejected():
    huge = ZipInfo("large")
    huge.file_size = 201 * 1024 * 1024
    with patch.object(ZipFile, "infolist", return_value=[huge]):
        with pytest.raises(ValueError, match="dekompresi"):
            validate_docx_input(package(), "test.docx")
    stream = BytesIO()
    with ZipFile(stream, "w") as archive:
        entry = ZipInfo("link")
        entry.create_system = 3
        entry.external_attr = 0o120777 << 16
        archive.writestr(entry, "target")
    with pytest.raises(ValueError, match="symbolic link"):
        validate_docx_input(stream.getvalue(), "test.docx")


def test_streamlit_invalid_and_changing_input_clears_old_download():
    current = {"file": SimpleNamespace(name=S1.name, getvalue=lambda: S1.read_bytes())}
    with patch("streamlit.file_uploader", side_effect=lambda *args, **kwargs: current["file"]):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        app.button[0].click().run()
        next(b for b in app.button if b.label == "Terapkan Perbaikan Otomatis").click().run()
        assert len(app.get("download_button")) == 2
        current["file"] = SimpleNamespace(name="bad.docx", getvalue=lambda: b"not a docx")
        app.run()
        assert not app.exception and app.error and not app.get("download_button")
        assert app.session_state.get("audit_t4a") is None
        app.button[0].click().run()
        assert not app.exception and not app.get("download_button")
        current["file"] = SimpleNamespace(name=MASTER.name, getvalue=lambda: MASTER.read_bytes())
        app.run()
        assert not app.exception and not app.get("download_button")
        assert app.selectbox[1].value is None
        assert not any(c.value for c in app.checkbox)
        app.selectbox[0].select("S2").run()
        assert not app.exception and not app.get("download_button")
        app.button[0].click().run()
        assert app.session_state["audit_t4a"]["degree"] == "S2"


def test_confirmation_scope_and_failed_validation_clears_output():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        app.selectbox[1].select("BodyText").run()
        app.checkbox[0].check()
        app.checkbox[2].check()
        app.checkbox[4].check()
        app.button[0].click().run()
        assert app.session_state["audit_t4a"]["confirmed"]
        assert app.session_state["audit_t4a"]["heading_confirmed"] == {60}
        next(b for b in app.button if b.label == "Terapkan Perbaikan Otomatis").click().run()
        assert len(app.get("download_button")) == 2
        with patch("core.formatter.format_docx", side_effect=ValueError("Validasi integritas gagal")):
            next(b for b in app.button if b.label == "Terapkan Perbaikan Otomatis").click().run()
            assert app.error and not app.get("download_button") and not app.exception
        app.selectbox[0].select("S3").run()
        assert not any(c.value for c in app.checkbox)
        assert app.session_state.get("audit_t4a") is None
