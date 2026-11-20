import streamlit as st
from collections import Counter
from hashlib import sha256
import json
import importlib
from pathlib import Path
import csv
import logging
import os
from io import StringIO, BytesIO
from docx import Document

from core.rules import filter_rules, load_rules
from core.audit import audit_docx, summarize, font_candidates, heading_candidates, page_number_structure, illustration_structure, citation_diagnostics, document_structure, validate_docx_input
from core.formatter import format_docx, plan_changes, skipped_changes, format_margins, font_targets
from core.structure import document_structure_map, recognize_structure, safe_format_scope
import core.operator_review as operator_review
import core.ai_planner as ai_planner
import core.pilot as pilot
import core.ai_beta as ai_beta

# Streamlit reruns app.py while imported modules may remain cached after an update.
if getattr(ai_beta, "BETA_RESULT_CONTRACT_VERSION", None) != 2:
    ai_beta = importlib.reload(ai_beta)


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
    st.session_state.pop("ai_preview", None)
    st.session_state.pop("pilot_result", None)
    st.session_state.pop("pilot_plan", None)
    st.session_state.pop("beta_result", None)
    st.session_state.pop("beta_failure", None)
    st.session_state.pop("margin_result", None)
    st.session_state.pop("evaluation_sample", None)
    st.session_state.pop("evaluation_result", None)
    st.session_state.pop("evaluation_import", None)
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

st.subheader("Perbaikan Otomatis dengan AI — pratinjau")
st.caption("Tahap ini hanya menganalisis dan tidak menerapkan perubahan. Maksimal 30 kandidat, masing-masing 180 karakter, dikirim dalam satu permintaan; kandidat lain belum dianalisis.")
st.warning("Jika disetujui, potongan teks dan informasi struktur dokumen akan dikirim ke OpenAI API dan dapat menimbulkan biaya. Jangan kirim data yang tidak ingin Anda bagikan.")
ai_model = st.text_input("Model OpenAI yang tersedia pada akun API", value=os.environ.get("OPENAI_MODEL", ""))
ai_tokens = st.number_input("Batas token output per permintaan", min_value=256, max_value=4096, value=1024, step=256)
ai_consent = st.checkbox("Saya menyetujui pengiriman potongan dokumen ke OpenAI untuk pratinjau ini.", key=f"ai_consent_{document_key}_{degree}")
ai_signature = (input_key, ai_model, ai_tokens)
if st.session_state.get("ai_signature") != ai_signature or not ai_consent:
    st.session_state.pop("ai_preview", None)
    st.session_state.ai_signature = ai_signature

def show_ai_usage(usage):
    if usage is None:
        st.caption("Penggunaan token tidak tersedia dari respons API.")
    else:
        def display(key):
            return usage[key] if usage[key] is not None else "tidak tersedia"
        st.caption(f"Token input: {display('input_tokens')} | output: {display('output_tokens')} | total: {display('total_tokens')}")

if st.button("Perbaiki Otomatis dengan AI (pratinjau)"):
    st.session_state.pop("ai_preview", None)
    if not ai_consent:
        st.warning("Persetujuan pengiriman diperlukan sebelum memanggil API.")
    elif not valid_upload or 'rules' not in locals():
        st.error("Pilih DOCX yang valid dan pastikan aturan tersedia.")
    else:
        try:
            prepared = ai_planner.prepare_analysis(uploaded.getvalue(), rules, degree, max_upload_mb * 1024 * 1024)
            result = ai_planner.request_analysis(prepared, ai_model, ai_tokens)
        except ai_planner.AnalysisError as exc:
            st.error(str(exc))
            show_ai_usage(exc.usage)
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Pratinjau AI gagal diproses; tidak ada rencana yang digunakan.")
        else:
            st.session_state.ai_preview = {"signature": ai_signature, "plan": result["plan"], "usage": result["usage"], "selected": prepared["selected_count"], "remaining": prepared["unprocessed_count"], "old": prepared["old_safe_count"], "protected": prepared["protected_count"], "omitted": prepared["omitted"]}
preview = st.session_state.get("ai_preview")
if preview and preview["signature"] == ai_signature:
    show_ai_usage(preview["usage"])
    st.write(f"Kandidat dikirim: {preview['selected']} | Belum dikirim: {preview['remaining']} | Paragraf dengan perubahan potensial menurut classifier lokal: {preview['old']}")
    st.write(f"Elemen dilindungi dan tidak dikirim: {preview['protected']}")
    st.write(f"Paragraf dengan usulan AI lolos pemeriksaan lokal: {len({row['lokasi'] for row in preview['plan'] if row['status'] == 'kandidat_pratinjau'})} | Usulan perlu review: {sum(row['status'] == 'needs_review' for row in preview['plan'])}")
    st.write(f"Keputusan usulan: diterima sebagai pratinjau {sum(row['status'] == 'kandidat_pratinjau' for row in preview['plan'])} | sudah sesuai {sum(row['status'] == 'sudah_sesuai' for row in preview['plan'])} | perlu review {sum(row['status'] == 'needs_review' for row in preview['plan'])}")
    st.caption("Cakupan AI dibatasi pada kandidat yang dikirim; jumlah classifier lokal mencakup seluruh dokumen. Tidak ada perubahan DOCX yang diterapkan.")
    st.dataframe(preview["plan"], hide_index=True)
    if preview["omitted"]:
        with st.expander("Kandidat belum dianalisis AI"):
            st.dataframe(preview["omitted"], hide_index=True)

st.subheader("Perbaiki Otomatis dengan AI — Beta")
st.warning("Beta mengirim teks kandidat dan konteks ke OpenAI, dapat dikenai biaya, dan klasifikasi dapat keliru. Periksa hasil di Word sebelum digunakan.")
st.caption("Kandidat diproses bertahap hingga selesai atau batas anggaran perkiraan tercapai. Atur harga sesuai model dan mata uang yang Anda gunakan.")
beta_batch_size = st.number_input("Jumlah kandidat per batch", min_value=1, max_value=30, value=30)
beta_budget = st.number_input("Anggaran maksimum per dokumen", min_value=0.000001, value=1.0, format="%.6f")
beta_price_in = st.number_input("Harga input per sejuta token", min_value=0.000001, value=1.0, format="%.6f")
beta_price_out = st.number_input("Harga output per sejuta token", min_value=0.000001, value=1.0, format="%.6f")
st.caption("Biaya bersifat perkiraan berdasarkan harga yang diisi dan token yang tersedia; tagihan aktual dapat berbeda. Harga bukan batas biaya yang dijamin penyedia.")
beta_consent = st.checkbox("Saya menyetujui pengiriman teks ke OpenAI dan penerapan perubahan beta pada salinan dokumen.", key=f"beta_consent_{document_key}_{degree}")
beta_signature = (input_key, ai_model, ai_tokens, beta_consent, beta_batch_size, beta_budget, beta_price_in, beta_price_out, ai_beta.BETA_RESULT_CONTRACT_VERSION)
if st.session_state.get("beta_signature") != beta_signature:
    if st.session_state.get("beta_result") is not None:
        previous = st.session_state.beta_result
        if not isinstance(previous, dict) or not isinstance(previous.get("operations"), list):
            st.error("Hasil Beta sebelumnya tidak memiliki laporan operasi lengkap; DOCX tidak tersedia. Hasil lama dibatalkan.")
        else:
            st.warning("Hasil Beta sebelumnya dibatalkan karena parameter atau versi hasil berubah.")
    st.session_state.pop("beta_result", None)
    st.session_state.pop("beta_failure", None)
    st.session_state.pop("margin_result", None)
    st.session_state.beta_signature = beta_signature
if st.button("Perbaiki Otomatis dengan AI — Beta"):
    st.session_state.pop("beta_result", None)
    st.session_state.pop("beta_failure", None)
    st.session_state.pop("margin_result", None)
    if not beta_consent:
        st.warning("Persetujuan tingkat dokumen diperlukan.")
    elif not valid_upload or 'rules' not in locals():
        st.error("Pilih DOCX valid dan pastikan aturan tersedia.")
    else:
        try:
            prepared_beta = ai_beta.prepare_beta(uploaded.getvalue(), rules, degree, max_upload_mb * 1024 * 1024, all_candidates=True)
            progress_beta = st.empty()
            def show_beta_progress(stage, batch, total, remaining, estimate, batch_cost):
                if stage == "starting":
                    progress_beta.info(f"Batch {batch} akan dikirim: perkiraan maksimal input {estimate} token; biaya perkiraan {batch_cost:.6f}.")
                else:
                    progress_beta.info(f"Batch {batch} selesai; {total - remaining}/{total} kandidat diproses, {remaining} belum diproses.")
            batching = ai_beta.request_batches(prepared_beta, ai_model, ai_tokens, batch_size=beta_batch_size,
                budget=beta_budget, input_price=beta_price_in, output_price=beta_price_out, progress=show_beta_progress)
            beta_result = ai_beta.format_beta(uploaded.getvalue(), rules, degree, prepared_beta, batching["decisions"])
            beta_result["batching"] = batching
            ai_beta.validate_beta_result(beta_result)
            st.session_state.beta_result = beta_result
        except ai_beta.BetaValidationError as exc:
            st.error(str(exc))
            st.session_state.beta_failure = exc.operations
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Pemrosesan beta gagal; hasil tidak tersedia.")
beta_failure = st.session_state.get("beta_failure")
if beta_failure and beta_consent:
    st.warning("Seluruh hasil dibatalkan; tidak ada DOCX tervalidasi. Laporan berikut berisi operasi yang gagal divalidasi.")
    failed_csv = StringIO(newline="")
    failed_writer = csv.DictWriter(failed_csv, fieldnames=["lokasi", "rule_code", "sebelum", "sesudah", "target", "status", "alasan"])
    failed_writer.writeheader(); failed_writer.writerows(beta_failure)
    st.download_button("Unduh laporan kegagalan beta CSV", failed_csv.getvalue(), file_name=Path(uploaded.name).stem + "_beta_failed.csv", mime="text/csv")
beta_result = st.session_state.get("beta_result")
if beta_result is not None and beta_consent:
    try:
        ai_beta.validate_beta_result(beta_result)
    except ValueError as exc:
        st.session_state.pop("beta_result", None)
        st.session_state.pop("margin_result", None)
        beta_result = None
        st.error(str(exc))
if beta_result and beta_consent:
    st.success("Status akhir: tervalidasi — formatter, audit ulang, integritas DOCX dan laporan operasi lengkap.")
    batching = beta_result["batching"]
    st.write(f"Batch: {len(batching['batches'])} | Token input: {batching['input_tokens']} | Token output: {batching['output_tokens']} | Total token: {batching['input_tokens'] + batching['output_tokens']} | Biaya perkiraan: {batching['cost']:.6f}")
    if not batching["usage_complete"]:
        st.warning("Token aktual tidak lengkap; biaya aktual belum dapat dihitung dan batch berikutnya dihentikan.")
    with st.expander("Rincian batch"):
        st.dataframe(batching["batches"], hide_index=True)
    counts = beta_result["counts"]
    summary_beta = beta_result["summary"]
    st.write(f"Kandidat terverifikasi: {counts.get('body_verified', 0)} | Dilindungi: {counts.get('protected', 0)} | Perlu review: {counts.get('uncertain', 0)} | Belum dianalisis: {counts.get('unprocessed', 0)}")
    st.write(f"Perubahan divalidasi: {summary_beta['planned']} | Nilai sudah sesuai: {summary_beta['known_compliant']} | Keputusan dilewati: {summary_beta['rejected']}")
    op_counts = Counter(row["status"] for row in beta_result["operations"])
    st.caption(f"Operasi: applied {op_counts['applied']} | already_compliant {op_counts['already_compliant']} | protected {op_counts['protected']} | uncertain {op_counts['uncertain']} | failed 0. Kegagalan validasi membatalkan seluruh hasil.")
    st.caption("Jumlah nilai sudah sesuai hanya untuk kandidat yang dipilih AI; bukan bukti kepatuhan seluruh dokumen.")
    exceptions_beta = [x for x in beta_result["decisions"] if x["status"] != "body_verified"]
    with st.expander("Pengecualian beta"):
        st.dataframe(exceptions_beta, hide_index=True)
        st.dataframe([r for r in beta_result["plan"] if r["unsafe_or_ambiguous"]], hide_index=True)
    with st.expander("Laporan operasi setelah validasi"):
        st.dataframe(beta_result["operations"], hide_index=True)
    report_beta = StringIO(newline="")
    writer_beta = csv.DictWriter(report_beta, fieldnames=["lokasi", "rule_code", "sebelum", "sesudah", "target", "status", "alasan"])
    writer_beta.writeheader(); writer_beta.writerows(beta_result["operations"])
    st.download_button("Unduh laporan operasi beta CSV", report_beta.getvalue(), file_name=Path(uploaded.name).stem + "_beta_operations.csv", mime="text/csv")
    if summary_beta["planned"]:
        st.download_button("Download DOCX hasil beta", beta_result["data"], file_name=Path(uploaded.name).stem + "_beta_formatted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

st.subheader("Perbaikan margin tanpa AI")
st.caption("Memakai salinan Beta yang tervalidasi bila tersedia, atau dokumen unggahan. Font hanya diterapkan pada cakupan Beta yang sudah diverifikasi; tidak ada permintaan AI baru.")
if st.button("Perbaiki margin deterministik"):
    st.session_state.pop("margin_result", None)
    if not valid_upload or 'rules' not in locals():
        st.error("Pilih DOCX valid dan pastikan aturan tersedia.")
    else:
        try:
            source = beta_result["data"] if beta_result else uploaded.getvalue()
            margin_doc, margin_rows = format_margins(source, rules, degree)
            previous_operations = beta_result["operations"] if beta_result else []
            font_rows = [r for r in previous_operations if r["rule_code"] == "PPKI-LAY-005" and r["status"] == "applied"]
            source_doc = Document(BytesIO(uploaded.getvalue()))
            targets_by_paragraph = [font_targets(source_doc.paragraphs[int(r["lokasi"].split(":")[1]) - 1], r["target"]) for r in font_rows]
            font_runs = sum(len(targets) for targets in targets_by_paragraph) if all(targets is not None for targets in targets_by_paragraph) else None
            st.session_state.margin_result = {"data": margin_doc, "rows": margin_rows, "previous": previous_operations, "font_runs": font_runs,
                                               "unknown_normalized": beta_result["summary"]["unknown_to_normalize"] if beta_result else 0,
                                               "changed": margin_doc != uploaded.getvalue()}
        except ValueError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Validasi margin gagal; DOCX hasil tidak tersedia.")
margin_result = st.session_state.get("margin_result")
if margin_result:
    margin_rows = margin_result["rows"]
    applied_sections = {row["lokasi"] for row in margin_rows if row["status"] == "applied"}
    previous = margin_result["previous"]
    paragraphs = {r["lokasi"] for r in previous if r["status"] == "applied"}
    rejected = sum(r['status'] in {'uncertain', 'protected'} for r in margin_rows + previous)
    st.write(f"Section diperbaiki: {len(applied_sections)} | Paragraf diperbaiki: {len(paragraphs)} | Run font diperbaiki: {margin_result['font_runs'] if margin_result['font_runs'] is not None else 'tidak dapat dipastikan'} | Normalisasi nilai tidak diketahui: {margin_result['unknown_normalized']} | Operasi dilewati: {rejected}.")
    st.write(f"Operasi diterapkan: {sum(r['status'] == 'applied' for r in margin_rows + previous)} | Sudah sesuai: {sum(r['status'] == 'already_compliant' for r in margin_rows + previous)} | Gagal: 0 (hasil telah divalidasi).")
    st.caption("Normalisasi font dari nilai tidak diketahui: 0; font yang tidak pasti tetap perlu review.")
    st.dataframe(margin_rows, hide_index=True)
    margin_csv = StringIO(newline="")
    margin_writer = csv.DictWriter(margin_csv, fieldnames=["lokasi", "rule_code", "properti", "sebelum", "sesudah", "target", "status", "alasan"])
    margin_writer.writeheader(); margin_writer.writerows(margin_rows)
    for row in previous:
        margin_writer.writerow({**row, "properti": "font" if row["rule_code"] == "PPKI-LAY-005" else row["rule_code"]})
    st.download_button("Unduh laporan margin CSV", margin_csv.getvalue(), file_name=Path(uploaded.name).stem + "_margin_report.csv", mime="text/csv")
    if margin_result["changed"]:
        st.download_button("Unduh DOCX margin tervalidasi", margin_result["data"], file_name=Path(uploaded.name).stem + "_margin_formatted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

with st.expander("Uji Klasifikasi AI — Tanpa Mengubah DOCX"):
    st.caption("Maksimal 20 sampel: kandidat lolos, tertahan, dan bagian khusus. Sampel ini hanya untuk evaluasi dan tidak memberi izin formatting. Jika API key pernah terekspos, rotasi key sebelum digunakan.")
    if st.button("Siapkan sampel evaluasi"):
        st.session_state.pop("evaluation_result", None)
        st.session_state.pop("evaluation_import", None)
        if not valid_upload or 'rules' not in locals():
            st.error("Pilih DOCX valid dan pastikan aturan tersedia.")
        else:
            try:
                st.session_state.evaluation_sample = ai_beta.evaluation_stratified(uploaded.getvalue(), rules, degree, max_upload_mb * 1024 * 1024)
            except ValueError as exc:
                st.error(str(exc))
    eval_sample = st.session_state.get("evaluation_sample")
    if eval_sample:
        st.write("Pratinjau lokal sampel; potongan dan konteks akan dikirim bila disetujui:")
        st.dataframe(eval_sample["request"]["paragraphs"], hide_index=True)
        label_upload = st.file_uploader("Impor CSV label pembanding (opsional)", type=["csv"], key=f"eval_csv_{document_key}_{degree}")
        if st.button("Impor label CSV"):
            st.session_state.pop("evaluation_import", None)
            try:
                if label_upload is None:
                    raise ValueError("Pilih CSV label terlebih dahulu.")
                imported = ai_beta.import_evaluation_labels(label_upload.getvalue(), eval_sample)
                for identifier, item in imported.items():
                    st.session_state[f"eval_label_{document_key}_{degree}_{identifier}"] = item["label"]
                st.session_state.evaluation_import = imported
                st.success(f"{len(imported)} label diimpor untuk evaluasi; tidak memberi izin formatter.")
                st.warning("ID, BAB, dan kelompok cocok; CSV tanpa hash dokumen tidak membuktikan asal label. Periksa file sumber.")
            except ValueError as exc:
                st.error(str(exc))
        st.caption("Label pembanding opsional dapat diisi sebelum AI dijalankan; tersimpan hanya dalam sesi lokal.")
        for row in eval_sample["request"]["paragraphs"]:
            st.selectbox(f"Penilaian operator {row['id']}", ["PENDING", "teks_isi", "bagian_khusus", "tidak_pasti"], key=f"eval_label_{document_key}_{degree}_{row['id']}")
        labels = {row["id"]: st.session_state.get(f"eval_label_{document_key}_{degree}_{row['id']}", "PENDING") for row in eval_sample["request"]["paragraphs"]}
        imported = st.session_state.get("evaluation_import")
        if imported:
            counts = ai_beta.comparison_counts(labels, {key: value["prediction"] for key, value in imported.items()})
            st.write(f"Prediksi dalam CSV (belum diverifikasi): TP {counts.get('tp', 0)} | FP {counts.get('fp', 0)} | FN {counts.get('fn', 0)} | belum pasti {counts.get('unresolved', 0)}.")
        estimated_tokens, estimated_cost = ai_beta.evaluation_estimate(eval_sample, ai_tokens, beta_price_in, beta_price_out)
        st.write(f"Perkiraan input: {estimated_tokens} token; batas output: {ai_tokens}; biaya perkiraan: {estimated_cost:.6f}.")
        st.caption("Perkiraan bukan batas tagihan yang dijamin; harga harus sesuai model yang dipilih.")
        eval_consent = st.checkbox("Saya menyetujui pengiriman sampel evaluasi ke OpenAI tanpa memformat DOCX.", key=f"eval_consent_{document_key}_{degree}")
        eval_signature = (input_key, ai_model, ai_tokens, beta_price_in, beta_price_out, eval_consent)
        if st.session_state.get("evaluation_signature") != eval_signature:
            st.session_state.pop("evaluation_result", None)
            st.session_state.evaluation_signature = eval_signature
        if st.button("Kirim sampel evaluasi AI"):
            st.session_state.pop("evaluation_result", None)
            if not eval_consent:
                st.warning("Persetujuan pengiriman sampel diperlukan.")
            elif not eval_sample["selected"]:
                st.warning("Tidak ada kandidat untuk dievaluasi.")
            elif estimated_cost > beta_budget:
                st.warning("Perkiraan biaya melebihi anggaran dokumen.")
            else:
                try:
                    decisions, usage = ai_beta.request_classifications(eval_sample, ai_model, ai_tokens, include_reason=True)
                    st.session_state.evaluation_result = {"decisions": decisions, "usage": usage}
                except ai_planner.AnalysisError as exc:
                    st.error(str(exc))
                    show_ai_usage(exc.usage)
                except ValueError as exc:
                    st.error(str(exc))
                except Exception:
                    st.error("Evaluasi gagal; DOCX tidak diubah.")
        eval_result = st.session_state.get("evaluation_result")
        if eval_result and eval_consent:
            show_ai_usage(eval_result["usage"])
            usage = eval_result["usage"]
            if usage and usage.get("input_tokens") is not None and usage.get("output_tokens") is not None:
                cost = (usage["input_tokens"] * beta_price_in + usage["output_tokens"] * beta_price_out) / 1000000
                st.caption(f"Perkiraan biaya aktual berdasarkan token tersedia: {cost:.6f}.")
            st.dataframe(eval_result["decisions"], hide_index=True)
            st.caption("Perbandingan memakai label operator pada sampel ini, bukan ground truth otomatis.")
            for title, field in (("AI mentah", "ai_role"), ("Gabungan konservatif", "effective_role")):
                counts = ai_beta.comparison_counts(labels, {e["lokasi"]: e.get(field, "") for e in eval_result["decisions"]})
                tp, fp = counts.get("tp", 0), counts.get("fp", 0)
                precision = f"{tp / (tp + fp):.1%}" if tp + fp else "belum tersedia"
                st.write(f"{title}: TP {tp} | FP {fp} | FN {counts.get('fn', 0)} | belum terukur {counts.get('unresolved', 0)} | precision body {precision}.")

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
            with st.expander("Peta kandidat BAB dan section"):
                mapped = document_structure_map(uploaded.getvalue())
                st.caption("Batas kandidat bersifat diagnostik; hubungan caption dan objek tetap perlu review. Tidak mengaktifkan formatter.")
                st.write("Rentang BAB")
                st.dataframe(mapped["chapters"], hide_index=True)
                st.write("Section")
                st.dataframe(mapped["sections"], hide_index=True)
                st.write("Elemen dan kandidat hubungan objek")
                st.dataframe(mapped["elements"], hide_index=True)
                st.dataframe(mapped["caption_relations"], hide_index=True)
            scope = safe_format_scope(uploaded.getvalue(), rules, degree)
            scope_counts = Counter(item["keputusan"] for item in scope)
            st.write(f"Pratinjau cakupan eksperimental: auto_safe {scope_counts['auto_safe']} | needs_review {scope_counts['needs_review']} | protected {scope_counts['protected']} | Paragraf dengan usulan perubahan {sum(bool(item['aturan_berubah']) for item in scope)}")
            st.write(f"Paragraf eligible: {sum(any(c['eligible'] for c in item['rule_decisions']) for item in scope)} | Paragraf needs_change: {sum(any(c['needs_change'] is True for c in item['rule_decisions']) for item in scope)} | Paragraf safe_to_apply: {sum(any(c['safe_to_apply'] for c in item['rule_decisions']) for item in scope)}")
            st.caption("Dry-run eksperimental: eligible berarti layak diperiksa; needs_change berarti nilainya tidak sesuai; safe_to_apply menilai perubahan teknis per aturan, bukan izin menjalankan formatter. Nilai yang sudah sesuai tetap dapat dinilai aman. Pratinjau AI diperiksa secara terpisah dan tidak mengubah hasil cakupan ini.")
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

if valid_upload and 'rules' in locals():
    with st.expander("Pilot formatting terkontrol (lokal)"):
        st.caption("Pilih dan periksa setiap paragraf secara manual. Pilot tidak menggunakan keputusan AI; hanya salinan yang lolos validasi dapat diunduh.")
        if st.checkbox("Aktifkan pilot lokal", key=f"pilot_enabled_{document_key}_{degree}"):
            candidate_rows = [r for r in recognize_structure(uploaded.getvalue()) if r["jenis"] == "teks_isi" and r["lokasi"].startswith("paragraf:")]
            candidate_text = {int(r["lokasi"].split(":")[1]): r["teks"] for r in candidate_rows}
            chosen = st.multiselect("Paragraf teks isi yang telah diperiksa satu per satu", list(candidate_text), format_func=lambda i: f"Paragraf {i}: {candidate_text[i][:120]}", key=f"pilot_paragraphs_{document_key}_{degree}")
            choice_key = sha256(",".join(map(str, sorted(chosen))).encode()).hexdigest()
            pilot_confirmed = st.checkbox("Saya memastikan paragraf terpilih adalah teks isi utama dan aman untuk diperiksa.", key=f"pilot_confirm_{document_key}_{degree}_{choice_key}")
            pilot_signature = (document_key, degree, tuple(sorted(chosen)), pilot_confirmed)
            if st.session_state.get("pilot_signature") != pilot_signature:
                st.session_state.pop("pilot_plan", None)
                st.session_state.pop("pilot_result", None)
                st.session_state.pilot_signature = pilot_signature
            if st.button("Buat rencana pilot"):
                st.session_state.pop("pilot_result", None)
                if not chosen or not pilot_confirmed:
                    st.warning("Pilih dan konfirmasi paragraf terlebih dahulu.")
                else:
                    try:
                        st.session_state.pilot_plan = pilot.pilot_plan(uploaded.getvalue(), rules, degree, set(chosen))
                    except Exception:
                        st.session_state.pop("pilot_plan", None)
                        st.error("Rencana pilot gagal divalidasi; tidak ada file yang dihasilkan.")
            pilot_rows = st.session_state.get("pilot_plan")
            if pilot_rows is not None:
                summary = pilot.pilot_summary(pilot_rows)
                st.write(f"Sudah sesuai: {summary['known_compliant']} | Rencana perubahan: {summary['planned']} | Nilai awal tidak diketahui: {summary['unknown_value']} | Rencana normalisasi nilai tidak diketahui: {summary['unknown_to_normalize']} | Dilewati: {summary['rejected']}")
                st.caption("Ringkasan menghitung pasangan kandidat–aturan, termasuk kandidat yang belum dikonfirmasi; nilai format terukur bukan bukti kepatuhan konteks. Kategori dapat saling tumpang tindih.")
                st.dataframe(pilot_rows, hide_index=True)
                if summary["planned"] and st.button("Terapkan pilot pada salinan"):
                    st.session_state.pop("pilot_result", None)
                    try:
                        result, checked_plan = pilot.format_pilot(uploaded.getvalue(), rules, degree, set(chosen))
                        st.session_state.pilot_result = result
                        st.session_state.pilot_plan = checked_plan
                    except Exception:
                        st.error("Validasi pilot gagal; file hasil tidak tersedia.")
                if st.session_state.get("pilot_result") is not None:
                    st.success(f"Validasi berhasil; {summary['planned']} perubahan diterapkan pada salinan.")
                    st.download_button("Unduh DOCX pilot tervalidasi", st.session_state.pilot_result, file_name=Path(uploaded.name).stem + "_pilot_formatted.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
