# T14 — Stabilitas, keamanan file, dan penanganan error

## Masalah dan perbaikan

Upload sebelumnya langsung diproses tanpa batas ukuran atau pemeriksaan paket;
konfirmasi dan output lama juga perlu diikat lebih ketat pada konteks. Upload
kini diperiksa sebelum python-docx membaca dokumen: ekstensi, ukuran, struktur
ZIP, komponen XML utama dan CRC. Batas default input 20 MiB dapat diubah dengan
variabel lingkungan `PPKI_MAX_UPLOAD_MB` bilangan bulat positif. Batas tetap:
2.000 entri, 200 MiB total ukuran dekompresi dan rasio 1.000 per entri.
Entri terenkripsi, duplikat/duplikat beda kapital, jalur berbahaya, symbolic
link, VBA dan ActiveX ditolak. Tidak ada ekstraksi ke filesystem atau eksekusi
macro/script; penolakan diberikan sebagai pesan, dan exception tak terduga
dicatat ke log lokal tanpa traceback ditampilkan di UI.

State audit dan output dibatalkan saat hash file, jenjang atau style berubah;
konfirmasi terkait dokumen/jenjang/style. Jika formatter gagal, output lama
dihapus dan tombol unduh tidak ditampilkan. Validasi integritas dan audit
ulang formatter tetap dipertahankan tanpa perubahan.

## Pengujian

`.\.venv\Scripts\python.exe -m pytest -q`: **132 passed, 0 failed**.
Tes negatif mencakup input kosong, bukan ZIP/DOCX, file terpotong, ekstensi
salah, XML utama rusak, komponen hilang, batas input, jumlah entri, batas
dekompresi, rasio kompresi, jalur traversal, symbolic link, duplikat, enkripsi,
VBA dan ActiveX. Batas dekompresi diuji dengan metadata ZIP sintetis.

AppTest mencakup upload valid/tidak valid, penggantian file dan jenjang,
konfirmasi isi dan BAB, mode Heading saja, kegagalan validasi dan penghapusan
unduhan lama. Tes T13 yang tetap lulus memeriksa empat fixture, integritas paket,
teks, tabel, audit ulang, idempotensi, dan ketersediaan DOCX/CSV. Pemeriksaan
integritas berlaku untuk konstruksi dan perubahan yang diuji; bukan jaminan
seluruh dokumen Word aman.

## Pengukuran sederhana

Satu pengukuran lokal, waktu dalam detik, bukan standar kinerja:

| Fixture | Byte | Validasi | Audit | Format dan audit ulang |
| --- | ---: | ---: | ---: | ---: |
| Skripsi S1 dasar | 39.552 | 0,003 | 0,046 | 0,135 |
| Dummy Master | 109.163 | 0,012 | 0,212 | 0,530 |

## Keterbatasan

Pemeriksaan ZIP bukan antivirus atau sandbox Word. Konten tertanam dan tautan
eksternal lain dapat tetap ada; aplikasi tidak menjalankannya, tetapi perilaku
Microsoft Word saat membuka dokumen di luar kendali aplikasi. Batas upload
diterapkan setelah Streamlit menerima bytes ke memori, bukan batas jaringan
Streamlit. Nilai batas dapat menolak dokumen sah yang sangat besar atau sangat
terkompresi. Paket kompleks yang lolos pemeriksaan awal masih dapat gagal
diproses; pengguna perlu memeriksa file dan log lokal. Pemeriksaan Word dan
dokumen nyata T13 masih PENDING; validasi visual belum diklaim selesai.

File berubah: [app.py](../app.py), [audit.py](../core/audit.py),
[test_t14_safety.py](../tests/test_t14_safety.py), [README.md](../README.md),
[TASKS.md](TASKS.md), dan laporan ini.
