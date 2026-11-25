# Beta v0.5.1 — margin efektif dan font bawaan

`main` lokal bersih pada awal pekerjaan dan menunjuk commit `8e0f2de`, sama dengan satu-satunya branch pada remote GitHub yang diperiksa. Tidak ada perubahan lokal v0.5 yang belum disimpan pada saat pemeriksaan. Pekerjaan PC kantor dengan 261 tes tidak dapat diidentifikasi pada branch remote tersebut; tidak diklaim telah disinkronisasi. Tidak dilakukan pull, commit, atau push.

## Margin

Aturan PPKI-LAY-008 menyebut **pias kiri bidang tulisan 4 cm**, berlaku untuk semua jenjang dengan `fix_mode=Auto`. Ukuran margin yang tertulis di section tidak selalu sama dengan posisi efektif bidang tulisan: gutter dan mirror margins dapat memengaruhi sisi penjilidan dan halaman ganjil/genap. Aturan JSON tidak menjelaskan cara menggabungkan kondisi tersebut. Karena itu koreksi tidak dipaksakan dan temuan ditandai perlu review. Section landscape, kolom khusus, continuous dan pengaturan halaman kompleks tetap dilindungi.

Pada tesis privat S2, kedua section portrait mempunyai margin kiri/kanan/atas/bawah masing-masing 3 cm, gutter 1 cm, dan mirror margins aktif. Hasil pemeriksaan: **0 section diperbaiki, 8 keputusan margin uncertain**, 0 gagal; margin kiri tetap 3 cm. Ini bukan pernyataan bahwa margin efektif sudah memenuhi aturan. File hasil pemeriksaan identik dengan sumber; SHA-256 sumber sebelum dan sesudah identik.

## Font

Pemeriksa font kini membaca `docDefaults` sebagai sumber terakhir setelah format langsung, style karakter dan style paragraf beserta pewarisannya. Nama ASCII dan hAnsi harus eksplisit dan identik; theme atau deklarasi tidak lengkap tetap tidak diketahui. Tidak ada perubahan style global, izin cakupan, aturan JSON, ataupun perlindungan elemen khusus. Nilai font yang tidak diketahui tidak dianggap salah dan belum dinormalisasi hanya berdasarkan asumsi.

Fixture sintetis dengan cakupan isi yang dikonfirmasi dan default Arial 11 pt menghasilkan koreksi menjadi Times New Roman 12 pt; bold dan italic tetap ada, bagian paket di luar `word/document.xml` identik, dan pemrosesan kedua tidak menghasilkan perubahan tambahan. Pengujian prioritas direct/style, default tidak lengkap dan theme ambigu juga dilakukan.

Pada 198 kandidat teks isi dalam tesis lokal, 11 font terukur sesuai dan 187 tidak dapat dipastikan atau memiliki struktur yang tidak aman; ini bukan penilaian seluruh dokumen. Tanpa cakupan isi tervalidasi untuk sesi ini, **0 paragraf dan 0 run font dinormalisasi**. Hasil mock, label sampel, dan kesamaan style tidak digunakan sebagai izin.

## Integritas dan keterbatasan

Tesis berisi 896 paragraf, 29 tabel, 15 gambar inline dan 2 section. Pemeriksaan margin tidak menghasilkan byte baru, sehingga isi, tabel, gambar, header/footer, field dan bagian paket tetap identik untuk pemeriksaan ini. Tidak ada API dipanggil. T14 tetap aktif. Fixture terpisah menguji koreksi nyata dan integritas paket. LibreOffice tidak ditemukan; Microsoft Word terpasang, tetapi tidak diotomasi atau digunakan untuk pemeriksaan visual pada sesi ini. Tidak ada pengukuran ulang layout dan validasi visual Microsoft Word masih PENDING; jumlah halaman, gambar, caption dan tabel tetap perlu pemeriksaan manusia saat perubahan nyata dilakukan.

Baseline sebelum perubahan: **254 passed**. Regresi akhir: **259 passed** (`.venv\Scripts\python.exe -m pytest -q`). Sebanyak **50 tes** terfokus formatter dan pilot termasuk Streamlit AppTest juga lulus. Penggunaan pada dokumen nyata dengan perubahan format tetap memerlukan cakupan yang dapat dibuktikan dan pemeriksaan visual.
