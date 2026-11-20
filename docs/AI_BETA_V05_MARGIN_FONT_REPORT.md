# Beta v0.5 — margin dan font

Status: **margin deterministik tersedia pada section yang terbukti aman; koreksi font tanpa klasifikasi/konfirmasi cakupan belum tersedia**. Tidak ada panggilan API selama pengujian ini. Perubahan rules JSON tidak dilakukan.

Formatter T4B dipakai kembali dengan allowlist empat aturan margin LAY-008–011, nilai target dari rule JSON yang sesuai dengan validator, `fix_mode=Auto`, dan audit ulang. Ukuran kertas dan orientasi tidak masuk allowlist. Section landscape, multi-kolom, continuous, halaman khusus/revisi, ukuran halaman tidak diketahui, gutter, atau mirror margins dilewati untuk review. Pemeriksaan tambahan ini khusus margin dan tidak memblokir formatter teks hanya karena gutter.

Panel margin tanpa AI memakai hasil Beta tervalidasi dalam sesi bila tersedia, atau DOCX unggahan. CSV berisi operasi margin dan, bila ada, operasi Beta sebelumnya; hitungan section, paragraf, run font, normalisasi nilai tidak diketahui dan operasi dilewati dibedakan. Font LAY-005 memakai formatter Beta yang sudah ada pada cakupan yang sebelumnya terverifikasi, dengan direct formatting dan pewarisan style yang dapat dipastikan; simbol, theme, struktur kompleks dan nilai tidak diketahui dilewati. Tidak ada perluasan izin pada seluruh style Normal dan tidak ada klasifikasi AI baru. Jika hasil Beta sebelumnya tidak ada dalam sesi, panel margin tidak mengarang izin untuk memformat font.

## Evaluasi tesis lokal S2

| Section | Orientasi / ukuran | Margin kiri sebelum | Margin kiri sesudah | Keputusan |
|---|---|---:|---:|---|
| 1 | Portrait A4 | 3 cm | 3 cm | Review: gutter 1 cm dan mirror margins |
| 2 | Portrait A4 | 3 cm | 3 cm | Review: gutter 1 cm dan mirror margins |

Kedua section mempunyai gutter 1 cm dan `mirrorMargins` aktif. Kombinasi ini memengaruhi interpretasi margin penjilidan dan halaman ganjil/genap; tidak cukup bukti untuk menetapkan margin kiri 4 cm tanpa review. Tidak ada section diubah, delapan keputusan margin memerlukan review, 0 gagal. Ini bukan klaim bahwa nilai 3 cm telah sesuai PPKI.

Pada 88 kandidat yang sebelumnya diinventarisasi sebagai calon isi, pemeriksaan font lokal menghasilkan satu yang dapat diketahui sesuai dan 87 yang tidak pasti atau kompleks; **0 paragraf dan 0 run font diubah tanpa cakupan yang dibuktikan**. Ini bukan inventaris seluruh dokumen atau bukti kepatuhan. Hasil API nyata yang disebut operator tidak tersedia sebagai session state dalam pengujian lokal ini, sehingga tidak direkonstruksi dari mock atau label. Normalisasi font dari nilai tidak diketahui: 0.

DOCX asli dan output pemeriksaan margin identik byte-per-byte. Terdapat 896 paragraf, 29 tabel, 15 gambar inline dan dua section; teks dan seluruh komponen paket dengan demikian tetap identik untuk pengujian ini. Fixture sintetis menguji perubahan margin nyata dan integritas paket terpisah. Tidak ada file tesis privat yang disalin ke Git.

## Render dan risiko

LibreOffice/`soffice` tidak ditemukan pada PATH, lokasi instalasi umum atau App Paths di lingkungan saat ini; render baru tidak dilakukan dan jumlah halaman sebelum/sesudah **tidak diverifikasi**. Nilai 86 halaman yang diberikan operator adalah hasil pengujian sebelumnya, bukan pengukuran ulang tahap ini. Pemeriksaan posisi gambar, tabel, caption, potongan konten, daftar isi, nomor halaman dan halaman kosong masih PENDING. Validasi visual Microsoft Word juga PENDING.

## Keterbatasan dan hasil tes

- Pembedaan isi dan bagian khusus belum dapat dibuktikan dari style saja. Tanpa hasil Beta tervalidasi atau konfirmasi cakupan yang aman, font tidak dinormalisasi otomatis; font theme dan nilai tidak diketahui tetap review.
- Section dengan gutter/mirror memerlukan peninjauan interpretasi aturan serta pemeriksaan layout sebelum margin diubah. Tidak ada klaim bahwa semua layout Word aman.
- Kegagalan validasi pada jalur margin membatalkan hasil dan menampilkan error; jalur ini belum menyediakan CSV kegagalan tersendiri.
- Regresi: `.\.venv\Scripts\python.exe -m pytest -q` — **254 passed**, termasuk Streamlit AppTest. Tes terfokus jalur Beta dan jalur margin juga lulus setelah penyesuaian terakhir.

File tahap ini: `core/formatter.py`, `app.py`, `tests/test_formatter.py`, `tests/test_ai_beta.py`, `docs/WORK_PROGRESS.md`, dan laporan ini.
