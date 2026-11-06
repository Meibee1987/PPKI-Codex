# Laporan T5 — tiga fixture representatif

Pengujian menggunakan snapshot aturan lokal dan jenjang masing-masing. Tidak ada
style isi yang dikonfirmasi: style Body Text juga digunakan pada abstrak,
ringkasan, atau lampiran. Oleh karena itu hanya perbaikan halaman Auto yang
aman diterapkan; properti paragraf tetap perlu review. Dokumen asli tidak ditulis.

| Dokumen | Audit dan buka ulang | Perbaikan tervalidasi | Dilewati (temuan halaman) | Gagal | Integritas yang diuji |
|---|---|---:|---:|---:|---|
| [S1](../tests/fixtures/PPKI_T4B_01_Skripsi_S1_Dasar.docx) | PASS | 5 | 0 | 0 | PASS |
| [S2](../tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx) | PASS | 4 | 0 | 0 | PASS |
| [S3](../tests/fixtures/PPKI_T4B_03_Disertasi_S3_MultiSection.docx) | PASS | 6 | 5 | 0 | PASS |

Status pemeriksaan yang diberikan pemilik:

| Dokumen | Status teknis | Tindak lanjut |
|---|---|---|
| S1 | PASS | Pemeriksaan akhir Microsoft Word: **PENDING** |
| S2 | PASS teknis | Review halaman 4; pemeriksaan akhir Microsoft Word: **PENDING** |
| S3 | PASS teknis | Review akhir Microsoft Word: **PENDING** |

Menurut hasil pemeriksaan S3 yang diberikan pemilik, enam perbaikan berstatus
PASS dan lima temuan pada section landscape sengaja dilewati. DOCX hasil tetap
memiliki tiga section dan empat halaman. Seluruh teks, tabel, gambar, header,
dan footer terjaga dalam pemeriksaan struktural dan render.

Perubahan yang diklaim berhasil lulus audit ulang. Lima temuan halaman S3 yang
dilewati berada pada section 3 landscape; section tersebut tetap utuh. Perbaikan
ulang tidak menghasilkan perubahan tambahan. Integritas mencakup teks paragraf,
jumlah tabel dan gambar inline, struktur dokumen selain properti yang diizinkan,
serta isi byte semua bagian paket lainnya termasuk header, footer, relasi dan
gambar. S2 memiliki satu hyperlink; jumlah dan struktur dokumen yang tidak masuk
properti yang diizinkan terjaga. S1 dan S3 tidak memiliki hyperlink dalam badan
dokumen sehingga tidak menguji hyperlink pada kedua fixture tersebut.

Ukuran berikut dalam cm; margin dalam urutan kiri, kanan, atas, bawah.

| Dokumen / section | Kertas sebelum → sesudah | Margin sebelum → sesudah |
|---|---|---|
| S1 / 1 | 21,59 × 27,94 → 21 × 29,7 | 3 / 2,5 / 2,5 / 2,5 → 4 / 3 / 3 / 3 |
| S2 / 1 | 21 × 29,7 → 21 × 29,7 | 2,5 / 2 / 2,5 / 3,5 → 4 / 3 / 3 / 3 |
| S3 / 1 | 21 × 29,7 → 21 × 29,7 | 3,2 / 3 / 2 / 3 → 4 / 3 / 3 / 3 |
| S3 / 2 | 21,59 × 27,94 → 21 × 29,7 | 3,5 / 2 / 3 / 2,5 → 4 / 3 / 3 / 3 |
| S3 / 3 | 29,7 × 21 → 29,7 × 21 | 2 / 2 / 2 / 2 → 2 / 2 / 2 / 2 |

`python -m pytest -q`: **58 passed** pada pengujian yang dicatat sebelumnya.
LibreOffice tidak ditemukan pada PATH atau lokasi instalasi Windows standar
yang diperiksa dalam sesi pengujian tersebut; render S3 yang disebut di atas
merupakan hasil pemeriksaan yang diberikan pemilik. Pemeriksaan akhir Microsoft
Word masih **PENDING**. Pengujian otomatis tidak membuktikan seluruh konstruksi
Word aman.

Pemilik proyek menetapkan tiga fixture S1/S2/S3 sebagai cakupan pengujian MVP;
dua fixture tambahan tidak diwajibkan hanya untuk mencapai jumlah lima. Validasi
batas ukuran file yang tercantum dalam rencana T5 belum diimplementasikan atau
diuji. T5 belum dinyatakan selesai sampai pemeriksaan wajib dapat diverifikasi.
