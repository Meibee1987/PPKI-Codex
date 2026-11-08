# T13 — Acceptance testing

## Hasil empat fixture

Mode umum menggunakan jenjang masing-masing, tanpa mengonfirmasi style isi
atau kandidat BAB. Angka status adalah jumlah **aturan** pada ringkasan audit,
dalam urutan pass / fail / needs_review / not_supported; angka dilewati adalah
jumlah temuan, bukan aturan unik. Setiap perubahan yang diterapkan lulus audit
ulang pada rule dan lokasi tersebut. File asli tidak ditulis.

| Fixture | Jenjang | Sebelum | Sesudah | Diterapkan | Dilewati | Gagal tindakan | Hasil teknis |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Dummy Master | S1 | 0 / 5 / 46 / 255 | 0 / 5 / 46 / 255 | 9 | 118 | 0 | PASS setelah perbaikan bug |
| Skripsi dasar | S1 | 0 / 5 / 46 / 255 | 5 / 0 / 46 / 255 | 5 | 26 | 0 | PASS |
| Tesis tabel/gambar | S2 | 1 / 4 / 46 / 248 | 5 / 0 / 46 / 248 | 4 | 42 | 0 | PASS |
| Disertasi multisection | S3 | 0 / 5 / 46 / 249 | 0 / 5 / 46 / 249 | 6 | 41 | 0 | PASS |

Pada Master section 5 dan S3 section 3, lima temuan halaman tetap fail karena
landscape dilewati dengan alasan eksplisit. Angka status per aturan tetap fail
meskipun seluruh lokasi yang benar-benar diperbaiki pass. Temuan lain yang
dilewati meliputi konteks belum dikonfirmasi, perlu review dan tidak didukung.

Mode Heading saja diuji terpisah pada Master: BAB II menghasilkan tiga
perubahan HDG-003/004/006 yang pass; BAB I/III dan section tetap utuh. Tes
idempotensi mode ini dan empat mode umum tidak menemukan perubahan tambahan.

## Integritas dan cakupan

Hasil dibuka kembali dengan python-docx. Tes membandingkan teks dan XML tabel,
bagian paket di luar `word/document.xml` secara byte, serta sumber asli. Selain
itu validasi formatter membandingkan struktur XML utama di luar properti target.
Master mencakup sel gabungan, gambar grafik sebagai gambar, hyperlink, field,
persamaan, footnote, header/footer dan field PAGE; bagian footnote dan footer
tetap identik. S2 juga mencakup hyperlink dan gambar. Bagian yang tidak ada di
suatu fixture tidak diuji pada fixture itu; tidak ada grafik Word native pada
keempat fixture ini. Integritas struktur bukan bukti tata letak visual atau
jaminan bagi semua konstruksi Word.

AppTest melakukan simulasi upload, audit, rencana, tindakan, audit ulang dan
memastikan tombol unduh DOCX/CSV tersedia; bytes output dibuka dan diuji di
memori. Pengunduhan browser secara manual tidak diuji. Konfirmasi BAB dan mode
Heading saja diuji dalam AppTest regresi tersendiri.

## Masalah yang ditemukan dan diperbaiki

Pada mode umum Dummy Master, serialisasi python-docx mengubah
`[Content_Types].xml`; validasi menolak hasil dan UI tidak menyediakan unduhan.
Tes reproduksi acceptance gagal sebelum perbaikan. Formatter kini menggunakan
mekanisme paket asli yang sudah dipakai mode Heading untuk semua mode, mengganti
hanya XML dokumen utama; validasi struktur dan audit ulang tetap wajib. Empat
fixture dan regresi lulus setelah perubahan.

## Pengujian dan status

`.\.venv\Scripts\python.exe -m pytest -q`: **118 passed, 0 failed**, termasuk
empat AppTest acceptance baru dan tes Heading saja. Pemeriksaan visual
Microsoft Word belum dilakukan oleh sesi ini: **PENDING**, lihat
[checklist](T13_WORD_CHECKLIST.md). Pengujian dokumen nyata anonim juga
**PENDING** karena tidak tersedia di fixture. T13 **belum siap ditutup** sampai
kedua pemeriksaan tersebut diterima; hasil teknis tidak menjamin keamanan semua
jenis dokumen Word. Review halaman 4 S2 dan validasi batas ukuran file T5 tetap
terbuka.

File berubah: [formatter.py](../core/formatter.py),
[test_t13_acceptance.py](../tests/test_t13_acceptance.py),
[README.md](../README.md), [TASKS.md](TASKS.md), laporan ini dan checklist Word.
