# v1.1A — Validasi struktur dokumen nyata

Satu tesis lokal yang disediakan pemilik diproses secara read-only setelah
lolos validasi DOCX. File sumber berada di folder yang diabaikan Git; hash
SHA-256 sebelum dan sesudah sama. Tidak ada isi penelitian, nama atau NIM yang
disimpan dalam laporan atau fixture. Tidak ada API eksternal yang dipanggil.

## Pencocokan acuan

Kelima judul BAB yang diberikan pemilik ditemukan pada paragraf 292, 335, 388,
412 dan 762. Kelimanya menjadi kandidat `bab` dengan status `needs_review`.
Lima kemunculan terkait pada daftar isi (paragraf 209, 215, 224, 228 dan 238)
memakai style TOC dan diklasifikasikan sebagai entri daftar isi, bukan BAB.
Untuk **lima BAB yang diberikan sebagai acuan**, diperiksa lima kandidat dan
lima lokasi sebenarnya: TP 5, FP 0, FN 0; precision dan recall masing-masing
5/5 = 100% untuk sampel lima judul ini saja. Kelimanya tetap memerlukan
konfirmasi; angka tersebut bukan ukuran akurasi keseluruhan atau bukti aman
untuk formatting. Identifikasi daftar isi didukung oleh style TOC dan field;
hasil belum membuktikan bahwa setiap entri lainnya sudah dinilai dengan benar.

## Hasil per kategori

Tabel berikut membedakan jumlah kandidat dari pemeriksaan terbatas terhadap
lokasi yang dapat diverifikasi. `—` berarti tidak diketahui, bukan nol.
Pemeriksaan parsial tidak menyediakan acuan lengkap untuk menghitung FP, FN,
precision atau recall pada kategori selain lima BAB tersebut.

| Jenis | Kandidat | Diperiksa pada acuan | TP | FP | FN | Belum pasti / cakupan |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| BAB acuan | 5 | 5 | 5 | 0 | 0 | 5 kandidat tetap `needs_review` |
| Entri daftar isi | 38 | 5 entri BAB | 5 | — | — | Sisa entri belum diberi label manual |
| Subbab | 27 | 1 contoh, paragraf 293 | 1 | — | — | Sisa dan bagian terlewat belum diukur |
| Sub-subbab | 12 | 1 contoh, paragraf 420 | 1 | — | — | Sisa dan bagian terlewat belum diukur |
| Teks isi | 198 | — | — | — | — | Semua kandidat perlu review |
| Daftar bernomor / berpoin | 168 | — | — | — | — | Kategori dan konteks belum diverifikasi |
| Caption tabel | 23 | — | — | — | — | Hubungan dengan objek belum diverifikasi |
| Caption gambar | 16 | — | — | — | — | Hubungan dengan objek belum diverifikasi |
| Paragraf sel tabel | 790 | Struktur sel | — | — | — | 29 tabel body teramati; belum dilabeli manual |
| Sampul / halaman judul | 0 | — | — | — | — | Ketiadaan kandidat bukan bukti tidak ada bagian |
| Ringkasan / summary | 1 / 1 | 2 label | 2 | — | — | Isi dan batas bagian belum diverifikasi |
| Daftar isi | 1 | 1 label | 1 | — | — | Batas seluruh bagian belum diverifikasi |
| Daftar pustaka / entri | 1 / 54 | 1 label | 1 | — | — | Semua entri masih kandidat, belum diverifikasi |
| Lampiran | 5 | 1 label | 1 | — | — | Kandidat lain dan batas bagian belum diverifikasi |

Diagnostik objek terpisah mengidentifikasi 7 gambar inline dan 89 objek kompleks;
ini bukan total seluruh gambar atau bukti hubungan caption. Tidak semua caption,
isi tabel, teks isi, atau bagian khusus telah dibandingkan dengan acuan manusia.

## Kesalahan yang ditemukan dan perbaikan

Sebelum perbaikan, TP BAB 0 dan FN 5 pada lima judul acuan: judul memakai
Heading 1 dengan drawing, sementara pemisah halaman terletak pada paragraf
kosong sebelumnya. Classifier terjebak pada konteks daftar isi. Heuristik kini
menghasilkan kandidat BAB `needs_review` hanya ketika ada Heading 1 berpola
Romawi setelah pemisah halaman dan tidak terdapat hyperlink/field atau tab.
Subheading dalam konteks yang masih ambigu juga tetap `needs_review`.

Heading daftar pustaka yang eksplisit tetapi memakai style `Heading` semula
terlewat; sekarang dikenali sebagai kandidat yang tetap perlu review. Dua tes
sintetis mereproduksi pola ini tanpa memakai isi tesis. Regresi awal sempat
memunculkan satu kandidat BAB palsu pada Dummy Master; kondisi diperketat dan
tes Master serta fixture baru lulus. Meski sampel BAB tesis menghasilkan FP 0,
ini tidak menjamin tidak ada FP pada dokumen atau pola lain.

## Keputusan dan batasan

**Belum cukup aman untuk memilih cakupan formatting otomatis v1.2.** Semua
judul BAB tesis masih ambigu, hasil kategori lain belum mempunyai acuan lengkap,
dan sejumlah objek/struktur Word tidak dapat dipastikan. Formatter lama,
aturan JSON dan konfirmasi operator tidak berubah. Pemeriksaan visual Word dan
acceptance dokumen nyata untuk hasil formatter tetap PENDING. Pengujian ini
mengevaluasi classifier read-only, bukan hasil format.

Regresi: `.\.venv\Scripts\python.exe -m pytest -q` — **137 passed**,
termasuk Streamlit AppTest.
