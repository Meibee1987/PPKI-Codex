import streamlit as st
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import csv
from io import StringIO

from core.rules import filter_rules, load_rules
from core.audit import audit_docx, summarize, font_candidates, heading_candidates, page_number_structure, illustration_structure
from core.formatter import format_docx, plan_changes, skipped_changes


st.set_page_config(page_title="PPKI Academic Formatter")
st.title("PPKI Academic Formatter")
st.write("Unggah dokumen dan pilih jenjang karya ilmiah.")

uploaded = st.file_uploader("Dokumen DOCX", type=["docx"])
degree = st.selectbox("Jenjang", ["S1", "S2", "S3"])

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
    st.write("Jumlah aturan berdasarkan domain:")
    st.dataframe([{"Domain": domain, "Jumlah": count} for domain, count in sorted(Counter(rule["domain"] for rule in rules).items())], hide_index=True)

styles = {}
illustrations = None
if uploaded is not None:
    try:
        styles = font_candidates(uploaded.getvalue())
        illustrations = illustration_structure(uploaded.getvalue())
    except ValueError as exc:
        st.error(str(exc))

st.subheader("Audit teks isi")
st.caption("Pilihan ini opsional untuk audit halaman dan BAB. Untuk dokumen dummy T4A, pilih Body Text (BodyText).")
style_order = sorted(styles, key=lambda key: (0 if key == "BodyText" else 1 if key == "Normal" else 2, styles[key]["name"].casefold()))
style_id = st.selectbox(
    "Style kandidat teks isi", [None, *style_order],
    format_func=lambda key: "Pilih style" if key is None else f"{styles[key]['name']} ({key}) — {len(styles[key]['paragraphs'])} paragraf",
)
if style_id:
    paragraphs = styles[style_id]["paragraphs"]
    if any(term in (style_id + " " + styles[style_id]["name"]).casefold() for term in ("title", "subtitle", "heading", "caption", "judul", "keterangan")):
        st.warning("Style ini kemungkinan digunakan untuk bagian khusus. Periksa seluruh kandidat sebelum mengonfirmasi sebagai teks isi.")
    st.write(f"{len(paragraphs)} paragraf kandidat. Pemilihan style tidak menjamin semuanya teks isi; periksa cakupan dalam dokumen.")
    for index, text in paragraphs[:3]:
        st.text(f"Paragraf {index}: {text[:200]}")

st.subheader("Audit Heading BAB")
candidates = heading_candidates(uploaded.getvalue()) if uploaded is not None and styles else []
st.write(f"Kandidat judul BAB (Heading 1): {len(candidates)}")
st.caption("Konfirmasi setiap kandidat secara terpisah. Heading lain tidak otomatis dianggap BAB.")

with st.form("audit_form", clear_on_submit=True):
    st.write("Konfirmasi teks isi (opsional untuk audit BAB):")
    confirmed = st.checkbox("Saya telah memeriksa dan memastikan semua paragraf kandidat style ini adalah teks isi utama untuk audit ini.")
    st.write("Konfirmasi kandidat BAB:")
    heading_confirmed = set()
    document_key = sha256(uploaded.getvalue()).hexdigest() if uploaded is not None else "none"
    for index, text in candidates:
        if st.checkbox(f"Paragraf {index}: {text}", key=f"chapter_{document_key}_{index}"):
            heading_confirmed.add(index)
    heading_only = st.checkbox("Batasi rencana perbaikan pada heading BAB yang dikonfirmasi.")
    caption_confirmed = set()
    if illustrations and illustrations["caption"]:
        st.write("Konfirmasi dugaan hubungan caption dan objek (opsional):")
        for caption in illustrations["caption"]:
            if caption["dugaan_objek"] != "Tidak diketahui":
                if st.checkbox(f"{caption['lokasi']}: {caption['teks']} → {caption['dugaan_objek']}", key=f"caption_{document_key}_{caption['lokasi']}"):
                    caption_confirmed.add(caption["lokasi"])
    submitted = st.form_submit_button("Audit")

if submitted:
    st.session_state.pop("audit_t4a", None)
    st.session_state.pop("output_t4a", None)
    if uploaded is None:
        st.warning("Pilih dokumen DOCX terlebih dahulu.")
    elif 'rules' not in locals():
        st.error("Audit tidak dapat dilakukan karena aturan gagal dimuat.")
    else:
        try:
            findings = audit_docx(uploaded.getvalue(), rules, degree, style_id, confirmed and style_id is not None, heading_confirmed)
        except ValueError as exc:
            st.error(str(exc))
        else:
            counts = summarize(findings)
            st.write("Ringkasan per aturan (termasuk konteks yang perlu review):")
            st.caption("Hasil paragraf hanya mencakup style yang dipilih dan dikonfirmasi; paragraf lain memerlukan pemeriksaan manual. Usulan perubahan hanya dry-run.")
            st.write(f"Diperiksa: {counts['diperiksa']} | Sesuai: {counts['sesuai']} | Tidak sesuai: {counts['tidak_sesuai']} | Tidak didukung: {counts['tidak_didukung']} | Perlu review: {counts['perlu_review']}")
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
            body_confirmed = bool(confirmed and style_id)
            plan = plan_changes(uploaded.getvalue(), rules, degree, style_id, body_confirmed, heading_confirmed, heading_only)
            signature = sha256(uploaded.getvalue() + json.dumps(rules, sort_keys=True).encode()).hexdigest()
            skipped = skipped_changes(uploaded.getvalue(), rules, degree, findings, plan, style_id, body_confirmed, heading_only)
            st.session_state.audit_t4a = {"signature": signature, "degree": degree, "style": style_id, "confirmed": body_confirmed, "heading_confirmed": heading_confirmed, "heading_only": heading_only, "plan": plan, "before": counts, "skipped": skipped}

snapshot = st.session_state.get("audit_t4a")
if snapshot and uploaded is not None and 'rules' in locals():
    signature = sha256(uploaded.getvalue() + json.dumps(rules, sort_keys=True).encode()).hexdigest()
    if (snapshot["signature"], snapshot["degree"], snapshot["style"]) == (signature, degree, style_id):
        st.write("Rencana perbaikan (hanya aturan Auto):")
        if snapshot["plan"]:
            st.dataframe(snapshot["plan"], hide_index=True)
            if st.button("Terapkan Perbaikan"):
                st.session_state.pop("output_t4a", None)
                try:
                    output, after, changes = format_docx(uploaded.getvalue(), rules, degree, style_id, snapshot["confirmed"], snapshot["heading_confirmed"], snapshot["heading_only"])
                    if changes != snapshot["plan"]:
                        raise ValueError("Rencana berubah; lakukan audit kembali.")
                except (ValueError, OSError) as exc:
                    st.error(f"Perbaikan gagal divalidasi: {exc}")
                else:
                    after_map = {(item["rule_code"], item["location"]): item for item in after}
                    report = [{"rule_code": item["rule_code"], "lokasi": item["location"], "sebelum": item["actual"], "sesudah": after_map[(item["rule_code"], item["location"])]["actual"], "target": item["expected"], "status": after_map[(item["rule_code"], item["location"])]["status"]} for item in changes]
                    st.session_state.output_t4a = {"data": output, "after": summarize(after), "changes": changes, "report": report, "signature": signature}
        else:
            st.info("Tidak ada perubahan Auto yang dapat diterapkan. Temuan lain memerlukan review.")
        if snapshot["skipped"]:
            st.write("Dilewati beserta alasan:")
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
