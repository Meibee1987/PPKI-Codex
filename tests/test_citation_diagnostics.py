from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
from streamlit.testing.v1 import AppTest

from core.audit import citation_diagnostics

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def make_document():
    doc = Document()
    doc.add_heading("Pendahuluan tahun 2021", 1)
    doc.add_paragraph("Rahman (2021); (Putri dan Sari 2022); (Rahman, 2021; Putri & Sari, 2022); Nugraha (2023).")
    doc.add_paragraph("Tahun 2021, (12 Mei 2021), (Mei 2021), (Tabel 2021), dan 1234.")
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_paragraph("Rahman A. 2021. Contoh.")
    doc.add_paragraph("Putri A, Sari M. 2022. Contoh.")
    doc.add_paragraph("Halim A. 2020. Belum dirujuk.")
    doc.add_heading("LAMPIRAN", 1)
    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def test_candidates_cross_reference_and_false_positives():
    result = citation_diagnostics(make_document())
    assert len(result["sitasi"]) == 5
    assert len(result["referensi"]) == 3
    rows = result["perbandingan"]
    assert sum(r["jenis"] == "sitasi" and r["status"] == "mungkin_cocok" for r in rows) == 4
    assert any("Nugraha" in r["teks"] and r["status"] == "kandidat_referensi_tidak_ditemukan" for r in rows)
    assert any("Halim" in r["teks"] and r["status"] == "kandidat_sitasi_tidak_ditemukan" for r in rows)
    assert all("Mei" not in r["teks"] and "Tabel" not in r["teks"] for r in rows)


def test_ambiguous_reference_continuation_and_missing_heading():
    doc = Document()
    doc.add_paragraph("Rahman (2021)")
    doc.add_heading("DAFTAR PUSTAKA", 1)
    doc.add_paragraph("Rahman A. 2021. Judul")
    doc.add_paragraph("lanjutan entri yang tidak jelas")
    stream = BytesIO(); doc.save(stream)
    rows = citation_diagnostics(stream.getvalue())["perbandingan"]
    assert all(row["status"] == "needs_review" for row in rows)
    doc = Document(); doc.add_paragraph("Rahman (2021)")
    stream = BytesIO(); doc.save(stream)
    result = citation_diagnostics(stream.getvalue())
    assert result["catatan"] and result["perbandingan"][0]["status"] == "needs_review"


def test_master_diagnostics_are_read_only_and_repeatable():
    data = MASTER.read_bytes()
    first = citation_diagnostics(data)
    assert first == citation_diagnostics(data)
    assert MASTER.read_bytes() == data
    assert len(first["sitasi"]) == 5 and len(first["referensi"]) == 4
    assert any("Nugraha" in r["teks"] and r["status"] == "needs_review" for r in first["perbandingan"])


def test_streamlit_displays_diagnostics_without_body_confirmation():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=20).run()
        assert app.selectbox[1].value is None
        app.button[0].click().run()
        assert not app.exception
        assert any("Audit Sitasi dan Daftar Pustaka" in s.value for s in app.subheader)
        assert any("Kandidat sitasi: 5" in s.value for s in app.markdown)
        assert any("pasangan" in frame.value.columns and "status" in frame.value.columns for frame in app.dataframe)
        findings = app.dataframe[1].value
        assert set(findings[findings.rule_code.str.startswith(("PPKI-CIT-", "PPKI-REF-"))].status) <= {"not_supported", "needs_review"}
        assert any("validator manual yang belum didukung: 65" in s.value for s in app.markdown)
