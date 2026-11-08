"""Local-only operator labels; never modifies the DOCX or formatter scope."""
import csv
import json
import os
import tempfile
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from docx import Document

from core.audit import validate_docx_input
from core.structure import recognize_structure, safe_format_scope


PRIVATE_DIR = Path(__file__).resolve().parent.parent / "private_tests"
RULE_CODES = ("PPKI-LAY-005", "PPKI-LAY-017", "PPKI-LAY-018", "PPKI-LAY-019")
ROLES = ("teks_isi", "bab", "subbab", "caption", "bagian_khusus", "daftar_pustaka", "lainnya", "belum_yakin")
SAFETY = ("aman", "tidak_aman", "belum_yakin")
FIELDS = ("document_sha256", "lokasi", "operator_role", *RULE_CODES)


def load_review(rules, private_dir=PRIVATE_DIR, max_bytes=20 * 1024 * 1024):
    """Load a fixed local sample, checking that it belongs to the exact DOCX."""
    folder = Path(private_dir)
    try:
        data = (folder / "tesis_uji.docx").read_bytes()
        validate_docx_input(data, "tesis_uji.docx", max_bytes)
        digest = sha256(data).hexdigest()
        metadata = json.loads((folder / "scope_operator_sample_meta.json").read_text(encoding="utf-8"))
        with (folder / "scope_operator_sample.csv").open(encoding="utf-8-sig", newline="") as source:
            samples = list(csv.DictReader(source))
        if metadata.get("source_sha256") != digest or metadata.get("rows") != len(samples):
            raise ValueError("Hash dokumen atau jumlah sampel tidak sesuai metadata; review dibatalkan.")
        locations = [row.get("lokasi", "") for row in samples]
        if not locations or len(locations) != len(set(locations)):
            raise ValueError("Lokasi sampel kosong atau duplikat.")
        recognized = {row["lokasi"]: row for row in recognize_structure(data)}
        scope = {row["lokasi"]: row for row in safe_format_scope(data, rules, "S2")}
        if any(location not in scope for location in locations):
            raise ValueError("Lokasi sampel tidak ditemukan pada dokumen ini.")
        labels = load_labels(folder, digest, set(locations))
        return {"data": data, "digest": digest, "locations": locations,
                "recognized": recognized, "scope": scope, "labels": labels}
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error, KeyError, TypeError) as exc:
        raise ValueError("File review privat tidak tersedia atau formatnya tidak valid.") from exc


def load_labels(folder, digest, locations):
    path = Path(folder) / "scope_operator_labels.csv"
    if path.is_symlink():
        raise ValueError("File label berupa symbolic link tidak didukung.")
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("Kolom file label tidak valid; file tidak diubah.")
        labels = {}
        for row in reader:
            location = row.get("lokasi")
            if row.get("document_sha256") != digest or location not in locations or location in labels:
                raise ValueError("Label berasal dari dokumen lain, lokasi tidak dikenal, atau duplikat.")
            if row.get("operator_role") not in ("", *ROLES) or any(row.get(code) not in ("", *SAFETY) for code in RULE_CODES):
                raise ValueError("Nilai label tidak dikenal; file tidak diubah.")
            labels[location] = row
        return labels


def save_label(folder, digest, locations, location, role, safety):
    """Merge one explicit label; refuse stale or foreign documents."""
    folder = Path(folder)
    if location not in locations or role not in ("", *ROLES) or set(safety) != set(RULE_CODES) or any(value not in ("", *SAFETY) for value in safety.values()):
        raise ValueError("Label atau lokasi tidak valid.")
    try:
        if sha256((folder / "tesis_uji.docx").read_bytes()).hexdigest() != digest:
            raise ValueError("Dokumen berubah sejak sampel dimuat; label tidak disimpan.")
        metadata = json.loads((folder / "scope_operator_sample_meta.json").read_text(encoding="utf-8"))
        with (folder / "scope_operator_sample.csv").open(encoding="utf-8-sig", newline="") as source:
            current_locations = [row.get("lokasi", "") for row in csv.DictReader(source)]
        if metadata.get("source_sha256") != digest or metadata.get("rows") != len(current_locations) or len(current_locations) != len(set(current_locations)) or set(current_locations) != set(locations):
            raise ValueError("Sampel berubah sejak dimuat; label tidak disimpan.")
        labels = load_labels(folder, digest, set(locations))
        labels[location] = {"document_sha256": digest, "lokasi": location, "operator_role": role, **safety}
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=folder, prefix=".labels_", suffix=".tmp", delete=False) as target:
                temp_path = Path(target.name)
                writer = csv.DictWriter(target, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(labels[key] for key in current_locations if key in labels)
            os.replace(temp_path, folder / "scope_operator_labels.csv")
        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        raise ValueError("Label gagal disimpan; periksa file privat dan izin direktori.") from exc


def paragraph_context(data, location):
    """Return local display text and neighbors, without writing or logging them."""
    doc = Document(BytesIO(data))
    parts = location.split("/")
    try:
        if len(parts) == 1 and parts[0].startswith("paragraf:"):
            paragraphs = doc.paragraphs
            index = int(parts[0].split(":")[1]) - 1
        elif len(parts) == 4 and [p.split(":")[0] for p in parts] == ["tabel", "baris", "kolom", "paragraf"]:
            table, row, column, index = (int(p.split(":")[1]) - 1 for p in parts)
            if min(table, row, column, index) < 0:
                raise IndexError
            paragraphs = doc.tables[table].rows[row].cells[column].paragraphs
        else:
            raise ValueError
        if index < 0 or index >= len(paragraphs):
            raise IndexError
        return {"sebelum": paragraphs[index - 1].text if index else "", "teks": paragraphs[index].text,
                "sesudah": paragraphs[index + 1].text if index + 1 < len(paragraphs) else ""}
    except (IndexError, ValueError) as exc:
        raise ValueError("Lokasi sampel tidak dapat dibaca.") from exc


def predicted_role(kind):
    if kind in ("teks_isi", "bab"):
        return kind
    if kind in ("subbab", "sub_subbab"):
        return "subbab"
    if kind in ("caption_tabel", "caption_gambar"):
        return "caption"
    if kind in ("daftar_pustaka", "entri_referensi"):
        return "daftar_pustaka"
    if kind in {"khusus", "kosong"}:
        return None
    return "bagian_khusus"


def evaluate_review(locations, recognized, scope, labels):
    """Compare only explicit labels; unsure and empty labels are never negatives."""
    categories = ROLES[:6]
    comparisons = []
    for location in locations:
        role = labels.get(location, {}).get("operator_role", "")
        if role in categories:
            comparisons.append((role, predicted_role(recognized.get(location, {}).get("jenis", "kosong"))))
    classification = []
    for category in categories:
        tp = sum(truth == category and pred == category for truth, pred in comparisons)
        fp = sum(truth != category and pred == category for truth, pred in comparisons)
        fn = sum(truth == category and pred != category for truth, pred in comparisons)
        abstained = sum(truth == category and pred is None for truth, pred in comparisons)
        # A small, selectively labeled sample is not representative of the document.
        enough = tp + fn >= 5
        classification.append({"kategori": category, "dilabeli_positif": tp + fn, "tp": tp, "fp": fp, "fn": fn, "prediksi_ambigu": abstained,
                               "precision": round(tp / (tp + fp), 3) if enough and tp + fp else None,
                               "recall": round(tp / (tp + fn), 3) if enough else None})
    safety_rows = []
    for code in RULE_CODES:
        labeled = []
        for location in locations:
            label = labels.get(location, {}).get(code, "")
            if label in ("aman", "tidak_aman"):
                check = next(c for c in scope[location]["rule_decisions"] if c["rule_code"] == code)
                prediction = True if check["safe_to_apply"] else False if scope[location]["keputusan"] == "protected" else None
                labeled.append((label == "aman", prediction))
        safety_rows.append({"rule_code": code, "dilabeli": len(labeled),
                            "operator_tidak_aman_prediksi_aman": sum(not truth and pred is True for truth, pred in labeled),
                            "operator_aman_prediksi_dilindungi": sum(truth and pred is False for truth, pred in labeled),
                            "prediksi_review": sum(pred is None for _, pred in labeled),
                            "sepakat": sum(pred is not None and truth == pred for truth, pred in labeled)})
    roles_pending = sum(labels.get(location, {}).get("operator_role", "") in ("", "lainnya", "belum_yakin") for location in locations)
    safety_pending = sum(labels.get(location, {}).get(code, "") in ("", "belum_yakin") for location in locations for code in RULE_CODES)
    return {"klasifikasi": classification, "keamanan": safety_rows, "jenis_pending": roles_pending, "aturan_pending": safety_pending,
            "sampel_terukur": len(comparisons)}
