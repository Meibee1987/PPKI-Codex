# Task Plan — kerjakan satu per satu dengan Codex

**Aturan:** jangan lompat ke task berikut sampai kriteria selesai dan tes task saat ini jelas. Prioritas `P0` dulu. Untuk setiap task, Codex harus menjelaskan file berubah, tes, serta batasan.

## T0 — Scaffold minimal [P0]
**Buat:** `app.py`, `requirements.txt`, `README.md` praktis, `.gitignore`, struktur folder `core/`, `tests/` hanya bila diperlukan. UI Streamlit: judul, upload DOCX, pilih S1/S2/S3, tombol Audit yang belum berjalan dengan pesan jujur.

**Selesai jika:** aplikasi Streamlit dapat dibuka lokal; tidak ada API key, database, atau request jaringan; file asli tidak tersimpan sembarangan.

## T1 — Rule loader + filter [P0]
**Buat:** baca `rules/ppki_rules_all.json`, validasi minimal field wajib, deduplikasi/cek unique `rule_code`, filter `applies_to` secara eksplisit. Tampilkan jumlah aturan applicable/unsupported.

**Selesai jika:** tes untuk S1/S2/S3, `rule_code` duplikat, JSON rusak, dan tag applicability yang tidak dikenal lulus. Tidak semua 317 dianggap applicable secara otomatis.

## T2 — Audit 6 properti halaman + font/body [P0, selesai untuk cakupan MVP terbatas]
**Buat:** validator awal untuk A4 dan empat margin (**LAY-003, LAY-008, LAY-009, LAY-010, LAY-011**); tambah satu validator body yang aman (**LAY-005**) saat klasifikasi body sudah cukup jelas. Tampilkan findings dengan `rule_code`, actual, expected, lokasi, status, dan alasan unsupported.

**Selesai jika:** nilai A4/margin sesuai dataset PPKI; paragraf ambigu tidak salah diklasifikasikan; tes unit berhasil.

T2 mendukung lima validator section dan satu validator font untuk style yang dipilih
dan cakupannya dikonfirmasi operator. Font tema, teks non-ASCII, struktur kompleks,
nilai yang tidak diketahui, dan paragraf di luar style terpilih perlu review manual.

## T3 — Audit dan format 3 properti body [P0, selesai untuk cakupan MVP terbatas]
**Buat:** tambah audit line spacing 1.0 (**LAY-017**), first line indent 1 cm (**LAY-018**), dan alignment justified (**LAY-019**). Implementasikan daftar perubahan yang diusulkan (dry-run). Jangan ubah paragraf khusus/field/tabel.

**Selesai jika:** 9 kandidat aturan memiliki audit yang dapat diuji; fixture body bisa dibedakan dari heading/caption/abstrak; hal yang ambigu di-skip.

T3 mengaudit tiga properti pada style isi yang dikonfirmasi operator dan menampilkan
usulan dry-run untuk ketidaksesuaian yang terbukti. Bagian di luar cakupan, nilai
tidak eksplisit, daftar, dan struktur kompleks tetap memerlukan review manual.

## T4 — Terapkan perbaikan aman + ekspor [P0]
**Buat:** tombol **Terapkan perbaikan aman**, formatter untuk 9 kandidat yang lolos audit/tes, simpan DOCX baru, audit ulang, report JSON dan CSV, tombol unduh. Tidak perlu database histori.

**Selesai jika:** DOCX asli tidak berubah, file hasil dapat dibuka di Word, aturan yang diklaim fixed lolos audit ulang, action yang gagal tercatat sebagai `needs_review`/`error`.

T4A selesai untuk tiga aturan Auto `LAY-017`, `LAY-018`, dan `LAY-019`: hasil
disimpan sebagai salinan, diperiksa integritasnya, dan diaudit ulang.

T4B selesai untuk `LAY-003` dan `LAY-008` sampai `LAY-011` pada section yang
aman, dengan audit ulang dan laporan perubahan CSV. Section landscape/berkolom
dilewati. Laporan JSON lengkap masih belum dikerjakan; karena itu T4
keseluruhan belum selesai.

## T5 — Uji dokumen nyata dan hardening dasar [P0]
**Buat:** tests untuk ≥5 fixture DOCX: normal, multi-section, tabel+gambar, heading campur, dan paragraf dengan runs/hyperlink/field. Tambah validasi file rusak dan ukuran maksimum.

**Selesai jika:** suite pengujian lulus; teks/tabel/gambar/relasi penting tidak hilang; docx rusak ditolak tanpa crash; daftar keterbatasan tersaji di UI.

Pengujian tiga fixture S1/S2/S3 dan hasil audit tercatat di [laporan T5](T5_REPORT.md).
Pemilik menerima tiga fixture untuk cakupan MVP, tanpa menambah dua fixture hanya
untuk memenuhi angka lima. T5 belum dinyatakan selesai: hasil pemeriksaan manual
Word belum diterima dan validasi batas ukuran file belum diimplementasikan atau diuji.

## T6 — Safe Font Formatter [selesai untuk cakupan MVP terbatas]

`PPKI-LAY-005` dapat diperbaiki pada style isi yang dipilih dan dikonfirmasi,
hanya jika setiap run teks dalam paragraf aman dan font serta ukurannya diketahui.
Font simbol, theme ambigu, struktur kompleks, dan nilai tidak diketahui tetap
perlu review. T5 masih menunggu pemeriksaan akhir Microsoft Word dan validasi
batas ukuran file; perubahan ini tidak menyatakan T5 selesai.

## Heading dan abstrak [P1, setelah T5; belum dikerjakan]
**Buat:** pilih subset rules `HDG` dan `ABS` yang benar-benar dapat ditangani, klasifikasi konservatif, konfirmasi untuk kasus ambigu. Tambah per aturan beserta tes.

**Selesai jika:** setiap handler baru punya test, tidak mengubah isi tulisan, dan tidak mengklaim support untuk aturan tanpa handler.

T7A (audit heading read-only) selesai untuk cakupan terbatas: `PPKI-HDG-003`,
`004`, dan `006` pada Heading 1 yang dikonfirmasi dan memuat nomor BAB serta
judul dalam satu paragraf sederhana. Heading 2 dan 3 baru ditampilkan sebagai
kandidat; aturan lainnya tetap belum didukung atau perlu review. Formatter
heading dan abstrak belum dibuat pada tahap T7A. T5 masih menunggu pemeriksaan akhir Word.

T7B selesai untuk cakupan BAB terbatas: `PPKI-HDG-003`, `004`, dan `006`
yang Auto dapat diperbaiki pada kandidat yang dikonfirmasi dan aman; lihat
[laporan T7B](T7B_REPORT.md). Penomoran, subbab, dan struktur ambigu belum didukung.

## T7 — AI opsional [P2, hanya kalau terbukti dibutuhkan]
Satu pemanggilan API model yang **konfigurasinya tidak hardcode** untuk usulan klasifikasi paragraf ambigu, **opt-in per dokumen**. Tidak boleh mengirim file penuh otomatis. Hasil AI berupa usulan yang divalidasi dan disetujui sebelum menyentuh DOCX.

**Selesai jika:** mode tanpa AI tetap berjalan sama baiknya, tidak ada data keluar tanpa persetujuan, biaya dan gagal API ditangani jelas.

## T8A — Diagnostik penomoran halaman read-only [cakupan terbatas]

Struktur section, format/restart eksplisit, referensi header/footer, dan instruksi
PAGE dapat ditampilkan untuk review. `PPKI-LAY-023`, `PPKI-LAY-024`, dan aturan
penomoran lain yang berkunci `manual.not-implemented` tetap `not_supported`;
tidak ada klaim lulus/gagal maupun formatter nomor halaman. Penomoran hasil
render dan cakupan bagian dokumen perlu pemeriksaan manual di Word.

## Definisi Done setiap task
- [ ] Perubahan kode sesuai lingkup task dan tidak mengubah aturan sumber.
- [ ] Tes yang relevan ada dan dijalankan; hasil dilaporkan.
- [ ] Tidak ada penambahan arsitektur yang tidak diperlukan.
- [ ] Kesalahan/fitur yang belum didukung dilaporkan jujur.
- [ ] Untuk formatter, input tetap utuh dan output di-audit ulang.

## Prompt untuk setiap task berikut
```text
Baca AGENTS.md dan docs/ terkait. Kerjakan HANYA T<n> dari docs/TASKS.md.
Jangan mengerjakan task lain, menambah dependensi, API/cloud, database, atau refactor besar.
Jalankan tests yang relevan, lalu laporkan file berubah, hasil tes, dan risiko.
```
