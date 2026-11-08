# PPKI Academic Formatter — MVP v1.0 Release Candidate

Status **RELEASE CANDIDATE**, belum siap untuk penggunaan dokumen pelanggan:
acceptance dokumen nyata dan pemeriksaan visual akhir Microsoft Word masih
PENDING. Lihat [laporan rilis](docs/T15_RELEASE_REPORT.md),
[kemampuan](docs/MVP_CAPABILITIES.md), [keterbatasan](docs/KNOWN_LIMITATIONS.md),
dan [panduan pengguna](docs/USER_GUIDE.md).

## Menjalankan aplikasi

Gunakan Python 3.12 atau lebih baru. Di PowerShell, dari folder proyek:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Buka alamat lokal yang ditampilkan Streamlit. Untuk berhenti, tekan Ctrl+C di terminal.
Instalasi dependensi membutuhkan akses ke sumber paket; aplikasi sendiri tidak memakai API atau database.

Audit read-only mendukung sembilan validator layout: `PPKI-LAY-003`, `005`, `008`, `009`,
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
Perbaikan Otomatis; hasil hanya tersedia setelah pemeriksaan integritas dan audit ulang.
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

Bagian **Audit Tabel, Gambar, dan Caption** menginventarisasi objek body, kandidat
caption berstyle yang dikenali, dan dugaan hubungan berdekatan. Operator dapat
mengonfirmasi dugaan tersebut, tetapi hasilnya tetap perlu review: semua aturan
terkait yang ditemukan berkunci `manual.not-implemented` dan belum didukung.
Lihat [laporan T9A](docs/T9A_REPORT.md) untuk cakupan dan keterbatasannya.

T10A menampilkan diagnostik read-only kandidat sitasi dan daftar pustaka tanpa
memerlukan konfirmasi style isi. Kecocokan penulis/tahun adalah kemungkinan,
bukan bukti kepatuhan; periksa kasus ambigu dan referensi yang belum ditemukan
secara manual. Aturan manual tetap belum memiliki validator kepatuhan. Rincian
dan hasil Dummy Master tersedia di [laporan T10A](docs/T10A_REPORT.md).

T11 menampilkan urutan kandidat bagian dari style Title dan Heading 1 secara
read-only. Identitas, bagian yang belum ditemukan dan urutan tetap perlu review;
inventaris ini bukan validasi kepatuhan. Lihat [laporan T11](docs/T11_REPORT.md).

Tampilan T12 memisahkan upload, audit dan ringkasan, detail diagnostik, serta
rencana perbaikan dan unduhan. Alasan perubahan yang dilewati tersedia dalam
expander. Lihat [laporan T12](docs/T12_REPORT.md).

Hasil acceptance teknis empat fixture tersedia di [laporan T13](docs/T13_REPORT.md).
Pemeriksaan Word dan dokumen nyata masih menunggu operator; gunakan
[checklist T13](docs/T13_WORD_CHECKLIST.md).

Upload DOCX dibatasi 20 MiB secara default. Untuk mengubah batas input,
tetapkan variabel lingkungan `PPKI_MAX_UPLOAD_MB` sebagai bilangan bulat
positif sebelum menjalankan aplikasi; batas jumlah dan dekompresi ZIP tetap
berlaku. Rincian dan keterbatasan ada di [laporan T14](docs/T14_REPORT.md).

Hasil pengujian tiga dokumen representatif dan keterbatasan review visual tersedia
di [laporan T5](docs/T5_REPORT.md). Pemilik menerima tiga fixture untuk cakupan
MVP; pemeriksaan manual masih diperlukan. Batas ukuran input telah diuji di T14.
Ringkasan aturan dibaca dari `rules/ppki_rules_all.json`. Metadata `is_implemented`
tidak berarti validator tersedia. Label penerapan yang belum dipetakan perlu review.

Untuk menjalankan tes loader di lingkungan yang sama:

```powershell
.\.venv\Scripts\python -m pip install pytest
.\.venv\Scripts\python -m pytest -q
```

MVP lokal ini ditujukan untuk satu operator pemformat skripsi, tesis dan
disertasi sekitar 20–30 dokumen per bulan setelah acceptance selesai.

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
