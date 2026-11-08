# PPKI Academic Formatter — Codex Starter Pack

## Menjalankan aplikasi T0

Gunakan Python 3.12 atau lebih baru. Di PowerShell, dari folder proyek:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Buka alamat lokal yang ditampilkan Streamlit. Untuk berhenti, tekan Ctrl+C di terminal.
Instalasi dependensi membutuhkan akses ke sumber paket; aplikasi sendiri tidak memakai API atau database.

Audit read-only mendukung sembilan validator: `PPKI-LAY-003`, `005`, `008`, `009`,
`010`, `011`, `017`, `018`, dan `019`. Untuk properti teks isi, pilih style yang ditemukan dalam dokumen, periksa
semua kandidat di Word dan konfirmasi cakupannya untuk setiap audit. Hasil font
hanya mencakup style terpilih; paragraf lain tetap perlu pemeriksaan manual.
Font tema, karakter non-ASCII, struktur kompleks, atau nilai yang tidak diketahui
memerlukan review. Spasi tinggi tetap/minimum, daftar, dan properti yang tidak
eksplisit juga perlu review. Usulan perubahan hanya dry-run dan belum diterapkan;
aturan lain tanpa validator memerlukan pemeriksaan manual.
Dokumen unggahan dibaca di memori dan dokumen asli tidak diubah.
T4A dapat menerapkan tiga aturan Auto `LAY-017`, `LAY-018`, dan `LAY-019`
yang gagal pada paragraf terkonfirmasi. Tinjau rencana, lalu pilih Terapkan
Perbaikan; hasil hanya tersedia setelah pemeriksaan integritas dan audit ulang.
Aturan Manual dan Confirm dilewati pada tahap ini. Struktur yang tidak dikenali
memerlukan review dan hasil tetap perlu diperiksa di Microsoft Word.
Formatter font `LAY-005` dapat memperbaiki run yang diketahui pada paragraf
yang style dan cakupannya telah dikonfirmasi. Jika satu run menggunakan font
simbol, theme ambigu, atau properti tak diketahui, seluruh paragraf dilewati
untuk review. Style global dan properti seperti bold dan italic tidak diubah.
T4B juga mendukung perbaikan halaman per section untuk `LAY-003` dan
`LAY-008` sampai `LAY-011`, dengan laporan perubahan CSV. Section landscape,
berkolom, atau tidak pasti dilewati untuk review. Audit dan format paragraf
tetap memerlukan pemilihan style dan konfirmasi cakupan.

Audit heading read-only menampilkan kandidat Heading 1 yang berpola BAB. Operator
mengonfirmasi setiap kandidat secara terpisah; kandidat lain tetap perlu review.
Aturan `PPKI-HDG-003`, `004`, dan `006` diperiksa terbatas pada paragraf teks
sederhana yang memuat nomor BAB dan judul bersama. Bold yang tidak eksplisit,
penomoran otomatis, dan konteks yang ambigu perlu review. Formatter BAB terbatas
dapat memperbaiki `HDG-003`, `004`, dan `006` yang Auto pada kandidat yang
dikonfirmasi dan aman. Pilih opsi rencana khusus heading untuk menjaga halaman dan
teks isi dari perbaikan lain. Aturan heading lainnya belum didukung.

Diagnostik penomoran halaman menampilkan format dan restart yang eksplisit,
referensi header/footer, serta instruksi PAGE yang terdeteksi per section. Ini
tidak menentukan nomor halaman hasil render atau kepatuhan: `PPKI-LAY-023` dan
`PPKI-LAY-024` tetap belum didukung karena kunci validasinya `manual.not-implemented`.
Hasil diagnostik memerlukan pemeriksaan di Word; tidak ada formatter nomor halaman.

Hasil pengujian tiga dokumen representatif dan keterbatasan review visual tersedia
di [laporan T5](docs/T5_REPORT.md). Pemilik menerima tiga fixture untuk cakupan
MVP; hasil pemeriksaan manual dan validasi batas ukuran file masih diperlukan.
Ringkasan aturan dibaca dari `rules/ppki_rules_all.json`. Metadata `is_implemented`
tidak berarti validator tersedia. Label penerapan yang belum dipetakan perlu review.

Untuk menjalankan tes loader di lingkungan yang sama:

```powershell
.\.venv\Scripts\python -m pip install pytest
.\.venv\Scripts\python -m pytest -q
```

Dokumentasi siap pakai untuk membangun **MVP lokal** pemformat skripsi (S1), tesis (S2), dan disertasi (S3). Digunakan sendiri oleh penyedia jasa, sekitar **20–30 dokumen/bulan**.

## Mulai dari sini

1. Buka folder ini sebagai **workspace/repository** di Codex (bukan menyalin prompt panjang saja).
2. Minta Codex membaca `AGENTS.md` dan `docs/PRD.md`, `docs/ERD.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`.
3. Mulai dari **T0** di `docs/TASKS.md`. Kerjakan **satu task per giliran**; review hasil dan tesnya sebelum melanjutkan.
4. Gunakan `rules/ppki_rules_all.json` sebagai snapshot resmi dataset; `rules/ppki_rules_mvp25.json` untuk daftar kandidat aturan yang pernah ditandai implemented.
5. Ketika aplikasi sudah jadi, jalankan di laptop lewat Streamlit. Gunakan **DOCX contoh tanpa data pribadi** untuk pengujian.

## Prompt pertama untuk Codex

```text
Baca AGENTS.md dan semua file dalam docs/ terlebih dahulu.
Kita membangun PPKI Academic Formatter untuk penggunaan pribadi 20–30 DOCX per bulan.
Gunakan rules/*.json yang tersedia; jangan membuat ulang rules PPKI.
Kerjakan HANYA Task T0 dari docs/TASKS.md.
Jangan menambah database baru, hosting, Docker, framework agent, atau OpenAI API pada tahap ini.
Setelah selesai, jalankan pengujian yang relevan dan laporkan: file yang diubah, hasil tes,
serta batasan yang masih ada. Jangan lanjut ke task lain tanpa instruksi.
```

## Urutan baca

- `docs/PRD.md`: **apa** yang perlu jadi dan apa yang tidak.
- `docs/ERD.md`: **data** apa yang sudah ada (bukan desain database baru).
- `docs/ARCHITECTURE.md`: **cara** membangunnya secara sederhana.
- `docs/TASKS.md`: **urutan langkah**, tiap langkah punya kriteria selesai.
- `AGENTS.md`: **aturan kerja Codex** di repository.

## Keputusan yang sengaja sederhana

- Satu aplikasi **Python + Streamlit + python-docx**.
- **Tanpa login**, tanpa frontend/backend terpisah, tanpa server online.
- **Tanpa database lokal**: cukup JSON rules dan file laporan per pekerjaan.
- **Tanpa API AI pada MVP pertama**; AI kelak hanya membantu mengenali struktur yang ambigu.
- **Tanpa sinkronisasi Supabase langsung** pada MVP. Update rules dilakukan dengan ekspor ulang JSON secara sengaja.
- Berkas DOCX asli tidak diubah. Semua pemformatan menghasilkan salinan baru.

> Penting: dataset rules yang dilampirkan adalah hasil ekspor, bukan bukti bahwa semua rules bisa dieksekusi. `is_implemented=true` hanyalah metadata. Validator dan formatter harus benar-benar memiliki implementasi serta tes.
