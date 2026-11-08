# Laporan T7B — Safe Heading BAB Formatter

Snapshot PPKI menetapkan `fix_mode=Auto` dan `applies_to=Semua` untuk
`PPKI-HDG-003` (kapitalisasi judul), `PPKI-HDG-004` (bold judul), dan
`PPKI-HDG-006` (perataan tengah). Jika metadata berubah menjadi `Manual` atau
`Confirm`, implementasi ini melewatkan aturan; persetujuan khusus untuk
`Confirm` belum disediakan.

Formatter memproses kandidat BAB yang dikonfirmasi, memiliki temuan `fail`,
dan lulus pemeriksaan struktur. Opsi rencana khusus heading memungkinkan
operator melewati perbaikan halaman dan teks isi. DOCX hasil divalidasi terhadap
paket asli, diaudit ulang, dan disediakan bersama laporan CSV. Nomor BAB dan
tanda titik tidak diubah.

Pada Dummy Master dengan ketiga kandidat dikonfirmasi dan rencana khusus heading:

| Rule / lokasi | Sebelum | Sesudah | Status |
|---|---|---|---|
| HDG-003 / paragraf 60 | Metode Penelitian. | METODE PENELITIAN. | pass |
| HDG-004 / paragraf 60 | Ada run tidak tebal | Semua run tebal | pass |
| HDG-006 / paragraf 60 | LEFT (0) | CENTER (1) | pass |

Hasil: **3 perubahan heading diterapkan, 0 temuan heading dilewati, 0 gagal**.
Ada **118 temuan non-heading dilewati** dari rencana khusus heading, termasuk
temuan yang perlu review; jumlah ini bukan jumlah seluruh aturan dalam snapshot.
BAB I dan III, kandidat non-BAB, section, tabel, gambar, bagian paket lain, dan
paragraf di luar target tetap terjaga dalam regresi. Hasil terbuka kembali dan
formatter kedua tidak menghasilkan perubahan tambahan.

`python -m pytest -q`: **97 passed**, termasuk Streamlit AppTest untuk konfirmasi,
rencana, audit ulang, dan unduhan. File berubah: `core/audit.py`,
`core/formatter.py`, `app.py`, `tests/test_heading_audit.py`,
`tests/test_heading_formatter.py`, `README.md`, `docs/TASKS.md`, dan laporan ini.

Judul non-ASCII, numbering otomatis, field, hyperlink, dan struktur run ambigu
tidak diperbaiki otomatis. Pengujian tidak menjamin keamanan seluruh konstruksi
Word. Pemeriksaan visual Microsoft Word dan hasil T5 tetap **PENDING**, termasuk
review akhir tata letak setelah perubahan kapitalisasi dan perataan BAB.
