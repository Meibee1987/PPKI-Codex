from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
from streamlit.testing.v1 import AppTest

from core.audit import document_structure

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def test_master_order_and_source_unchanged():
    original = MASTER.read_bytes()
    result = document_structure(original)
    assert result == document_structure(original)
    assert MASTER.read_bytes() == original
    rows = result["bagian"]
    assert [(r["lokasi"], r["bagian_kandidat"]) for r in rows if r["bagian_kandidat"] == "BAB"] == [("paragraf:40", "BAB"), ("paragraf:60", "BAB"), ("paragraf:75", "BAB")]
    assert any(r["lokasi"] == "paragraf:11" and r["bagian_kandidat"] == "Pernyataan" for r in rows)
    assert any(r["lokasi"] == "paragraf:97" and r["bagian_kandidat"] == "Daftar pustaka" for r in rows)
    assert [r["lokasi"] for r in rows if r["bagian_kandidat"] == "Lampiran"] == ["paragraf:90", "paragraf:103"]
    assert all(r["status"] == "needs_review" for r in rows)
    assert [r["urutan"] for r in rows] == list(range(1, len(rows) + 1))


def test_candidates_require_heading_and_missing_not_proof():
    doc = Document()
    doc.add_paragraph("DAFTAR PUSTAKA")
    doc.add_heading("ABSTRAK", 1)
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_heading("BAB I PENDAHULUAN", 1)
    doc.add_heading("LAMPIRAN", 1)
    doc.add_heading("ABSTRAK", 1)
    data = BytesIO(); doc.save(data)
    result = document_structure(data.getvalue())
    rows = result["bagian"]
    assert [r["bagian_kandidat"] for r in rows] == ["Abstrak", "Daftar pustaka", "BAB", "Lampiran", "Abstrak"]
    assert rows[1]["lokasi"] == "paragraf:3"
    assert "Pernyataan" in result["tanpa_kandidat"]
    assert all(r["status"] == "needs_review" for r in rows)


def test_streamlit_degrees_and_no_body_confirmation():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=20).run()
        assert app.selectbox[1].value is None
        for degree in ("S1", "S2", "S3"):
            app.selectbox[0].select(degree).run()
            app.button[0].click().run()
            assert not app.exception
            assert any("Audit Struktur Dokumen" in s.value for s in app.subheader)
            tables = [frame.value for frame in app.dataframe if "bagian_kandidat" in frame.value.columns]
            assert len(tables) == 1 and (tables[0].status == "needs_review").all()
            inventories = [frame.value for frame in app.dataframe if "status_validator" in frame.value.columns]
            assert len(inventories) == 1
            assert (inventories[0].status_validator == "not_supported").all()
            assert "PPKI-STR-001" in set(inventories[0].rule_code)
            assert ("PPKI-STR-017" in set(inventories[0].rule_code)) == (degree in ("S2", "S3"))
