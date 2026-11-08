# T11 — Audit struktur dokumen read-only

## Aturan dan cakupan

Inventaris luas mencakup 64 aturan: 25 STR, 16 CVR, 19 ABS, dan empat CNT
(PPKI-CNT-003, 014, 021, 033) yang terjaring kata struktur atau urutan.
Sebagian CNT menyangkut urutan internal pembahasan, sehingga perlu review
relevansinya untuk urutan bagian utama. Sebanyak 58 memiliki validation_key
`manual.not-implemented`; enam lainnya memiliki key khusus abstrak/ringkasan
yang belum memiliki handler pada audit ini. **Tidak ada validator kepatuhan
struktur baru yang didukung.** Dari 64 aturan, fix_mode adalah 17 Auto,
36 Confirm dan 11 Manual; tidak ada formatter struktur yang dijalankan.

Inventaris UI menampilkan ketentuan resmi, target, validation_key, applies_to,
fix_mode, severity dan sumber dari JSON. Jenjang dipetakan menggunakan filter
yang ada; konteks lain tetap ditampilkan untuk review. Contohnya STR-017 hanya
diterapkan pada tesis/disertasi oleh filter. Tidak ada daftar wajib atau urutan
yang diasumsikan sama untuk semua jenjang. STR-001 menetapkan urutan bagian
awal, tetapi `manual.not-implemented` sehingga tidak diberi pass/fail.

## Dummy Master

Ditemukan 16 kandidat: satu Title, pernyataan, abstrak, abstract, ringkasan,
summary, daftar isi, daftar tabel, daftar gambar, tiga BAB, daftar pustaka,
dua lampiran, serta satu Heading 1 lain yang belum dikenali. BAB I, II, III
berada pada paragraf 40, 60, 75; daftar pustaka pada 97 dan lampiran pada 90
dan 103. Urutan aktual dapat diperiksa pada tabel; seluruh kandidat berstatus
`needs_review`, termasuk lampiran sebelum daftar pustaka. Tidak ada klaim
bahwa daftar bagian telah lengkap atau urutannya sesuai.

## Pengujian

`.\.venv\Scripts\python.exe -m pytest -q`: **113 passed**, termasuk AppTest
S1/S2/S3, regresi fitur terdahulu, pengujian kandidat hilang/duplikat/urutan
ambigu dan pemeriksaan bahwa byte fixture asli tidak berubah.

File berubah: [audit.py](../core/audit.py), [app.py](../app.py),
[test_document_structure.py](../tests/test_document_structure.py),
[README.md](../README.md), [TASKS.md](TASKS.md) dan laporan ini.

## Keterbatasan

Pencarian menggunakan paragraf body dengan style Title atau Heading 1 dan
label eksplisit; Title hanya kandidat halaman judul, bukan bukti sampul atau
halaman judul. Heading kustom, halaman tanpa heading, field, tabel, kotak teks,
header/footer dan bagian yang terpecah dapat terlewat atau memerlukan review.
Bagian tanpa kandidat tidak otomatis hilang atau wajib. Status identitas dan
urutan selalu `needs_review`, bukan penilaian aturan. Pemeriksaan visual akhir
Microsoft Word masih PENDING.
