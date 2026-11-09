import csv
import json
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pytest
from docx import Document
from streamlit.testing.v1 import AppTest

from core.operator_review import (
    RULE_CODES, evaluate_review, load_labels, load_review, paragraph_context, save_label,
)
from core.rules import load_rules


ROOT = Path(__file__).resolve().parent.parent


def make_review(folder):
    doc = Document()
    doc.add_heading("BAB I CONTOH", 1)
    doc.add_paragraph("Synthetic confidential text only for testing.", style="Body Text")
    doc.add_paragraph("Context after the selected paragraph.")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Synthetic table cell"
    stream = BytesIO(); doc.save(stream); data = stream.getvalue()
    (folder / "tesis_uji.docx").write_bytes(data)
    locations = ["paragraf:1", "paragraf:2", "paragraf:3", "tabel:1/baris:1/kolom:1/paragraf:1"]
    with (folder / "scope_operator_sample.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["lokasi", "suggested_type", "operator_role"])
        writer.writeheader()
        for location in locations:
            writer.writerow({"lokasi": location, "suggested_type": "teks_isi", "operator_role": ""})
    digest = sha256(data).hexdigest()
    (folder / "scope_operator_sample_meta.json").write_text(json.dumps({"source_sha256": digest, "rows": len(locations)}), encoding="utf-8")
    return data, digest, locations


def test_save_labels_is_document_bound_and_does_not_write_text(tmp_path):
    data, digest, locations = make_review(tmp_path)
    review = load_review(load_rules(), tmp_path)
    assert review["labels"] == {}
    assert paragraph_context(data, "paragraf:2")["teks"].startswith("Synthetic")
    assert paragraph_context(data, locations[3])["teks"] == "Synthetic table cell"
    safety = {code: "" for code in RULE_CODES}
    safety[RULE_CODES[0]] = "belum_yakin"
    safety[RULE_CODES[1]] = "aman"
    save_label(tmp_path, digest, set(locations), locations[1], "teks_isi", safety)
    loaded = load_labels(tmp_path, digest, set(locations))
    assert loaded[locations[1]][RULE_CODES[0]] == "belum_yakin"
    assert loaded[locations[1]][RULE_CODES[1]] == "aman"
    assert (tmp_path / "tesis_uji.docx").read_bytes() == data
    assert "Synthetic" not in (tmp_path / "scope_operator_labels.csv").read_text(encoding="utf-8")
    assert (tmp_path / "scope_operator_sample.csv").read_text(encoding="utf-8").count("teks_isi") == 4
    other = Document(); other.add_paragraph("A different document")
    stream = BytesIO(); other.save(stream)
    (tmp_path / "tesis_uji.docx").write_bytes(stream.getvalue())
    with pytest.raises(ValueError, match="berubah"):
        save_label(tmp_path, digest, set(locations), locations[2], "bab", {code: "" for code in RULE_CODES})
    with pytest.raises(ValueError, match="Hash"):
        load_review(load_rules(), tmp_path)


def test_existing_foreign_labels_and_modified_samples_are_rejected(tmp_path):
    data, digest, locations = make_review(tmp_path)
    save_label(tmp_path, digest, set(locations), locations[0], "bab", {code: "" for code in RULE_CODES})
    with pytest.raises(ValueError, match="dokumen lain"):
        load_labels(tmp_path, "0" * 64, set(locations))
    with (tmp_path / "scope_operator_sample.csv").open("a", encoding="utf-8") as f:
        f.write("paragraf:1,teks_isi,\n")
    with pytest.raises(ValueError, match="Sampel berubah"):
        save_label(tmp_path, digest, set(locations), locations[1], "teks_isi", {code: "" for code in RULE_CODES})
    assert (tmp_path / "tesis_uji.docx").read_bytes() == data


def test_blank_submission_remains_pending(tmp_path):
    _, digest, locations = make_review(tmp_path)
    save_label(tmp_path, digest, set(locations), locations[0], "", {code: "" for code in RULE_CODES})
    review = load_review(load_rules(), tmp_path)
    result = evaluate_review(review["locations"], review["recognized"], review["scope"], review["labels"])
    assert result["jenis_pending"] == 4 and result["aturan_pending"] == 16
    assert result["sampel_terukur"] == 0


def test_evaluation_excludes_pending_unsure_and_abstentions():
    locations = [f"paragraf:{i}" for i in range(1, 9)]
    recognized = {loc: {"jenis": "teks_isi" if i < 7 else "khusus"} for i, loc in enumerate(locations, 1)}
    scope = {loc: {"keputusan": "protected" if i == 6 else "needs_review", "rule_decisions": [{"rule_code": code, "safe_to_apply": False} for code in RULE_CODES]} for i, loc in enumerate(locations, 1)}
    labels = {loc: {"operator_role": "teks_isi", RULE_CODES[0]: "aman"} for loc in locations[:7]}
    labels[locations[7]] = {"operator_role": "belum_yakin", RULE_CODES[0]: "belum_yakin"}
    result = evaluate_review(locations, recognized, scope, labels)
    body = result["klasifikasi"][0]
    assert (body["tp"], body["fp"], body["fn"], body["prediksi_ambigu"]) == (6, 0, 1, 1)
    assert body["precision"] is None and body["recall"] is None
    assert result["jenis_pending"] == 1
    safety = result["keamanan"][0]
    assert safety["dilabeli"] == 7 and safety["prediksi_review"] == 6
    assert safety["operator_aman_prediksi_dilindungi"] == 1
    assert result["aturan_pending"] == 25


def test_metrics_require_positive_and_negative_labels():
    locations = [f"paragraf:{i}" for i in range(10)]
    recognized = {loc: {"jenis": "teks_isi" if i in (0, 1, 2, 3, 5) else "bab"} for i, loc in enumerate(locations)}
    scope = {loc: {"keputusan": "needs_review", "rule_decisions": [{"rule_code": code, "safe_to_apply": False} for code in RULE_CODES]} for loc in locations}
    labels = {loc: {"operator_role": "teks_isi" if i < 5 else "bab"} for i, loc in enumerate(locations)}
    body = evaluate_review(locations, recognized, scope, labels)["klasifikasi"][0]
    assert (body["tp"], body["fp"], body["fn"]) == (4, 1, 1)
    assert body["precision"] == .8 and body["recall"] == .8


def test_streamlit_private_review_opt_in_save_and_local_binding(tmp_path):
    data, digest, locations = make_review(tmp_path)
    with patch.dict("os.environ", {"PPKI_LOCAL_REVIEW": "1"}), patch("streamlit.get_option", return_value="localhost"), patch("core.operator_review.PRIVATE_DIR", tmp_path):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        next(c for c in app.checkbox if c.label == "Buka 40 sampel privat").check().run()
        assert not app.exception and not app.error
        next(s for s in app.selectbox if s.label == "Lokasi sampel").select(locations[1]).run()
        next(s for s in app.selectbox if s.label == "Jenis menurut operator").select("teks_isi")
        next(s for s in app.selectbox if s.label == RULE_CODES[0]).select("belum_yakin")
        next(b for b in app.button if b.label == "Simpan label lokal").click().run()
        assert not app.exception and not app.error
        assert load_labels(tmp_path, digest, set(locations))[locations[1]][RULE_CODES[0]] == "belum_yakin"
        assert (tmp_path / "tesis_uji.docx").read_bytes() == data
    with patch.dict("os.environ", {"PPKI_LOCAL_REVIEW": "1"}), patch("streamlit.get_option", return_value="0.0.0.0"), patch("core.operator_review.PRIVATE_DIR", tmp_path):
        app = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        assert any("localhost" in warning.value for warning in app.warning)
        assert not any(c.label == "Buka 40 sampel privat" for c in app.checkbox)
