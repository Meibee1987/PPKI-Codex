from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
from docx.oxml import OxmlElement
from docx.enum.style import WD_STYLE_TYPE
from streamlit.testing.v1 import AppTest

from core.audit import audit_docx, illustration_structure
from core.rules import load_rules


MASTER = Path(__file__).parent / "fixtures" / "PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx"


def test_master_tables_images_captions_and_unsupported_rules():
    data = MASTER.read_bytes()
    result = illustration_structure(data)
    assert len(result["tabel"]) == 3
    assert result["tabel"][0]["baris"] == 69  # satu header dan 68 baris data
    assert result["tabel"][0]["baris_header_berulang"] == "1"
    assert result["tabel"][1]["sel_gabungan"] == "Terdeteksi"
    assert result["tabel"][2]["section"] == 5
    assert str(Document(BytesIO(data)).sections[4].orientation).startswith("LANDSCAPE")
    assert len(result["gambar"]) == 2
    assert [item["jenis"] for item in result["caption"]].count("tabel") == 3
    assert [item["jenis"] for item in result["caption"]].count("gambar") == 2
    assert all(item["status"] == "needs_review" for group in result.values() for item in group)
    assert all("berdekatan" in item["dugaan_objek"] for item in result["caption"])
    assert result == illustration_structure(data)
    findings = audit_docx(data, load_rules(), "S1")
    relevant = {r["rule_code"] for r in load_rules() if r["domain"] in {"TBL", "FIG"}}
    assert len(relevant) == 66
    assert all(item["status"] == "not_supported" for item in findings if item["rule_code"] in relevant)
    assert MASTER.read_bytes() == data


def test_plain_paragraph_not_caption_and_floating_object_reported():
    doc = Document()
    doc.add_paragraph("Tabel 1 adalah data dalam narasi.", style="Normal")
    doc.add_paragraph("Tabel tidak sesuai karena merupakan catatan biasa.", style="Normal")
    doc.add_paragraph("Gambar 1 Contoh", style="Caption")
    paragraph = doc.add_paragraph("Objek")
    drawing = OxmlElement("w:drawing"); drawing.append(OxmlElement("wp:anchor"))
    paragraph.add_run()._r.append(drawing)
    stream = BytesIO(); doc.save(stream)
    result = illustration_structure(stream.getvalue())
    assert len(result["caption"]) == 1
    assert result["caption"][0]["dugaan_objek"] == "Tidak diketahui"
    assert len(result["objek_kompleks"]) == 1 and "mengambang" in result["objek_kompleks"][0]["jenis"]


def test_custom_caption_style_and_unconfirmed_relationship():
    doc = Document()
    doc.styles.add_style("Table Caption", WD_STYLE_TYPE.PARAGRAPH)
    doc.add_paragraph("Tabel tanpa nomor yang jelas", style="Table Caption")
    doc.add_table(rows=1, cols=1)
    stream = BytesIO(); doc.save(stream)
    caption = illustration_structure(stream.getvalue())["caption"][0]
    assert caption["style"] == "Table Caption" and caption["status"] == "needs_review"
    assert "belum pasti" in caption["dugaan_objek"]


def test_streamlit_master_counts_and_caption_confirmation():
    data = MASTER.read_bytes()
    with patch("streamlit.file_uploader", return_value=SimpleNamespace(name=MASTER.name, getvalue=lambda: data)):
        app = AppTest.from_file(Path(__file__).resolve().parent.parent / "app.py", default_timeout=20).run()
        caption = next(box for box in app.checkbox if box.label.startswith("paragraf:69:"))
        caption.check(); app.button[0].click().run()
        assert not app.exception
        assert any("Tabel: 3 | Gambar inline: 2 | Kandidat caption tabel: 3 | Kandidat caption gambar: 2" in x.value for x in app.markdown)
        frames = [frame.value for frame in app.dataframe]
        caption_frame = next(frame for frame in frames if "hubungan_dikonfirmasi" in frame.columns)
        assert bool(caption_frame[caption_frame["lokasi"] == "paragraf:69"].iloc[0]["hubungan_dikonfirmasi"])
        assert set(caption_frame["status"]) == {"needs_review"}
