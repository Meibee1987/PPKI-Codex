# v1.1 — Pengenalan struktur read-only

## Implementasi

[structure.py](../core/structure.py) mengenali kandidat bagian awal, judul,
BAB berpola `BAB I` dan `I`, subbab/sub-subbab bernomor, teks isi, daftar,
caption, paragraf sel tabel, daftar pustaka dan lampiran. Lokasi memakai nomor
paragraf body atau tabel/baris/kolom/paragraf pada dokumen yang dianalisis.
Style, alasan, kategori keyakinan kualitatif dan status `detected` atau
`needs_review` ditampilkan. `detected` berarti bukti struktur terbatas, bukan
hasil validator PPKI atau keyakinan statistik. Kandidat teks isi selalu perlu
review. Pengenalan ini tidak menjadi input formatter atau audit lama; konfirmasi
manual tetap berlaku dan validasi keamanan upload tetap digunakan.

[app.py](../app.py) menampilkan ringkasan dan tabel pada panel struktur yang
sudah ada. Tes menggunakan DOCX sintetis dalam memori dan fixture yang tersedia;
tidak ada dokumen tesis nyata yang dibaca atau dimasukkan ke repository.

## Hasil pada fixture

Angka adalah kandidat, bukan temuan yang telah diverifikasi manusia. Urutan
kolom: BAB, subbab/sub-subbab, teks isi, caption tabel, caption gambar, review.

| Fixture | BAB | Subbab | Isi | Caption tabel | Caption gambar | Review |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dummy Master | 3 | 8 | 26 | 3 | 2 | 90 |
| Skripsi S1 | 1 | 2 | 11 | 1 | 0 | 17 |
| Tesis S2 | 3 | 1 | 18 | 1 | 2 | 26 |
| Disertasi S3 | 1 | 1 | 13 | 1 | 0 | 28 |

Tes sintetis memeriksa angka Romawi, style Normal, daftar isi, cover, caption,
sel tabel, referensi dan determinisme. Dummy Master mengenali tiga BAB pada
paragraf 40, 60 dan 75. Baseline sebelum perubahan: **132 passed**; regresi
setelah perubahan: **135 passed** termasuk Streamlit AppTest.

## False positive, false negative dan batasan

Pada uji awal, paragraf 57 Dummy Master yang menyerupai judul BAB sempat
menjadi kandidat BAB tambahan. Heuristik dipersempit dan tiga BAB sebenarnya
kini terdeteksi; paragraf tersebut masih dapat menjadi kandidat teks isi
`needs_review`, bukan bukti teks isi yang aman. Heading yang memakai style
Normal di tengah BAB tanpa batas halaman eksplisit dapat terlewat sebagai BAB;
Heading 1 tepat setelah daftar isi tanpa pemisah yang dapat dipastikan juga
dibiarkan ambigu. Ini adalah false negative yang disengaja untuk melindungi
entri daftar isi. Pencocokan label dan pola dapat salah pada dokumen lain dan
belum dikalibrasi terhadap korpus dokumen nyata; angka di atas bukan metrik
akurasi. Hubungan caption dengan objek, identitas sampul versus judul, dan isi
referensi masih memerlukan review. Tabel bersarang, text box, header/footer,
footnote, nomor otomatis yang tidak terwujud sebagai teks, dan batas halaman
hasil render tidak dikenali secara menyeluruh. Status `detected` pada heading
tidak menjamin klasifikasinya benar atau formatnya sesuai.

Konteks yang lebih kompleks mungkin dibantu AI pada tahap berikutnya setelah
persetujuan eksplisit dan pengujian privasi; AI tidak diperlukan untuk fitur
ini dan tidak boleh menggantikan validasi. Rekomendasi berikut: evaluasi
read-only pada salinan dokumen anonim dengan label acuan operator dan ukur
false positive/false negative sebelum menggunakan klasifikasi untuk formatter.
Acceptance Word dan dokumen nyata T13 tetap PENDING.

File berubah: [structure.py](../core/structure.py), [app.py](../app.py),
[test_structure_recognition.py](../tests/test_structure_recognition.py),
[README.md](../README.md), [TASKS.md](TASKS.md), dan laporan ini.
