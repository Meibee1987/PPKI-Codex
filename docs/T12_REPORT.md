# T12 — Penyempurnaan UI dan laporan audit

## Perubahan

Tampilan dibagi menjadi upload/jenjang, audit/ringkasan, detail dan diagnostik,
serta rencana perbaikan/unduhan. Ringkasan menampilkan nama status `pass`,
`fail`, `needs_review` dan `not_supported`, beserta penjelasannya; diagnostik
kandidat dijelaskan bukan bukti kepatuhan. Konfirmasi style isi, BAB dan mode
Heading saja tetap terpisah. Alasan dilewati dan jumlah aturan per domain
tersedia di expander. Tombol tindakan bernama **Terapkan Perbaikan Otomatis**;
DOCX dan CSV tetap tersedia setelah validasi sukses. Ringkasan sebelum tetap
terlihat setelah tindakan perbaikan.

Perhitungan ringkasan, validator dan formatter tidak diubah. Ringkasan dihitung
per aturan menggunakan prioritas status yang sudah ada, bukan jumlah baris
temuan individual. Detail diagnostik ditampilkan ketika audit dijalankan;
jalankan audit kembali jika perlu melihatnya setelah interaksi perbaikan.

## Pengujian

`.\.venv\Scripts\python.exe -m pytest -q`: **114 passed**, termasuk AppTest
startup, semua diagnostik dan alur Dummy Master mode Heading saja. Tes T12
membandingkan ringkasan UI dengan hasil audit langsung, memeriksa tiga perubahan
heading, audit ulang pass, kedua unduhan dan byte input yang tidak berubah.

File berubah: [app.py](../app.py), [test_ui_t12.py](../tests/test_ui_t12.py),
[test_formatter.py](../tests/test_formatter.py),
[test_heading_audit.py](../tests/test_heading_audit.py),
[test_heading_formatter.py](../tests/test_heading_formatter.py),
[README.md](../README.md), [TASKS.md](TASKS.md), dan laporan ini.

## Batasan

Perbaikan hanya mencakup rencana Auto yang didukung dan lolos validasi;
diagnostik serta temuan review memerlukan pemeriksaan operator. Pemeriksaan
visual akhir Microsoft Word tetap PENDING.
