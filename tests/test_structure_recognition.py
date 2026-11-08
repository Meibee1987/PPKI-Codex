from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
from docx.enum.text import WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from streamlit.testing.v1 import AppTest

from core.structure import recognize_structure

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def synthetic_document():
    doc = Document()
    doc.add_paragraph("Nama penulis pada sampul", style="Normal")
    doc.add_heading("DAFTAR ISI", level=1)
    doc.add_paragraph("I PENDAHULUAN\t1", style="Normal")
    p = doc.add_heading("I PENDAHULUAN", level=1)
    p.paragraph_format.page_break_before = True
    doc.add_paragraph("Kandidat isi di dalam BAB.", style="Normal")
    doc.add_heading("1.1 Latar Belakang", level=2)
    doc.add_heading("4.2.1 Data Produksi", level=3)
    doc.add_paragraph("Gambar 1 Diagram", style="Caption")
    doc.add_paragraph("Tabel 1 Data", style="Caption")
    doc.add_paragraph("Satu butir", style="List Bullet")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Isi tabel"
    doc.add_heading("DAFTAR PUSTAKA", level=1)
    doc.add_paragraph("Rahman A. 2021. Referensi.")
    doc.add_heading("LAMPIRAN A", level=1)
    doc.add_paragraph("Isi lampiran")
    result = BytesIO(); doc.save(result)
    return result.getvalue()


def test_classification_is_read_only_and_context_aware():
    data = synthetic_document()
    first = recognize_structure(data)
    assert first == recognize_structure(data)
    rows = {row["teks"]: row for row in first}
    assert rows["Nama penulis pada sampul"]["jenis"] == "khusus"
    assert rows["I PENDAHULUAN\t1"]["jenis"] != "bab"
    assert rows["I PENDAHULUAN"]["jenis"] == "bab"
    assert rows["1.1 Latar Belakang"]["jenis"] == "subbab"
    assert rows["4.2.1 Data Produksi"]["jenis"] == "sub_subbab"
    assert rows["Kandidat isi di dalam BAB."]["jenis"] == "teks_isi"
    assert rows["Kandidat isi di dalam BAB."]["status"] == "needs_review"
    assert rows["Gambar 1 Diagram"]["jenis"] == "caption_gambar"
    assert rows["Tabel 1 Data"]["jenis"] == "caption_tabel"
    assert rows["Isi tabel"]["jenis"] == "paragraf_tabel"
    assert rows["Satu butir"]["jenis"] == "daftar"
    assert rows["Rahman A. 2021. Referensi."]["jenis"] == "entri_referensi"
    assert rows["Isi lampiran"]["jenis"] == "lampiran"


def test_roman_normal_is_review_and_toc_is_not_a_chapter():
    doc = Document()
    doc.add_paragraph("II TINJAUAN PUSTAKA")
    doc.add_paragraph("Paragraf isi")
    doc.add_heading("BAB III HASIL", 1)
    data = BytesIO(); doc.save(data)
    rows = recognize_structure(data.getvalue())
    assert rows[0]["jenis"] == "bab" and rows[0]["status"] == "needs_review"
    assert rows[2]["jenis"] == "bab" and rows[2]["status"] == "detected"


def test_heading_with_drawing_after_separate_page_break_needs_review():
    doc = Document()
    doc.add_heading("DAFTAR ISI", 1)
    doc.add_paragraph("I BAGIAN AWAL\t1")
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    heading = doc.add_heading("I BAGIAN AWAL", 1)
    heading.add_run()._r.append(OxmlElement("w:drawing"))
    doc.add_heading("1.1 Bagian", 2)
    doc.add_paragraph("Paragraf contoh.")
    data = BytesIO(); doc.save(data)
    rows = recognize_structure(data.getvalue())
    assert rows[1]["jenis"] == "entri_daftar"
    assert rows[2]["jenis"] == "bab" and rows[2]["status"] == "needs_review"
    assert rows[3]["jenis"] == "subbab" and rows[3]["status"] == "needs_review"
    assert rows[4]["jenis"] == "teks_isi" and rows[4]["status"] == "needs_review"


def test_bibliography_heading_style_with_drawing_is_candidate():
    doc = Document()
    doc.add_heading("LAMPIRAN A", 1)
    doc.styles.add_style("Heading", WD_STYLE_TYPE.PARAGRAPH)
    heading = doc.add_paragraph("DAFTAR PUSTAKA", style="Heading")
    heading.add_run()._r.append(OxmlElement("w:drawing"))
    doc.add_paragraph("Sumber A. 2020. Contoh.")
    data = BytesIO(); doc.save(data)
    rows = recognize_structure(data.getvalue())
    assert rows[1]["jenis"] == "daftar_pustaka" and rows[1]["status"] == "needs_review"
    assert rows[2]["jenis"] == "entri_referensi" and rows[2]["status"] == "needs_review"


def test_master_stays_unchanged_and_streamlit_shows_diagnostic():
    data = MASTER.read_bytes()
    rows = recognize_structure(data)
    assert MASTER.read_bytes() == data and rows == recognize_structure(data)
    assert [r["lokasi"] for r in rows if r["jenis"] == "bab"] == ["paragraf:40", "paragraf:60", "paragraf:75"]
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        app.button[0].click().run()
        assert not app.exception
        assert any("Pengenalan struktur (kandidat)" in s.value for s in app.markdown)
        assert app.selectbox[1].value is None
