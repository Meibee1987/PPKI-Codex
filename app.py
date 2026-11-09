import streamlit as st
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import csv
import logging
import os
from io import StringIO

from core.rules import filter_rules, load_rules
from core.audit import audit_docx, summarize, font_candidates, heading_candidates, page_number_structure, illustration_structure, citation_diagnostics, document_structure, validate_docx_input
from core.formatter import format_docx, plan_changes, skipped_changes
from core.structure import recognize_structure, safe_format_scope
import core.operator_review as operator_review


st.set_page_config(page_title="PPKI Academic Formatter")
st.title("PPKI Academic Formatter")
st.header("1. Upload dokumen dan pilih jenjang")

uploaded = st.file_uploader("Dokumen DOCX", type=["docx"])
degree = st.selectbox("Jenjang", ["S1", "S2", "S3"])
try:
    max_upload_mb = int(os.environ.get("PPKI_MAX_UPLOAD_MB", "20"))
    if max_upload_mb < 1:
        raise ValueError
except ValueError:
    logging.warning("PPKI_MAX_UPLOAD_MB tidak valid; menggunakan 20 MB.")
    max_upload_mb = 20

document_key = sha256(uploaded.getvalue()).hexdigest() if uploaded is not None else "none"
input_key = (document_key, degree)
if st.session_state.get("input_key") != input_key:
    st.session_state.pop("audit_t4a", None)
    st.session_state.pop("output_t4a", None)
    st.session_state["input_key"] = input_key

try:
    rules = load_rules()
except ValueError as exc:
    st.error(f"Aturan gagal dimuat: {exc}")
else:
    applicable, review = filter_rules(rules, degree)
    st.success("Aturan berhasil dimuat dari snapshot lokal.")
    st.write(f"Jumlah aturan: {len(rules)}")
    st.write(f"Metadata is_implemented=true: {sum(rule['is_implemented'] for rule in rules)}")
    st.caption("Metadata tersebut bukan bukti handler tersedia.")
    st.write(f"Berlaku untuk {degree}: {len(applicable)}")
    st.write(f"Konteks penerapan perlu review: {len(review)}")
    with st.expander("Jumlah aturan berdasarkan domain"):
        st.dataframe([{"Domain": domain, "Jumlah": count} for domain, count in sorted(Counter(rule["domain"] for rule in rules).items())], hide_index=True)

styles = {}
illustrations = None
valid_upload = False
if uploaded is not None:
    try:
        validate_docx_input(uploaded.getvalue(), uploaded.name, max_upload_mb * 1024 * 1024)
        styles = font_candidates(uploaded.getvalue())
        illustrations = illustration_structure(uploaded.getvalue())
        valid_upload = True
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        logging.exception("Gagal membuka struktur DOCX upload")
        st.error("DOCX tidak dapat diproses. Periksa apakah file valid dan tidak rusak.")

st.header("2. Audit dan ringkasan")
st.subheader("Audit teks isi")
st.caption("Pilihan ini opsional untuk audit halaman dan BAB. Untuk dokumen dummy T4A, pilih Body Text (BodyText).")
style_order = sorted(styles, key=lambda key: (0 if key == "BodyText" else 1 if key == "Normal" else 2, styles[key]["name"].casefold()))
style_id = st.selectbox(
    "Style kandidat teks isi", [None, *style_order],
    key=f"body_style_{document_key}_{degree}",
    format_func=lambda key: "Pilih style" if key is None else f"{styles[key]['name']} ({key}) — {len(styles[key]['paragraphs'])} paragraf",
)
scope_key = (document_key, degree, style_id)
if st.session_state.get("scope_key") != scope_key:
    st.session_state.pop("audit_t4a", None)
    st.session_state.pop("output_t4a", None)
    st.session_state["scope_key"] = scope_key
if style_id:
    paragraphs = styles[style_id]["paragraphs"]
    if any(term in (style_id + " " + styles[style_id]["name"]).casefold() for term in ("title", "subtitle", "heading", "caption", "judul", "keterangan")):
        st.warning("Style ini kemungkinan digunakan untuk bagian khusus. Periksa seluruh kandidat sebelum mengonfirmasi sebagai teks isi.")
    st.write(f"{len(paragraphs)} paragraf kandidat. Pemilihan style tidak menjamin semuanya teks isi; periksa cakupan dalam dokumen.")
    for index, text in paragraphs[:3]:
        st.text(f"Paragraf {index}: {text[:200]}")

st.subheader("Audit Heading BAB")
candidates = heading_candidates(uploaded.getvalue()) if valid_upload and styles else []
st.write(f"Kandidat judul BAB (Heading 1): {len(candidates)}")
st.caption("Konfirmasi setiap kandidat secara terpisah. Heading lain tidak otomatis dianggap BAB.")

with st.form("audit_form", clear_on_submit=True):
    st.write("Konfirmasi teks isi (opsional untuk audit BAB):")
    confirmed = st.checkbox("Saya telah memeriksa dan memastikan semua paragraf kandidat style ini adalah teks isi utama untuk audit ini.", key=f"body_confirm_{document_key}_{degree}_{style_id}")
    st.write("Konfirmasi kandidat BAB:")
    heading_confirmed = set()
    for index, text in candidates:
        if st.checkbox(f"Paragraf {index}: {text}", key=f"chapter_{document_key}_{degree}_{index}"):
            heading_confirmed.add(index)
    heading_only = st.checkbox("Batasi rencana perbaikan pada heading BAB yang dikonfirmasi.", key=f"heading_only_{document_key}_{degree}")
    caption_confirmed = set()
    if illustrations and illustrations["caption"]:
        st.write("Konfirmasi dugaan hubungan caption dan objek (opsional):")
        for caption in illustrations["caption"]:
            if caption["dugaan_objek"] != "Tidak diketahui":
                if st.checkbox(f"{caption['lokasi']}: {caption['teks']} → {caption['dugaan_objek']}", key=f"caption_{document_key}_{degree}_{caption['lokasi']}"):
                    caption_confirmed.add(caption["lokasi"])
    submitted = st.form_submit_button("Audit")

summary_area = st.container()


def show_summary(counts):
    st.write("Ringkasan per aturan (termasuk konteks yang perlu review):")
    st.write(f"Diperiksa: {counts['diperiksa']} | pass: {counts['sesuai']} | fail: {counts['tidak_sesuai']} | needs_review: {counts['perlu_review']} | not_supported: {counts['tidak_didukung']}")
    st.caption("pass: sesuai pada cakupan yang diperiksa. fail: ketidaksesuaian terdeteksi validator yang didukung. needs_review: perlu pemeriksaan operator. not_supported: validator belum tersedia.")
    st.caption("Hasil paragraf hanya mencakup style yang dipilih dan dikonfirmasi; paragraf lain memerlukan pemeriksaan manual. Diagnostik kandidat tidak membuktikan kepatuhan PPKI.")


if submitted:
    st.session_state.pop("audit_t4a", None)
    st.session_state.pop("output_t4a", None)
    if uploaded is None:
        st.warning("Pilih dokumen DOCX terlebih dahulu.")
    elif not valid_upload:
        st.error("Audit dibatalkan karena file DOCX tidak valid atau tidak dapat diproses.")
    elif 'rules' not in locals():
        st.error("Audit tidak dapat dilakukan karena aturan gagal dimuat.")
    else:
        try:
            findings = audit_docx(uploaded.getvalue(), rules, degree, style_id, confirmed and style_id is not None, heading_confirmed)
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            logging.exception("Audit DOCX gagal")
            st.error("Audit gagal memproses DOCX. Periksa struktur file dan coba kembali.")
        else:
            counts = summarize(findings)
            with summary_area:
                show_summary(counts)
            st.header("3. Detail temuan dan diagnostik")
            st.dataframe(findings, hide_index=True)
            st.subheader("Struktur penomoran halaman")
            st.caption("Diagnostik read-only, bukan bukti kepatuhan. LAY-023 dan LAY-024 tetap belum didukung; penomoran aktual perlu review di Word.")
            try:
                st.dataframe(page_number_structure(uploaded.getvalue()), hide_index=True)
            except ValueError as exc:
                st.warning(str(exc))
            if illustrations is not None:
                st.subheader("Audit Tabel, Gambar, dan Caption")
                captions = [{**item, "hubungan_dikonfirmasi": item["lokasi"] in caption_confirmed} for item in illustrations["caption"]]
                st.write(f"Tabel: {len(illustrations['tabel'])} | Gambar inline: {len(illustrations['gambar'])} | Kandidat caption tabel: {sum(item['jenis'] == 'tabel' for item in captions)} | Kandidat caption gambar: {sum(item['jenis'] == 'gambar' for item in captions)} | Objek kompleks: {len(illustrations['objek_kompleks'])}")
                st.caption("Inventaris struktur memerlukan review; konfirmasi dugaan hubungan bukan validasi aturan. Aturan manual.not-implemented tetap tidak didukung.")
                for label, rows in (("Tabel", illustrations["tabel"]), ("Gambar inline", illustrations["gambar"]), ("Kandidat caption", captions), ("Objek kompleks", illustrations["objek_kompleks"])):
                    if rows:
                        st.write(label)
                        st.dataframe(rows, hide_index=True)
                rule_codes = {r["rule_code"] for r in rules if r["domain"] in {"TBL", "FIG"} or any(term in (r["element"] + " " + r["official_requirement"]).casefold() for term in ("caption", "ilustrasi", "gambar", "tabel"))}
                related_findings = [item for item in findings if item["rule_code"] in rule_codes]
                if related_findings:
                    st.write("Status aturan terkait")
                    st.dataframe(related_findings, hide_index=True)
            st.subheader("Audit Sitasi dan Daftar Pustaka")
            diagnostics = citation_diagnostics(uploaded.getvalue())
            rows = diagnostics["perbandingan"]
            st.write(f"Kandidat sitasi: {len(diagnostics['sitasi'])} | Kandidat referensi: {len(diagnostics['referensi'])} | Sitasi mungkin cocok: {sum(row['jenis'] == 'sitasi' and row['status'] == 'mungkin_cocok' for row in rows)} | Sitasi tanpa kandidat referensi: {sum(row['status'] == 'kandidat_referensi_tidak_ditemukan' for row in rows)} | Referensi tanpa kandidat sitasi: {sum(row['status'] == 'kandidat_sitasi_tidak_ditemukan' for row in rows)} | Perlu review: {sum(row['status'] == 'needs_review' for row in rows)}")
            st.caption("Pemeriksaan silang hanya diagnostik kandidat, bukan bukti kepatuhan PPKI. Aturan manual.not-implemented tetap tidak didukung; hasil dan pasangan perlu diperiksa manusia.")
            citation_rules = [r for r in rules if r["domain"] in {"CIT", "REF"} or any(term in (r["element"] + " " + r["official_requirement"]).casefold() for term in ("sitasi", "kutipan", "daftar pustaka", "perujukan", "pengutipan", "mengutip", "rujukan", "referensi"))]
            st.write(f"Aturan terkait: {len(citation_rules)}; validator manual yang belum didukung: {sum(r['validation_key'] == 'manual.not-implemented' for r in citation_rules)}. Konteks penerapan beberapa aturan juga memerlukan review.")
            for note in diagnostics["catatan"]:
                st.warning(note)
            if rows:
                st.dataframe(rows, hide_index=True)
            st.subheader("Audit Struktur Dokumen")
            recognized = recognize_structure(uploaded.getvalue())
            counts_structure = Counter(item["jenis"] for item in recognized)
            st.write(f"Pengenalan struktur (kandidat): BAB {counts_structure['bab']} | Subbab {counts_structure['subbab'] + counts_structure['sub_subbab']} | Teks isi {counts_structure['teks_isi']} | Caption tabel {counts_structure['caption_tabel']} | Caption gambar {counts_structure['caption_gambar']} | Perlu review {sum(item['status'] == 'needs_review' for item in recognized)}")
            st.caption("Pengenalan read-only; tidak mengubah cakupan audit atau perbaikan dan bukan bukti kepatuhan PPKI.")
            with st.expander("Hasil pengenalan struktur dan contoh perlu review"):
                st.dataframe(recognized, hide_index=True)
            scope = safe_format_scope(uploaded.getvalue(), rules, degree)
            scope_counts = Counter(item["keputusan"] for item in scope)
            st.write(f"Pratinjau cakupan eksperimental: auto_safe {scope_counts['auto_safe']} | needs_review {scope_counts['needs_review']} | protected {scope_counts['protected']} | Paragraf dengan usulan perubahan {sum(bool(item['aturan_berubah']) for item in scope)}")
            st.write(f"Paragraf eligible: {sum(any(c['eligible'] for c in item['rule_decisions']) for item in scope)} | Paragraf needs_change: {sum(any(c['needs_change'] is True for c in item['rule_decisions']) for item in scope)} | Paragraf safe_to_apply: {sum(any(c['safe_to_apply'] for c in item['rule_decisions']) for item in scope)}")
            st.caption("Dry-run eksperimental: eligible berarti layak diperiksa; needs_change berarti nilainya tidak sesuai; safe_to_apply menilai perubahan teknis per aturan, bukan izin menjalankan formatter. Nilai yang sudah sesuai tetap dapat dinilai aman. Kandidat Normal atau konteks ambigu tetap membutuhkan konfirmasi; bantuan AI belum tersedia.")
            with st.expander("Detail pratinjau cakupan"):
                st.dataframe([{key: value for key, value in row.items() if key != 'rule_decisions'} for row in scope], hide_index=True)
                st.write("Keputusan per paragraf dan aturan (None berarti belum diketahui):")
                st.dataframe([{"lokasi": row["lokasi"], "jenis": row["jenis"], **{key: value for key, value in check.items() if key != 'reason_codes'}} for row in scope for check in row["rule_decisions"]], hide_index=True)
            structure = document_structure(uploaded.getvalue())
            st.caption("Urutan berikut adalah inventaris kandidat, bukan validasi kepatuhan atau daftar bagian wajib. Identitas dan urutan perlu review; bagian tanpa kandidat belum tentu tidak ada.")
            if structure["bagian"]:
                st.dataframe(structure["bagian"], hide_index=True)
            st.write("Belum ditemukan kandidat untuk: " + (", ".join(structure["tanpa_kandidat"]) or "Tidak ada"))
            structure_rules = [r for r in applicable + review if r["domain"] in {"STR", "CVR", "ABS"} or r["domain"] == "CNT" and any(term in (r["element"] + " " + r["official_requirement"]).casefold() for term in ("struktur", "bagian awal", "bagian inti", "bagian akhir", "urutan", "susunan bab"))]
            st.write(f"Aturan terkait untuk {degree} dan konteks yang belum dipetakan: {len(structure_rules)}. Validator struktur T11 belum tersedia.")
            with st.expander("Inventaris aturan struktur terkait"):
                st.dataframe([{**{key: r[key] for key in ("rule_code", "domain", "element", "official_requirement", "expected_value_pattern", "validation_key", "applies_to", "fix_mode", "severity", "source_section", "pdf_page", "printed_page")}, "status_validator": "not_supported"} for r in structure_rules], hide_index=True)
            body_confirmed = bool(confirmed and style_id)
            plan = plan_changes(uploaded.getvalue(), rules, degree, style_id, body_confirmed, heading_confirmed, heading_only)
            signature = sha256(uploaded.getvalue() + json.dumps(rules, sort_keys=True).encode()).hexdigest()
            skipped = skipped_changes(uploaded.getvalue(), rules, degree, findings, plan, style_id, body_confirmed, heading_only)
            st.session_state.audit_t4a = {"signature": signature, "degree": degree, "style": style_id, "confirmed": body_confirmed, "heading_confirmed": heading_confirmed, "heading_only": heading_only, "plan": plan, "before": counts, "skipped": skipped}

snapshot = st.session_state.get("audit_t4a")
if snapshot and valid_upload and uploaded is not None and 'rules' in locals():
    signature = sha256(uploaded.getvalue() + json.dumps(rules, sort_keys=True).encode()).hexdigest()
    if (snapshot["signature"], snapshot["degree"], snapshot["style"]) == (signature, degree, style_id):
        if not submitted:
            with summary_area:
                show_summary(snapshot["before"])
        st.header("4. Rencana perbaikan dan download")
        st.write("Rencana perbaikan (hanya aturan Auto):")
        if snapshot["plan"]:
            st.dataframe(snapshot["plan"], hide_index=True)
            if st.button("Terapkan Perbaikan Otomatis"):
                st.session_state.pop("output_t4a", None)
                try:
                    output, after, changes = format_docx(uploaded.getvalue(), rules, degree, style_id, snapshot["confirmed"], snapshot["heading_confirmed"], snapshot["heading_only"])
                    if changes != snapshot["plan"]:
                        raise ValueError("Rencana berubah; lakukan audit kembali.")
                except (ValueError, OSError) as exc:
                    st.error(f"Perbaikan gagal divalidasi: {exc}")
                except Exception:
                    logging.exception("Perbaikan DOCX gagal")
                    st.error("Perbaikan gagal diproses atau divalidasi; file hasil tidak tersedia.")
                else:
                    after_map = {(item["rule_code"], item["location"]): item for item in after}
                    report = [{"rule_code": item["rule_code"], "lokasi": item["location"], "sebelum": item["actual"], "sesudah": after_map[(item["rule_code"], item["location"])]["actual"], "target": item["expected"], "status": after_map[(item["rule_code"], item["location"])]["status"]} for item in changes]
                    st.session_state.output_t4a = {"data": output, "after": summarize(after), "changes": changes, "report": report, "signature": signature}
        else:
            st.info("Tidak ada perubahan Auto yang dapat diterapkan. Temuan lain memerlukan review.")
        if snapshot["skipped"]:
            with st.expander(f"Dilewati beserta alasan ({len(snapshot['skipped'])})"):
                st.dataframe(snapshot["skipped"], hide_index=True)
        output = st.session_state.get("output_t4a")
        if output and output["signature"] == signature:
            st.success(f"{len(output['changes'])} perubahan lolos validasi dan audit ulang.")
            st.write("Ringkasan sebelum:", snapshot["before"])
            st.write("Ringkasan sesudah:", output["after"])
            st.write(f"Diterapkan: {len(output['changes'])}; dilewati: {len(snapshot['skipped'])}; gagal: 0.")
            st.dataframe(output["report"], hide_index=True)
            filename = Path(uploaded.name).stem + "_formatted.docx"
            st.download_button("Unduh DOCX hasil", output["data"], file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            report_file = StringIO(newline="")
            writer = csv.DictWriter(report_file, fieldnames=["rule_code", "lokasi", "sebelum", "sesudah", "target", "status"])
            writer.writeheader()
            writer.writerows(output["report"])
            st.download_button("Unduh laporan perubahan CSV", report_file.getvalue(), file_name=Path(uploaded.name).stem + "_perubahan.csv", mime="text/csv")

# This opt-in panel only reads the fixed private local sample and never feeds the formatter.
if os.environ.get("PPKI_LOCAL_REVIEW") == "1" and 'rules' in locals():
    if st.get_option("server.address") not in {"localhost", "127.0.0.1", "::1"}:
        st.warning("Review privat hanya tersedia jika Streamlit diikat ke localhost.")
    else:
        with st.expander("Review privat sampel operator"):
            st.caption("Hanya lokal. Teks dokumen ditampilkan di layar dan tidak disimpan dalam CSV label. Hasil review tidak mengaktifkan formatter.")
            if st.checkbox("Buka 40 sampel privat", key="open_private_review"):
                try:
                    review_data = operator_review.load_review(rules, operator_review.PRIVATE_DIR, max_upload_mb * 1024 * 1024)
                    location = st.selectbox("Lokasi sampel", review_data["locations"], key="private_sample_location_" + review_data["digest"])
                    context = operator_review.paragraph_context(review_data["data"], location)
                    predicted = review_data["recognized"].get(location, {"jenis": "kosong", "alasan": "Paragraf kosong."})
                    scope_row = review_data["scope"][location]
                    st.write(f"Lokasi: {location} | Prediksi: {predicted['jenis']} | Cakupan: {scope_row['keputusan']}")
                    st.write("Alasan classifier:", predicted["alasan"], scope_row["alasan"])
                    st.write("Konteks sebelum (maksimum 200 karakter):")
                    st.text(context["sebelum"][-200:])
                    st.write("Paragraf terpilih:")
                    st.text(context["teks"])
                    st.write("Konteks sesudah (maksimum 200 karakter):")
                    st.text(context["sesudah"][:200])
                    st.dataframe([{"rule_code": c["rule_code"], "ketentuan": next((r["official_requirement"] for r in rules if r["rule_code"] == c["rule_code"]), "Tidak tersedia"), "status": c["status"], "alasan": c["alasan"]} for c in scope_row["rule_decisions"]], hide_index=True)
                    label = review_data["labels"].get(location, {})
                    role_names = {"": "Belum diisi (PENDING)", "teks_isi": "Teks isi biasa", "bab": "Heading BAB", "subbab": "Subbab", "caption": "Caption", "bagian_khusus": "Bagian khusus", "daftar_pustaka": "Daftar pustaka", "lainnya": "Lainnya", "belum_yakin": "Belum yakin"}
                    safety_names = {"": "Belum diisi (PENDING)", "aman": "Aman diperbaiki", "tidak_aman": "Tidak aman diperbaiki", "belum_yakin": "Belum yakin"}
                    widget_key = review_data["digest"] + "_" + location
                    with st.form("private_review_" + widget_key):
                        role_values = ("", *operator_review.ROLES)
                        role = st.selectbox("Jenis menurut operator", role_values, index=role_values.index(label.get("operator_role", "")), format_func=lambda value: role_names[value], key="private_role_" + widget_key)
                        safety_values = ("", *operator_review.SAFETY)
                        answers = {}
                        for code in operator_review.RULE_CODES:
                            answers[code] = st.selectbox(code, safety_values, index=safety_values.index(label.get(code, "")), format_func=lambda value: safety_names[value], key="private_" + code + "_" + widget_key)
                        saved = st.form_submit_button("Simpan label lokal")
                    if saved:
                        operator_review.save_label(operator_review.PRIVATE_DIR, review_data["digest"], set(review_data["locations"]), location, role, answers)
                        review_data["labels"] = operator_review.load_labels(operator_review.PRIVATE_DIR, review_data["digest"], set(review_data["locations"]))
                        st.success("Label disimpan di CSV privat. Label ini tidak mengubah rencana perbaikan.")
                    evaluation = operator_review.evaluate_review(review_data["locations"], review_data["recognized"], review_data["scope"], review_data["labels"])
                    st.write(f"Jenis PENDING/belum yakin: {evaluation['jenis_pending']} | Penilaian aturan PENDING/belum yakin: {evaluation['aturan_pending']}")
                    st.caption("Hanya label eksplisit dibandingkan. Prediksi ambigu dihitung dalam FN dan juga ditampilkan terpisah. Precision/recall memerlukan minimal lima label positif dan lima label kategori lain; hasil hanya berlaku untuk sampel yang dilabeli.")
                    st.dataframe(evaluation["klasifikasi"], hide_index=True)
                    st.dataframe(evaluation["keamanan"], hide_index=True)
                except ValueError as exc:
                    st.error(str(exc))
                except Exception:
                    logging.error("Review privat gagal; periksa file lokal dan konfigurasi.")
                    st.error("Review privat tidak dapat dibuka atau disimpan. Periksa file lokal.")
