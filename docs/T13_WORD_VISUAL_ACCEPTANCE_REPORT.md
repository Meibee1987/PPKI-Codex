# T13 — Validasi Visual Microsoft Word

**Status: PARTIAL.** Operator menerima terbatas cakupan 71 paragraf pada tesis uji dan menahan 11 paragraf, termasuk seluruh operasi 401. **Acceptance teknis varian 71: PASS TERBATAS** (86 halaman, integritas utuh, visual tujuh halaman terfokus). Penerimaan akhir file oleh operator, item historis halaman 4 S2 dan cakupan acceptance objek kompleks yang belum teruji tetap terbuka. Output Beta 82 bukan hasil final yang disetujui; tidak ada izin otomatis generik.

## Catatan privasi untuk sinkronisasi laptop — 26 November 2026

Nama pribadi pada nama file unduhan, path profil Windows, dan fingerprint
DOCX privat disamarkan dalam versi repository ini. Hash serta bukti lengkap
tetap ada di manifest lokal `private_tests/`; salinan laporan sebelum
penyamaran juga dicadangkan di sana. Path `private_tests/...` di laporan
adalah petunjuk lokasi lokal, bukan file yang dikirim ke GitHub.
Laptop menerima kode, tes sintetis dan laporan status; acceptance dengan
bukti privat hanya dapat dilanjutkan setelah pemilik memindahkan folder
privat secara lokal/kanal yang dipilih sendiri. Tidak ada DOCX tesis,
cuplikan audit privat, CSV asli, render atau hasil eksperimen yang dimasukkan
ke commit ini. Status T13 tetap PARTIAL dan regresi historis tetap 274 passed.

## Penerimaan cakupan 71 dan acceptance teknis akhir — 26 November 2026

**Keputusan operator diterima secara eksplisit:** 71 paragraf naratif diterima
terbatas sebagai cakupan validasi akhir T13 pada salinan tesis uji. Sebelas
paragraf ambigu ditahan dengan seluruh format sumber dipertahankan; semua
operasi 401, termasuk spasi dan indentasi, dikecualikan. Output Beta 82 tidak
digunakan sebagai hasil final yang disetujui. Keputusan ini tidak berlaku
sebagai izin otomatis untuk dokumen lain atau perubahan izin UI/produksi.

Keputusan ini menggantikan status PENDING **cakupan 71** pada catatan sebelumnya.
Bukti lama dipertahankan sebagai riwayat, bukan ditulis ulang. Penerimaan
**file keluaran akhir** tidak disamakan dengan persetujuan cakupan; tidak
dicatat sebagai persetujuan operator otomatis setelah pemeriksaan teknis.

### File yang diperiksa dan keputusan terikat hash

Menggunakan varian yang sudah tersedia, tidak diregenerasi atau disimpan ulang:

`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/EXPERIMENT_NOT_OPERATOR_APPROVED.docx`

SHA-256 varian:
`[hash tersedia pada manifest privat]`.
Nama file adalah label saat eksperimen awal; nama dan byte dipertahankan.
Status cakupan terbaru tercatat terpisah dalam
`experiment_71_only/limited_scope_final_technical_acceptance.json`, bersama
batas keputusan, hash, scope, pengecualian dan bukti akhir. File ini tetap
salinan uji lokal, bukan output produksi otomatis.

### Verifikasi operasi dan preservasi

| Pemeriksaan final | Hasil aktual | Status |
|---|---|---|
| LAY-017 | 71 operasi pada 71 target; spasi hasil langsung 1,0 pada seluruh target | PASS TERBATAS |
| LAY-018 | Tepat 3 operasi: paragraf 386, 410, 414, indentasi 567 twip (sekitar 1 cm) | PASS TERBATAS |
| Sebelas paragraf ditahan | 307,314,319,326,373,401,757,758,759,764,769 seluruh XML paragraf identik dengan sumber | PASS TERBATAS; tidak ada operasi pada kelompok ini |
| Paragraf 401 | Semua format sumber dipertahankan, termasuk spasi asal dan indentasi sekitar 0,926 cm | PASS TERBATAS untuk pengecualian yang diminta |
| Semua paragraf di luar scope | Seluruh 825 paragraf non-target identik XML dengan sumber | PASS TERBATAS |
| Teks dan tabel | Seluruh teks paragraf identik; XML seluruh 29 tabel identik | PASS TERBATAS |
| Media, section, header/footer, field | Bagian paket selain XML utama identik, termasuk seluruh media dan header/footer; XML section serta struktur utama di luar properti operasi identik | PASS TERBATAS untuk preservasi, bukan seluruh perilaku pembaruan field |
| Word dan pagination | Pembukaan read-only, repagination dan ComputeStatistics diulang hanya untuk varian; 86 halaman, 2 section portrait (1–16 dan 17–86), 29 tabel, 15 inline shapes, 201 field body | PASS TERBATAS; tidak diwarisi dari Beta 82 |
| Integritas file | Hash varian sebelum/sesudah Word dan hash tesis asli sesuai bukti | PASS TERBATAS |

Pengamanan T14/formatter tidak diubah. Gutter dan mirror margins tetap
sebagaimana sumber. Tidak ditemukan kehilangan/perubahan konten atau kerusakan
baru pada pemeriksaan struktur dan sampel visual; ini bukan klaim semua aturan
PPKI, seluruh glyph atau semua konstruksi Word sudah diterima.

### Pemeriksaan visual akhir yang hemat

Render varian **29, 31, 33, 34** yang sudah tersedia diperiksa kembali secara
visual dan memakai bukti perbandingan pixel sebelumnya. Halaman lain ditambah
hanya bila ada celah bukti: **17** mewakili normalisasi spasi, **74 dan 76**
mewakili area paragraf tertahan beserta narasi/daftar di sekitarnya.

| Halaman fisik varian 71 | Bukti akhir | Hasil |
|---|---|---|
| 29 | Render tersimpan identik dengan hasil indentasi 386 yang sudah ditinjau | Perubahan diharapkan, tabel/caption tetap terlihat, tanpa clipping baru yang teramati |
| 33 | Render tersimpan identik dengan hasil indentasi 410 yang sudah ditinjau | Perubahan diharapkan, tanpa clipping baru yang teramati |
| 34 | Render tersimpan identik dengan hasil indentasi 414 yang sudah ditinjau | Perubahan diharapkan, heading/isi tetap terlihat |
| 31 | Render tersimpan identik dengan sumber awal | Paragraf 401 dan daftar berikutnya tetap pada tampilan sumber |
| 17 | Ekspor Word baru hanya halaman ini, PNG identik dengan render sumber tersimpan; dilihat langsung | Tidak ada perubahan tak terduga pada sampel spasi/heading |
| 74 | Ekspor Word baru hanya halaman ini, PNG identik dengan sumber; dilihat langsung | Narasi dan area enumerasi tertahan tetap; nomor tercetak 58 terlihat |
| 76 | Ekspor Word baru hanya halaman ini, PNG identik dengan sumber; dilihat langsung | Pengantar kesimpulan/saran dan daftar tetap terlihat, tanpa overlap baru |

Tambahan Word menggunakan versi **16.0 build 16.0.20625**, read-only, ditutup
`Close(0)` tanpa menyimpan. Bukti: `final_word_check.json`,
`final_sample_comparison.json`, tiga `final_page_17/74/76.pdf` dan PNG di folder
varian. Hanya **3 halaman baru** dirender; tidak ada render ulang 86 halaman.
Tujuh halaman varian telah diperiksa; **79 halaman lainnya belum dibandingkan
secara visual untuk varian 71**. Tidak digunakan klaim "82 halaman identik"
milik Beta 82 untuk meluluskan sisa halaman varian. Tidak teramati clipping,
pergeseran objek atau perubahan nomor halaman baru pada sampel yang diperiksa.

**Acceptance teknis varian 71: PASS TERBATAS**, terikat hash, operasi, lingkungan
Word dan lingkup bukti di atas. Keputusan ini mencakup integritas seluruh
konten secara struktural, pengukuran pagination dan pemeriksaan visual
terfokus; tidak menyatakan seluruh halaman bebas masalah baseline.

### Syarat yang masih menghalangi penutupan T13

1. **Penerimaan akhir file oleh operator**, terpisah dari persetujuan cakupan
   71 yang sudah diberikan. File yang diputuskan adalah varian dengan hash di
   atas; output Beta 82 tetap bukan hasil final yang disetujui.
2. **Item "halaman 4 S2"**: sumber T5 merujuk fixture sintetis S2 tetapi tidak
   menjelaskan versi artefak atau nomor fisik/tercetak. Belum ada dasar menutup
   item atau menggantinya dengan halaman fisik 4 tesis privat. Butuh identifikasi
   artefak atau keputusan eksplisit penyelesaian catatan historis tersebut.
3. **Cakupan acceptance objek kompleks yang belum ditutup**: tesis ini tidak
   memiliki footnote aktif, persamaan native atau landscape; preservasi field
   bukan pengujian pembaruan field. Bukti acceptance yang relevan atau batas
   cakupan yang disepakati perlu dicatat, tanpa mengklaim fitur belum didukung
   sebagai PASS. Tidak otomatis diperlukan pengulangan seluruh fixture.
4. **Batas visual varian**: tujuh halaman dipilih berdasarkan perubahan dan
   risiko; 79 halaman belum diperiksa visual ulang. Jika diperlukan untuk
   sign-off operator, tindak lanjut harus berbasis lokasi berisiko, bukan
   langsung merender semua halaman tanpa alasan.

Langkah berikut yang paling berdampak: **sign-off akhir operator terhadap file
varian 71 yang terikat hash ini**, memakai tujuh halaman bukti dan batas
cakupan yang dinyatakan; ini menyelesaikan gerbang penerimaan tesis sebelum
mengurus sisa item matriks T13. Tidak diminta mengulang review 82 paragraf.
T13 tetap **PARTIAL** dan tidak dijadikan izin otomatis lintas dokumen.

Perubahan pada Git hanya dua laporan pada tahap ini. Bukti privat tambahan
dan catatan keputusan disimpan tanpa menghapus bukti lama. Formatter produksi,
aturan JSON, tesis asli, varian dan output Beta lama tidak diubah; tidak ada
API, pull, commit atau push. `git diff --check` lulus. Pytest tidak diulang;
regresi terakhir tetap **274 passed**.

## Persiapan keputusan operator dan varian eksperimen 71 — 26 November 2026

**Keputusan operator masih PENDING. T13 tetap PARTIAL.** Kandidat yang
 direkomendasikan: 71 paragraf naratif. Sebelas paragraf ambigu direkomendasikan
untuk dikecualikan sementara dari normalisasi dan mempertahankan format sumber.
Tidak ada persetujuan operator yang dicatat atau izin produksi yang diperluas.

### Keputusan kelompok 71

Cakupan: 71 paragraf narasi berisiko lebih rendah yang tercantum pada audit
privat sebelumnya. Rekomendasi hanya untuk dokumen/hash ini dan aturan
**LAY-017 (spasi eksplisit 1,0)** serta tiga **LAY-018 (indentasi 1 cm)**,
bukan seluruh aturan atau dokumen baru. Dasar: jenis sistem `teks_isi`, style
Normal, struktur sederhana, tidak ditemukan heading/caption/numPr/field/
tabel/objek kompleks pada target, preservasi teknis pasangan lama sudah
terbukti, serta semua operasi tercatat per lokasi.

Contoh: paragraf 294 halaman 17, spasi langsung tidak eksplisit menjadi 1,0;
paragraf 386 halaman 29, indentasi 1,27 cm menjadi sekitar 1 cm. Spasi tidak
eksplisit tidak membuktikan format efektif sebelumnya salah; normalisasi
properti tidak selalu menghasilkan perubahan visual. Narasi yang secara
struktur sederhana tetap dapat mempunyai maksud editorial khusus. Karena
itu rekomendasi tidak menjadi konfirmasi semantik atau izin untuk tesis lain.

### Sebelas kasus untuk ditahan

Cuplikan asli hanya disimpan secara lokal pada tabel privat:

`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/operator_decision_11_private.csv`

Tabel tersebut memuat cuplikan singkat, struktur, operasi lama, operasi varian,
alasan review dan rekomendasi per paragraf. Ringkasan berikut memakai konteks
yang diparafrasekan agar isi tesis tidak disalin ke dokumentasi tracked.
Operasi di kolom ini merupakan operasi lama/usulan yang **tidak diterapkan**
pada varian 71; seluruh sebelas paragraf di varian sama dengan sumber.

| Paragraf | Konteks ringkas | Struktur | Operasi lama yang ditahan | Alasan review | Rekomendasi |
|---|---|---|---|---|---|
| 307 | Pengantar pertanyaan penelitian | Pengantar daftar bernomor | Spasi 1,0 | Batas format pengantar/daftar belum disetujui | Pertahankan sumber; kecualikan sementara |
| 314 | Pengantar tujuan khusus | Pengantar daftar bernomor | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |
| 319 | Pengantar manfaat | Pengantar daftar manfaat | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |
| 326 | Pengantar faktor penelitian | Pengantar daftar bernomor | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |
| 373 | Pengantar proposisi | Pengantar P1/P2/P3 | Spasi 1,0 | Gaya pengantar belum pasti; proposisi tetap terlindungi | Pertahankan sumber; kecualikan sementara |
| **401** | Pengantar alat analisis | Pengantar daftar bernomor | **Spasi 1,0 dan indentasi 1 cm** | Aturan umum tidak menetapkan konteks pengantar ini secara tegas | **Pertahankan sumber, termasuk indentasi sekitar 0,926 cm; kecualikan seluruh operasi** |
| 757 | Keterbatasan pertama | Enumerasi verbal tanpa numPr | Spasi 1,0 | Prosa berurutan atau daftar khusus belum diputuskan | Pertahankan sumber; kecualikan sementara |
| 758 | Keterbatasan kedua | Enumerasi verbal tanpa numPr | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |
| 759 | Keterbatasan ketiga | Enumerasi verbal tanpa numPr | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |
| 764 | Pengantar kesimpulan | Pengantar daftar bernomor | Spasi 1,0 | Gaya pengantar belum disetujui | Pertahankan sumber; kecualikan sementara |
| 769 | Pengantar saran | Pengantar daftar prioritas | Spasi 1,0 | Alasan sama | Pertahankan sumber; kecualikan sementara |

Ini penahanan konservatif, bukan temuan bahwa kesebelas paragraf pasti salah
kategori. Tidak ada rekomendasi koreksi baru untuk kelompok ini.

### Prioritas paragraf 401: bukti aturan dan batas interpretasi

Snapshot JSON PPKI untuk LAY-018 menyatakan: "Baris pertama paragraf menjorok
1 cm dari bidang tulisan kiri." Target `1 cm`, applies_to `Semua`, fix_mode
`Auto`, sumber Lampiran 16, halaman PDF 161. LAY-017 pada sumber yang sama
menyatakan jarak baris 1 spasi. Keduanya dibaca dari JSON, tidak diubah.

Aturan tersebut mendukung angka 1 cm bagi paragraf yang berada dalam cakupan
yang tepat, tetapi tidak menjelaskan secara khusus apakah pengantar daftar
401 harus diperlakukan sebagai isi biasa atau mengikuti desain daftar.
Tidak cukup bukti untuk menetapkan bahwa koreksi indentasi 401 pasti tepat.
`Auto` tidak menghapus kebutuhan memastikan cakupan. Rekomendasi: kecualikan
401 dari seluruh normalisasi sampai operator memutuskan konteksnya.
Mempertahankan format sumber bukan klaim bahwa nilai sumber sudah patuh PPKI.

### Varian 71: eksperimen lokal yang sudah dibuat

File yang disiapkan untuk review, **bukan hasil yang disetujui operator**:

`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/EXPERIMENT_NOT_OPERATOR_APPROVED.docx`

Sumber input adalah salinan tesis awal, bukan file Beta yang masih mengandung
11 operasi tertahan. Handler `core.pilot.format_pilot` yang sudah ada dipakai
dengan aturan 017/018 yang difilter **dalam memori**, dan lingkup sementara
71 paragraf khusus eksperimen yang diminta pengguna. Parameter pemilihan
`confirmed` pada pemanggilan diagnostik hanya mewakili hipotesis eksperimen;
tidak ditulis sebagai label/persetujuan operator, state UI atau izin produksi.
Aturan lain, font, margin, gutter dan mirror margins tidak diperluas.

Varian menghasilkan tepat **74 operasi**: 71 spasi 1,0 dan 3 indentasi pada
386/410/414. Semua 11 paragraf tertahan, termasuk spasi dan indentasi 401,
identik XML dengan sumber. Seluruh **825 paragraf di luar 71** juga identik
XML dengan sumber. Tidak ada operasi tersembunyi terhadap kelompok tertahan.

Verifikasi integritas: teks paragraf utuh, seluruh XML tabel sama, seluruh
bagian paket di luar `word/document.xml` identik (termasuk media, header/footer,
relasi dan objek tertanam). Setelah hanya properti format 74 operasi tersebut
disisihkan, struktur XML utama sama dengan sumber. Validasi input T14,
pengamanan pilot, pemeriksaan integritas dan audit ulang handler tetap aktif.
File asli, output Beta lama dan CSV operasi lama tidak diganti.

### Pengukuran independen varian, bukan asumsi dari hasil 82

Word 16.0 build 16.0.20625 membuka varian read-only, menjalankan repagination
serta ComputeStatistics, lalu menutup tanpa menyimpan. SHA-256 varian sebelum/
sesudah identik. Hasil aktual: **86 halaman, 2 section portrait, 29 tabel,
15 gambar inline**. Gutter dan mirror tetap ada. Angka ini diukur pada varian,
bukan diwariskan dari hasil Beta 82.

Hanya halaman relevan 29/31/33/34 diekspor melalui mesin layout Word dan
dirender pada skala maksimum 1250 px:

| Halaman fisik varian | Perbandingan pixel aktual | Makna |
|---|---|---|
| 29 | Identik dengan Beta 82 pada halaman 29 | Koreksi indentasi 386 tetap ada |
| **31** | **Identik dengan sumber awal; berbeda dari Beta 82** | **Seluruh operasi 401 ditahan, format pengantar sumber dipertahankan** |
| 33 | Identik dengan Beta 82 pada halaman 33 | Koreksi indentasi 410 tetap ada |
| 34 | Identik dengan Beta 82 pada halaman 34 | Koreksi indentasi 414 tetap ada |

Referensi pixel tersebut telah ditinjau visual pada sesi sebelumnya. Tidak
ada render ulang seluruh 86 halaman dan tidak ada klaim 82 halaman varian
identik: halaman lain pada varian 71 **belum dirender ulang/dibandingkan**.
Preservasi struktur dan empat halaman terfokus lulus; acceptance visual
keseluruhan varian tetap PENDING MANUAL REVIEW.

Bukti baru privat: `experiment_evidence.json` (scope, 74 operasi, hash dan
invarian integritas), `word_experiment_evidence.json` (pengukuran Word), empat
PDF/PNG halaman relevan dan tabel keputusan 11 kasus di folder eksperimen.

### Keputusan yang perlu diberikan operator

1. Setujui atau tolak **71 paragraf naratif sebagai kelompok** untuk review/
   penggunaan terbatas pada dokumen ini, beserta 71 spasi dan 3 indentasi;
   bukan izin otomatis generik bagi semua dokumen.
2. Setujui atau revisi rekomendasi **mempertahankan seluruh 11 paragraf sesuai
   sumber**, khususnya mengecualikan spasi dan indentasi 401. Jika ingin
   mengoreksi kelompok tersebut, tentukan kebijakan editorial pengantar/
   enumerasi terlebih dahulu; belum ada perubahan untuk pilihan itu.
3. Nyatakan penerimaan akhir varian eksperimen setelah review yang diperlukan.
   Keputusan scope saja tidak otomatis menutup T13; item halaman 4 S2 yang
   artefaknya belum jelas dan cakupan objek kompleks belum teruji tetap terbuka.

Tidak ada pilihan yang dianggap sudah disetujui. T13 **PARTIAL**; acceptance
teknis pasangan Beta 82 sebelumnya tetap PASS TERBATAS. Varian 71 adalah
hasil eksperimen baru dengan bukti integritas/pagination sendiri dan pemeriksaan
visual terfokus empat halaman, bukan hasil AI Beta lama atau rilis produksi.
Regresi terakhir **274 passed** tidak diulang; formatter produksi dan JSON
aturan tidak diubah. `git diff --check` lulus. Tidak ada API, pull, commit
atau push. Seluruh cuplikan dan DOCX eksperimen disimpan hanya secara privat.

## Review kualitas cakupan 82 paragraf — 26 November 2026

**Rekomendasi: penerimaan bersyarat per kelompok, bukan izin otomatis untuk
seluruh 82 paragraf.** Preservasi teknis terbukti pada **82/82** paragraf
pasangan tersimpan. Dari tinjauan fungsi teks dan struktur, **71** merupakan
narasi isi berisiko lebih rendah yang layak direkomendasikan untuk persetujuan
kelompok; **11** masih perlu review kelompok; **0** terbukti wajib dikecualikan
karena heading/caption/field/tabel/objek kompleks masuk secara keliru.
Sebelas kasus review disarankan **ditahan sementara dari izin otomatis**,
bukan sudah diputuskan sebagai pelanggaran atau pengecualian permanen.
**Persetujuan operator yang sudah diberikan: 0; masih menunggu: 82.**
Angka 71 adalah rekomendasi audit khusus dokumen ini, bukan bukti universal
bahwa fungsi paragraf dapat dikenali otomatis. Status T13 tetap **PARTIAL**;
acceptance teknis before/after tetap **PASS TERBATAS**.

### Audit per lokasi dan dasar rekomendasi

Audit lengkap 82 baris tersedia pada:

`private_tests/t13_real_acceptance_20261125_235720/scope_82_operator_audit.csv`

Ringkasan mesin:
`private_tests/t13_real_acceptance_20261125_235720/scope_82_review_summary.json`.
CSV memuat lokasi paragraf dan halaman fisik, jenis sistem, style, kelompok
review, aturan/target JSON, nilai spasi dan indentasi sebelum/sesudah, alasan
rekomendasi atau penahanan, bukti visual, status persetujuan operator, dan
cuplikan singkat. Cuplikan penelitian hanya disimpan di folder privat yang
diabaikan Git. Tidak ada label operator, dokumen atau kode yang diubah.

| Kelompok untuk keputusan operator | Paragraf | Operasi tersimpan | Rekomendasi, bukan persetujuan |
|---|---:|---|---|
| Narasi isi berisiko lebih rendah | 71 | 71 spasi + 3 indentasi = 74 | Layak diterima terbatas sebagai satu kelompok pada pasangan tesis ini, setelah operator menyetujui konteksnya |
| Pengantar daftar/proposisi | 8 | 8 spasi + 1 indentasi = 9 | Tahan: tentukan apakah pengantar mengikuti format isi atau gaya bagian daftar khusus |
| Enumerasi naratif Pertama/Kedua/Ketiga | 3 | 3 spasi | Tahan: tentukan apakah prosa berurutan atau daftar khusus yang harus dipertahankan |
| Salah kategori struktural yang terbukti dalam 82 | 0 | 0 | Tidak ada heading/caption/item daftar Word/field/tabel/objek kompleks yang ditemukan di cakupan berubah |

Sistem mengenali seluruh 82 sebagai `teks_isi`, style **Normal**. Pemeriksaan
langsung XML dan style beserta pewarisannya tidak menemukan `numPr`, outline
heading, field Word, hyperlink, drawing/pict/object, footnote, persamaan,
content control atau tracked insert/delete pada 82 paragraf tersebut. Semuanya
paragraf langsung dalam body, bukan isi tabel. Tidak ditemukan penanda awal
caption atau item daftar bernomor/proposisi pada paragraf yang diubah.

Hal ini membuktikan tidak ada struktur terlindungi yang jelas terlewat pada
82 paragraf, tetapi tidak membuktikan semua fungsi semantik. Daftar khusus
bisa berupa prosa tanpa `numPr`; karena itulah 11 kasus tetap ditampilkan.
Diagnostik lokal sebelumnya masih menandai identitas kandidat `uncertain`.
Tidak dibuat label `auto_verified` atau konfirmasi baru dari hasil audit ini.

Contoh kontrol konteks: item daftar 308, 315, 320, 327, 402, 765 dan 770 berada
di luar cakupan berubah dan setiap aturan pada CSV tersimpan berstatus
`protected`. Proposisi P1/P2/P3 pada paragraf **374–376** juga tidak diubah,
meskipun pengenal struktur memberi jenis `teks_isi`; lapisan perlindungan Beta
mencatat keempat aturan masing-masing sebagai `protected`. Ini menunjukkan
mengapa jenis/style saja tidak cukup menjadi izin.

### Semua kasus ambigu, disajikan per kelompok

Nomor berikut adalah indeks paragraf langsung body, satu-based, seperti CSV
Beta. Halaman adalah nomor fisik Word, bukan nomor tercetak.

| Paragraf | Halaman | Konteks yang harus diputuskan | Perubahan / alasan penahanan |
|---|---:|---|---|
| 307 | 19 | Pengantar pertanyaan penelitian; diikuti daftar bernomor | Spasi eksplisit 1,0; fungsi pengantar versus format daftar perlu diputuskan |
| 314 | 20 | Pengantar tujuan khusus; diikuti daftar bernomor | Spasi 1,0; alasan sama |
| 319 | 20 | Pengantar manfaat; diikuti daftar manfaat | Spasi 1,0; alasan sama |
| 326 | 21 | Pengantar faktor penelitian; diikuti daftar bernomor | Spasi 1,0; alasan sama |
| 373 | 28 | Pengantar proposisi; diikuti P1/P2/P3 terlindungi | Spasi 1,0; pastikan pemisahan gaya pengantar dan proposisi |
| 401 | 31 | "Dalam proses analisis data, digunakan beberapa alat bantu seperti:"; diikuti daftar bernomor | Spasi 1,0 **dan indentasi sekitar 0,926 menjadi 1 cm**; satu-satunya kasus review dengan perubahan visual |
| 757 | 74 | Prosa keterbatasan dimulai "Pertama," | Spasi 1,0; enumerasi verbal tidak terdeteksi sebagai daftar Word |
| 758 | 75 | Prosa keterbatasan dimulai "Kedua," | Spasi 1,0; alasan sama |
| 759 | 75 | Prosa keterbatasan dimulai "Ketiga," | Spasi 1,0; alasan sama |
| 764 | 76 | Pengantar kesimpulan; diikuti daftar bernomor | Spasi 1,0; gaya pengantar perlu diputuskan |
| 769 | 76 | Pengantar saran; diikuti daftar prioritas | Spasi 1,0; gaya pengantar perlu diputuskan |

Tidak ada bukti bahwa 11 paragraf ini adalah heading, caption, kutipan langsung
atau item daftar bernomor yang pasti. Karena fungsi editorialnya berdekatan
dengan daftar, rekomendasi penahanan adalah tindakan konservatif. Daftar
alasan ini adalah catatan review, bukan perubahan aturan/handler aplikasi.

### Konsistensi operasi dan visual

- **82 paragraf unik, 86 operasi**, terdiri dari 78 paragraf spasi saja dan
  4 paragraf spasi sekaligus indentasi; bukan 86 paragraf.
- Sebelum normalisasi, `line_spacing` langsung pada seluruh 82 paragraf tidak
  eksplisit; nilai efektifnya tidak boleh disebut salah atau 2,0 hanya dari
  ketiadaan properti. Sesudahnya seluruh 82 mempunyai spasi eksplisit 1,0
  (`LAY-017`, target berasal dari snapshot JSON PPKI, Auto untuk S2).
- Empat koreksi `LAY-018` menghasilkan 567 twip, sekitar 1 cm: paragraf 386
  (halaman 29) dari 1,27 cm; 401/410/414 (halaman 31/33/34) dari sekitar
  0,926 cm. Tiga target naratif 386/410/414 masuk kelompok risiko lebih rendah;
  401 tetap memerlukan keputusan pengantar daftar.
- Bukti raster sebelumnya: **82 halaman identik**, empat bbox perubahan
  berada tepat pada keempat target indentasi. Tidak ada perubahan visual
  tambahan yang terukur dari penulisan spasi eksplisit. Ini konsisten dengan
  normalisasi properti tanpa perubahan layout yang terlihat pada lingkungan
  Word tersebut; bukan pembuktian nilai spasi efektif awal untuk semua kondisi.
- Angka 82 halaman identik dan 82 paragraf beroperasi bukan pengukuran yang
  sama. Operasi spasi menjangkau 27 halaman; hanya empat halaman memiliki
  perbedaan pixel. Seluruh pagination tetap 86 menjadi 86.

Contoh representatif sebelum/sesudah:

| Contoh | Sebelum | Sesudah | Bukti / keputusan |
|---|---|---|---|
| Narasi pendahuluan, paragraf 294, halaman 17 | Spasi langsung tidak eksplisit | Spasi eksplisit 1,0 | Halaman identik; contoh penerimaan kelompok narasi, operator tetap PENDING |
| Narasi sintesis penelitian, paragraf 386, halaman 29 | Spasi tidak eksplisit; indentasi 1,27 cm | Spasi 1,0; indentasi sekitar 1 cm | Reflow target terlihat, tanpa kerusakan baru; layak direkomendasikan |
| Pengantar daftar metode, paragraf 401, halaman 31 | Spasi tidak eksplisit; indentasi sekitar 0,926 cm | Spasi 1,0; indentasi sekitar 1 cm | Perubahan terlihat dan secara teknis utuh, tetapi fungsi pengantar tetap perlu keputusan |
| Enumerasi keterbatasan, paragraf 757, halaman 74 | Spasi tidak eksplisit; tanpa numPr | Spasi 1,0; teks/struktur sama | Halaman identik; tentukan apakah format prosa isi atau daftar khusus |

### Rekomendasi keputusan dan status T13

Operator cukup menilai **tiga kelompok** di atas, dibantu contoh dan sebelas
lokasi ambigu; tidak diminta memeriksa seluruh 82 secara terpisah. Rekomendasi:
terima secara bersyarat 71 paragraf naratif untuk pasangan tersimpan ini,
tahan delapan pengantar dan tiga enumerasi sampai kebijakan editorialnya
jelas. File Beta yang ada tetap berisi operasi pada seluruh 82; persetujuan
71 paragraf tidak berarti file tersebut otomatis disetujui seluruhnya.
Tidak dibuat file dengan 11 operasi dibatalkan dan tidak diubah izin UI.

Risiko tersisa: struktur/style tidak memastikan identitas semantik, sitasi
naratif tidak otomatis kutipan khusus, deteksi daftar verbal terbatas, dan
spasi implisit tidak membuktikan ketidaksesuaian. Bukti satu pasangan/raster
1250 px bukan jaminan seluruh tesis atau dokumen baru aman secara otomatis.

Item "halaman 4 S2" tetap belum terselesaikan: TASKS mengarah ke checklist,
checklist merujuk tabel T5 untuk fixture sintetis S2. T5 tidak mengidentifikasi
versi artefak atau nomor fisik/tercetak. Tidak ada dasar menyamakannya dengan
halaman fisik 4 tesis privat; fixture tidak diuji ulang untuk mencari-cari
halaman keempat.

Acceptance teknis tesis tetap **PASS TERBATAS**; T13 tetap **PARTIAL**.
Dapat dilanjutkan ke keputusan akhir operator per kelompok, tetapi belum
layak ditutup sebelum keputusan 11 kasus dan item checklist yang terbuka
terselesaikan. Tidak diperlukan render 86 halaman atau pytest ulang untuk
keputusan dokumentasi ini. Jika cakupan/output kelak diubah, baru verifikasi
hasil yang berubah diperlukan; kasus objek kompleks yang belum teruji tetap
berstatus belum teruji.

Hanya dua laporan dan dua artefak audit privat baru diperbarui/dibuat; kode,
formatter, dokumen asli/output Beta, CSV operasi asli, JSON aturan dan
persetujuan operator tidak diubah. Regresi terakhir **274 passed**, tidak
diulang. `git diff --check` lulus; tidak ada API, pull, commit atau push.

## Finalisasi acceptance teknis before/after tesis — 26 November 2026

**Acceptance teknis pasangan tesis yang tersimpan: PASS TERBATAS.**
**T13 keseluruhan: PARTIAL.** Finalisasi menggunakan hasil sesi sebelumnya;
terhentinya sesi karena usage limit bukan kegagalan pengujian. Pada finalisasi
ini tidak dilakukan render ulang, pembukaan Word ulang, pemanggilan formatter,
pengujian fixture, atau pengulangan 274 pytest.

### Output Beta ditemukan dan cocok dengan sumber

Pencarian diperluas dari repository/folder privat ke lokasi unduhan hasil
aplikasi. Output dan CSV pendamping ditemukan pada:

- `<folder-unduhan-lokal>/tesis_privat_beta_formatted.docx`
- `<folder-unduhan-lokal>/tesis_privat_beta_operations.csv`

File sumber di Downloads identik byte-per-byte dengan
`private_tests/tesis_uji.docx`. Output memiliki 73 bagian paket yang sama;
72 bagian identik, hanya `word/document.xml` berubah. Perubahan XML tepat
cocok dengan lokasi/properti berstatus `applied` dalam CSV. Ini mendukung
hubungan sumber-output secara kuat, bukan hanya kesamaan nama file.
CSV tidak memuat identitas model, run API atau hash sumber; tidak dibuat
klaim mengenai model/klasifikasi AI yang dipakai pada run lama.

CSV run tersimpan memuat 3584 baris: **86 applied, 161 already_compliant,
2660 protected, 677 uncertain**. Angka ini bukan 91 operasi pada laporan
mock terdahulu; kedua hasil tidak disamakan. Tidak dibuat hasil pengujian
formatter baru, tidak menjalankan API, dan file yang ditemukan tidak diubah
atau dihapus.

### Bukti yang dipertahankan dan diperiksa kembali

Folder bukti privat, diabaikan Git:

`private_tests/t13_real_acceptance_20261125_235720/`

Berisi `source_before.docx`, `beta_after.docx`, `beta_operations.csv`, dua PDF
hasil ekspor Word, 86 PNG `before-*`, 86 PNG `after-*`, dan empat PNG
`compare-29/31/33/34`. Bukti mesin tersedia dalam `integrity_evidence.json`,
`word_comparison.json`, `render_comparison.json`, `acceptance_review.json`
dan `search_evidence.json`.

Pada finalisasi, seluruh file bukti utama dan empat gambar perbandingan
masih tersedia. Urutan PNG masing-masing lengkap 1–86. Hash PNG yang ada
mengonfirmasi **82 pasangan identik per byte**, sementara empat pasangan
yang berbeda tepat 29/31/33/34, sesuai catatan perbandingan pixel sebelumnya.
Tidak ada render baru untuk memperoleh hasil tersebut.

Hash sumber asli, unduhan sumber, output Beta, CSV asli dan salinan analisis
kembali cocok dengan manifest. SHA-256 sumber tesis:
`[hash tersedia pada manifest privat]`.
SHA-256 output Beta:
`[hash tersedia pada manifest privat]`.

### Hasil teknis yang terverifikasi

| Pemeriksaan | Hasil before / after | Status terbatas |
|---|---|---|
| Layout Word | 86 / 86 halaman, Word 16.0 build 16.0.20625; salinan dibuka read-only, repaginate, diekspor dan ditutup tanpa menyimpan pada sesi sebelumnya | PASS TERBATAS |
| Struktur | 896 / 896 paragraf, 29 / 29 tabel, 15 / 15 gambar inline, 2 / 2 section portrait | PASS TERBATAS |
| Seluruh teks dan isi tabel | Seluruh node teks Word dan teks paragraf sama; seluruh XML tabel sama. Pemeriksaan XML utama setelah hanya properti format yang dilaporkan disisihkan juga sama | PASS TERBATAS untuk integritas, bukan penilaian isi ilmiah |
| Gambar dan komponen paket | Seluruh 12 bagian media identik; 15 objek inline dapat memakai media bersama. Seluruh bagian paket selain XML utama identik, termasuk header/footer, relasi dan objek tertanam | PASS TERBATAS untuk integritas |
| Font, section dan margin | Font/run, XML section, orientasi, gutter sekitar 1 cm dan mirror margins dipertahankan; tidak ada koreksi font atau margin pada run tersimpan ini | PASS TERBATAS untuk preservasi; interpretasi margin efektif tetap perlu review |
| Pagination dan posisi objek | Awal/akhir halaman seluruh 896 paragraf sama, rentang halaman seluruh tabel sama, halaman/ukuran seluruh gambar inline sama; metadata section/header/footer Word sama | PASS TERBATAS |
| Perbandingan visual | 86 pasangan render Word pada skala maksimum 1250 px dibandingkan: 82 identik; empat halaman berbeda telah diperiksa berdampingan pada sesi sebelumnya | PASS TERBATAS pada pasangan/resolusi/lingkungan ini |
| Heading, caption dan nomor halaman | XML di luar properti target identik, 39 kandidat caption tetap pada halaman fisik yang sama; perbedaan pixel hanya berada pada paragraf indentasi target. Tidak teramati pemisahan caption/objek baru atau perubahan penomoran baru | PASS TERBATAS untuk tidak adanya perubahan baru, bukan kepatuhan seluruh caption/field |
| Kerusakan baru | Tidak ditemukan kehilangan/perubahan teks, tabel atau media. Tidak teramati clipping atau pergeseran objek baru pada empat halaman yang berbeda | Tidak ada FAIL baru yang terbukti pada pasangan ini |

Nilai 1250 px adalah skala maksimum render halaman; bukan jaminan pemeriksaan
setiap glyph pada semua tingkat pembesaran. Pixel identik membuktikan tidak
ada perubahan raster pada skala tersebut, bukan bahwa baseline bebas masalah.

### Operasi formatter yang sesuai bukti

- **82 operasi LAY-017 pada 82 paragraf:** properti spasi eksplisit menjadi
  1,0; seluruh nilai hasil diperiksa terhadap CSV dan XML. Normalisasi properti
  ini tidak menghasilkan perubahan raster halaman tambahan pada pengukuran.
- **4 operasi LAY-018**, termasuk dalam 82 paragraf tersebut, memperbaiki
  indentasi baris pertama menjadi sekitar 1 cm (567 twip):

| Paragraf | Halaman fisik | Indentasi sebelum | Sesudah |
|---|---:|---:|---:|
| 386 | 29 | 1,27 cm | sekitar 1 cm |
| 401 | 31 | sekitar 0,926 cm | sekitar 1 cm |
| 410 | 33 | sekitar 0,926 cm | sekitar 1 cm |
| 414 | 34 | sekitar 0,926 cm | sekitar 1 cm |

Empat perbedaan visual yang sudah ditinjau berada pada paragraf target
tersebut. Reflow teks di halaman 29 sesuai perubahan indentasi; tabel,
caption dan objek di luar target tidak bergeser. Halaman 31, 33 dan 34
memperlihatkan perubahan posisi awal baris sesuai indentasi. Tidak ada
perubahan jumlah halaman. Angka 82 paragraf dan 82 halaman identik adalah
dua ukuran berbeda dan tidak boleh disamakan.

### Pemisahan masalah baseline, perubahan dan persetujuan

- **Baseline:** halaman kosong fisik 2/4 pada tesis dan catatan caption/objek
  terpisah pada fixture S2 berasal dari pemeriksaan sebelumnya. Tidak
  diperbaiki atau dianggap sebagai kerusakan baru oleh run tesis ini.
- **Perubahan diharapkan:** 86 operasi properti di atas cocok dengan CSV,
  XML dan empat perubahan visual; hanya perubahan tersebut yang diklaim.
- **Kerusakan baru:** tidak terbukti pada pemeriksaan konten, inventaris dan
  raster pasangan tersimpan ini. Temuan ini tidak menjamin semua dokumen aman.
- **Persetujuan operator:** belum diterima untuk cakupan pemformatan otomatis
  tesis. Diagnostik lokal sebelumnya masih menempatkan 82 paragraf sebagai
  kandidat berstatus `uncertain`; pemilihan kandidat/CSV/label AI bukan
  ground truth atau izin baru untuk formatter. PASS teknis tidak mengubah
  pengamanan, cakupan otomatis maupun status aturan yang belum didukung.

### Klarifikasi halaman 4 S2 dan komponen yang tertunda

`docs/TASKS.md` mengarahkan T13 ke laporan dan checklist. Checklist
`T13_WORD_CHECKLIST.md` merujuk catatan T5; tabel `T5_REPORT.md` menautkan S2
ke fixture sintetis `tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx`
dan mencatat "Review halaman 4". Tidak ditemukan aturan PPKI pada sumber
catatan tersebut yang menjadikan halaman fisik 4 setiap tesis sebagai target.

Sumber tugas tidak menjelaskan versi input/output, artefak terkait, atau
apakah nomor itu fisik maupun tercetak. Baseline fixture S2 sebelumnya
terukur 3 halaman; tidak diuji ulang. Item historis ini tetap **PENDING
MANUAL REVIEW** sampai operator menjelaskan artefak/halaman yang dimaksud.
Halaman fisik 4 tesis privat yang kosong bukan penggantinya.

Yang masih menghalangi penutupan seluruh T13:

1. Persetujuan operator atas kelayakan cakupan pemformatan otomatis dan
   penerimaan akhir hasil tesis, terpisah dari preservasi teknis.
2. Penyelesaian item historis halaman 4 S2 berdasarkan artefak yang tepat.
3. Cakupan objek kompleks yang belum teruji: tesis ini tidak mempunyai
   footnote aktif, persamaan native Word atau section landscape; preservasi
   field/objek tidak membuktikan seluruh perilaku update field atau semua
   variasi konstruksi Word. Status yang belum diuji tetap PENDING MANUAL REVIEW.

Acceptance teknis before/after tesis **PASS TERBATAS**; seluruh T13
**PARTIAL**. Belum ada dasar menutup T13 atau menyatakan otomatisasi penuh/
rilis produksi siap. Langkah berikut tetap T13: review akhir operator atas
pasangan tesis yang sudah tersedia, terutama cakupan 82 paragraf dan empat
halaman perubahan, beserta penjelasan item halaman 4 S2.

Hanya laporan ini dan `WORK_PROGRESS.md` diperbarui pada finalisasi. Perubahan
Git sebelumnya (`tests/test_pilot.py`, `scripts/`, dan tes fixture baru) tetap
ada; HEAD tetap `e525e57`. `git diff --check` lulus. Pytest tidak diulang;
**274 passed** adalah hasil regresi terakhir yang sudah tersedia. Tidak ada
perubahan tesis, aturan JSON, kode/T14, API, pull, commit, push, reset, clean
atau penghapusan artefak.

## Halaman kosong margin dan baseline tesis privat — 25 November 2026

**T13 tetap PARTIAL.** Penyebab halaman kedua pada fixture margin telah
terverifikasi sebagai desain fixture; formatter tidak menambahkan halaman
kosong baru. Baseline tesis privat berhasil diperiksa terbatas dengan mesin
layout Word, tanpa menjalankan formatter atau membuat klaim hasil Beta tesis.

### Fixture margin: sebab halaman kedua

`build_margin_before()` pada `scripts/t13_fixtures.py` menambahkan section
kedua dengan `doc.add_section(WD_SECTION_START.NEW_PAGE)` setelah gambar.
Section baru tidak diberi teks, tabel atau gambar. Paragraf kosong pembawa
section break dan final `sectPr` memang sudah ada pada input. Tidak ditemukan
page break eksplisit `w:br type="page"`; ini bukan halaman tambahan hasil
hitung page break atau overflow objek yang baru disebabkan formatter.

Bukti sebelum/sesudah:

- Word COM: **2 halaman, 2 section** pada kedua file; section 1 halaman 1,
  section 2 halaman 2, `SectionStart=2` (New Page) pada keduanya.
- Word COM: body section 2 kosong setelah karakter kontrol dibuang; header dan
  footer section 2 `LinkToPrevious=True`, sehingga keduanya masih terlihat.
- Setelah hanya empat atribut margin pada section 1 disisihkan, seluruh
  `word/document.xml` sebelum dan sesudah identik. Tidak ada section break,
  paragraf atau page break baru dari formatter.
- Empat halaman PDF hasil ekspor Word ditinjau sebagai PNG. Halaman 1 memuat
  teks/tabel/gambar yang sama dengan posisi mengikuti margin baru. Halaman 2
  hanya header/footer; PNG halaman 2 sebelum dan sesudah **identik per byte**.
- **PASS terbatas:** formatter tidak menambahkan halaman kosong baru pada
  pasangan ini. Fixture dan formatter tidak diubah pada pemeriksaan ini.
  Section kosong dipertahankan karena sengaja menguji dua section dengan
  pengaturan halaman berbeda, bukan dokumen yang perlu dibersihkan.

### Sumber, metode dan integritas baseline

Sumber privat: `private_tests/tesis_uji.docx`. Pencarian DOCX di folder
`private_tests` hanya menemukan tesis input, hasil pilot Dummy Master dan
fixture T13 beserta cadangannya; tidak ditemukan output Beta tesis yang
relevan. Hasil Dummy Master bukan hasil tesis dan tidak dipakai sebagai
pembanding. Tidak dijalankan ulang AI atau formatter tesis.

Salinan byte-identik, PDF ekspor Word, PNG lokal dan bukti mesin disimpan pada
folder privat yang diabaikan Git:

`private_tests/t13_baseline_20261125_234928/`

Bukti: `word_evidence.json` (inventaris COM) dan `review_observations.json`
(cakupan pengamatan visual). Empat salinan DOCX dibuka read-only di instance
Word tanpa dokumen awal, direpaginate, kemudian diekspor melalui
`ExportAsFixedFormat` menjadi PDF lokal. Word **16.0 build 16.0.20625** dipakai;
PDF juga mencatat produsen Microsoft Word dan 86 halaman untuk tesis.
Dokumen ditutup dengan `Close(0)` tanpa menyimpan. Tidak ada `Fields.Update`
yang dipanggil secara eksplisit; hasil field tidak dinyatakan tervalidasi penuh.

Hash sumber sebelum/sesudah dan hash salinan cocok:

| Sumber | SHA-256 |
|---|---|
| Tesis privat | `[hash tersedia pada manifest privat]` |
| Fixture S2 asli | `[hash tersedia pada manifest privat]` |

Kedua fixture margin juga tetap memiliki SHA-256 yang tercatat pada bagian
penghitungan halaman sebelumnya. Tidak ada perubahan dokumen sumber, gutter,
mirror margins, formatter, kode tes atau 317 aturan JSON pada tahap ini.

### Hasil baseline tesis privat (bukan hasil formatter)

Semua nomor halaman berikut adalah **halaman fisik Word/PDF**, bukan nomor
halaman tercetak yang dapat dimulai ulang antar-section.

| Komponen | Bukti yang diperoleh | Status / batas pemeriksaan |
|---|---|---|
| Pembukaan dan jumlah halaman | Word membuka salinan read-only, repagination dan ekspor PDF berhasil; 86 halaman | PASS untuk pembukaan/render dan pengukuran baseline ini |
| Section dan orientasi | 2 section portrait; section 1 halaman 1–16, section 2 halaman 17–86 | PASS untuk inventaris; tidak menguji peralihan landscape |
| Gutter/mirror | Kedua section gutter 28,35 pt (sekitar 1 cm), mirror margins aktif | Dicatat, tidak diperbaiki; interpretasi margin efektif tetap PENDING MANUAL REVIEW |
| Header/footer dan nomor halaman | COM menemukan field PAGE pada header primer/genap kedua section; section 2 restart 1 terkonfigurasi. Pada sampel render tampak nomor 2 di halaman fisik 18, 12 di halaman 28, 35 di halaman 51 dan 64/65 di halaman 80/81 | PARTIAL: struktur dan sampel render diperiksa; seluruh variasi header/footer dan penomoran awal belum diluluskan |
| Heading dan caption | Daftar isi/daftar objek terlihat pada halaman 14–16; heading BAB di 17 dan heading akhir di 82/86; caption tabel/gambar terlihat pada halaman sampel | PARTIAL: tidak mengklaim seluruh urutan, rujukan, kapitalisasi atau kepatuhan aturan |
| Tabel | COM menghitung 29 tabel. Sampel halaman 11, 28–29, 50–51, 68, 80–81 memperlihatkan sel dan tabel; tabel lanjutan pada 29/51 diberi label lanjutan | PARTIAL: tidak tampak pemotongan jelas pada sampel, tetapi seluruh sel/baris belum diverifikasi satu per satu |
| Gambar/grafik/objek mengambang | 15 inline shapes dan 43 floating shapes menurut COM; diagram/grafik ditinjau antara lain pada 18, 36, 48, 50–51, 59 dan 68 | PARTIAL: sampel terlihat, detail semua floating shape dan objek tertanam belum tervalidasi |
| Field | COM menghitung 201 field body; instruksi XML mencakup TOC, PAGEREF dan SEQ; daftar isi/caption terlihat pada render sampel | PARTIAL: keberadaan terverifikasi, seluruh hasil/tautan field dan pembaruan field belum diuji |
| Footnote/endnote | COM: 0 footnote dan 0 endnote; part footnotes hanya memuat separator dan continuationSeparator | Tidak ada footnote aktif untuk diuji; dukungan visual footnote tetap belum teruji, bukan PASS |
| Persamaan | COM OMaths=0; tidak ditemukan OMML pada part Word XML yang diperiksa | Tidak ada persamaan native untuk diuji; konten matematis dalam gambar tidak disimpulkan dari hitungan ini |
| Landscape | COM: 0 section landscape | Tidak teruji pada tesis ini; checklist landscape tetap PENDING MANUAL REVIEW |
| Halaman kosong baseline | Halaman fisik 4 tampak kosong pada render; thumbnail juga memperlihatkan halaman 2 kosong. Tidak ada formatter tesis yang dijalankan | Temuan baseline untuk review operator; tidak diklaim sebagai kerusakan formatter atau langsung dihapus |
| Clipping/overlap | Thumbnail seluruh 86 halaman ditinjau, 19 halaman diperiksa satu per satu sebagai PNG | PARTIAL: pada sampel tidak terlihat clipping/overlap jelas; tidak menjamin seluruh glyph, sel atau objek pada 86 halaman |
| Before/after tesis | Pada tahap baseline output belum ditemukan; kemudian ditemukan di Downloads | Hasil terbaru: PASS TERBATAS teknis, lihat finalisasi 26 November 2026; persetujuan operator masih PENDING |

Halaman yang ditinjau satu per satu pada skala render lebih besar:
**4, 11, 14, 15, 16, 17, 18, 28, 29, 36, 48, 50, 51, 59, 68, 80, 81, 82, 86**.
Contact sheet seluruh 86 halaman hanya merupakan tinjauan umum; tidak
menggantikan pemeriksaan detail setiap halaman. Tidak ada PASS keseluruhan
untuk objek kompleks atau acceptance tesis nyata.

### Item checklist halaman 4 S2

Item ini pada `T5_REPORT.md` merujuk fixture sintetis
`tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx`, bukan otomatis halaman
4 tesis privat. Baseline fixture S2 yang tersedia kini menghasilkan **3 halaman,
1 section**, 1 tabel dan 1 gambar di Word; ketiga halaman render ditinjau.
Tabel terlihat pada halaman 2, gambar pada halaman 3. Caption gambar berada di
akhir halaman 2 dan gambarnya pada halaman 3: ini temuan baseline tentang
pemisahan caption/objek, perlu review; bukan efek formatter pada sesi ini.

Tidak ada halaman fisik 4 pada baseline fixture S2 ini. Versi hasil acceptance
yang dimaksud oleh catatan lama belum tersedia untuk dibandingkan. **Review
halaman 4 S2 tetap PENDING**, tidak digantikan oleh pemeriksaan halaman 4 tesis
privat yang kosong. Tidak dibuat output formatter baru hanya untuk merekayasa
halaman keempat.

### Ringkasan status sesi

- **PASS terbatas:** sebab halaman kedua margin terverifikasi sebagai desain,
  tidak ada halaman kosong baru dari formatter; pembukaan/render baseline dan
  inventaris halaman/section Word berhasil; integritas sumber terjaga.
- **PARTIAL:** pemeriksaan visual baseline tesis dan objeknya; seluruh T13.
- **FAIL:** tidak ada kegagalan baru formatter yang terbukti pada cakupan sesi.
  Halaman kosong baseline dan caption/objek terpisah dicatat sebagai temuan
  review, bukan otomatis FAIL kepatuhan PPKI atau akibat formatter.
- **PENDING MANUAL REVIEW:** before/after tesis, acceptance nyata, pemeriksaan
  detail semua objek/halaman, field, landscape dan item halaman 4 S2.

`git diff --check` lulus. Pytest tidak diulang karena tidak ada perubahan kode;
regresi terakhir tetap **274 passed**. Hanya dua laporan diperbarui pada Git;
artefak diagnosis tersimpan lokal pada folder privat di atas. Tidak ada API,
pull, commit atau push. Langkah T13 berikutnya adalah review operator terhadap
baseline/temuan tersebut dan menyediakan hasil Beta tesis yang benar-benar
terkait bila hendak melakukan acceptance before/after.

## Penghitungan halaman melalui Microsoft Word — 25 November 2026

**Jumlah halaman terverifikasi menggunakan mesin layout Word**, bukan jumlah
page break, metadata jumlah halaman DOCX, atau perkiraan struktur XML.
Word COM tersedia pada sesi Windows ini: versi **16.0**, build
**16.0.20625**. Setiap salinan sementara dibuka dengan `ReadOnly=True`
(diperiksa kembali melalui properti dokumen), kemudian dipanggil
`Document.Repaginate()` dan `Document.ComputeStatistics(2, false)`
(`wdStatisticPages`). Dokumen ditutup dengan `Close(0)` tanpa penyimpanan.

| Fixture | Jumlah halaman Word | Verifikasi |
|---|---:|---|
| `font_sebelum.docx` | 1 | Terverifikasi Word COM pada salinan byte-identik |
| `font_sesudah.docx` | 1 | Terverifikasi Word COM pada salinan byte-identik |
| `margin_sebelum.docx` | 2 | Terverifikasi Word COM pada salinan byte-identik |
| `margin_sesudah.docx` | 2 | Terverifikasi Word COM pada salinan byte-identik |

Percobaan pertama pada path asli menghasilkan 2 halaman untuk masing-masing
fixture margin. Pada kedua fixture font, pembacaan hash biasa gagal karena
file sedang dipakai proses lain dan Word tidak mengonfirmasi read-only;
penghitungan font dibatalkan. Output perbandingan hash font pada percobaan
awal tidak sah karena kedua pembacaan gagal; output tersebut tidak digunakan
sebagai bukti integritas.

Percobaan kedua membaca byte sumber menggunakan akses baca dengan file sharing,
membuat empat salinan sementara, dan memverifikasi SHA-256 setiap salinan
terhadap sumber sebelum dibuka di Word. Keempat penghitungan dalam tabel
berasal dari percobaan kedua yang berhasil. Salinan diagnosis berada di:

`<folder-temporer-lokal>/ppki_t13_pages_fb54f9c1eb564798a3d78a5fca415027/`

SHA-256 file asli sebelum dan sesudah percobaan kedua identik:

| Fixture | SHA-256 sumber sebelum = sesudah |
|---|---|
| `font_sebelum.docx` | `[hash tersedia pada manifest privat]` |
| `font_sesudah.docx` | `[hash tersedia pada manifest privat]` |
| `margin_sebelum.docx` | `[hash tersedia pada manifest privat]` |
| `margin_sesudah.docx` | `[hash tersedia pada manifest privat]` |

Tidak ada penyimpanan perubahan pada file pengujian, modifikasi tesis,
perubahan keamanan Word, panggilan API, commit atau push. Angka tersebut berlaku
untuk fixture dan lingkungan Word saat pengukuran; tidak memverifikasi posisi
objek pada setiap halaman. Jumlah halaman tidak berubah dalam kedua pasangan,
tetapi page break visual, clipping/overlap, objek kompleks dan acceptance tesis
nyata tetap **PENDING MANUAL REVIEW**. T13 tetap **PARTIAL**.

Jika perlu memeriksa manual, buka file di Word lalu tekan **Ctrl+P** untuk
Print Preview. Tunggu preview selesai, lalu lihat indikator halaman di bawah
preview (misalnya `1 of 2` / `1 dari 2`); tombol panah dapat digunakan untuk
meninjau tiap halaman. Tidak perlu menekan Print atau menyimpan dokumen.

Hanya laporan T13 dan `WORK_PROGRESS.md` diperbarui. `git diff --check` lulus;
pytest tidak diulang karena kode tidak berubah. Regresi terakhir tetap
**274 passed** dari tahap perbaikan fixture.

## Bukti operator setelah perbaikan fixture — 25 November 2026

Sumber bukti: laporan langsung pengguna dalam percakapan ini setelah membuka
keempat fixture pengganti di Microsoft Word. Screenshot disebut oleh operator,
tetapi tidak dilampirkan pada pesan ini dan tidak diperiksa langsung oleh
Codex. Status berikut berdasarkan verifikasi operator, bukan otomatisasi Word.
Versi Word, nomor halaman temuan dan jumlah halaman belum diberikan; tanggal
ini adalah tanggal pencatatan laporan, bukan tanggal pengujian yang dikonfirmasi.

| Pemeriksaan | Bukti yang diberikan operator | Status dan cakupan |
|---|---|---|
| Pembukaan empat fixture | `font_sebelum.docx`, `font_sesudah.docx`, `margin_sebelum.docx`, `margin_sesudah.docx` semuanya terbuka tanpa error Word | PASS terverifikasi operator untuk pembukaan empat file tersebut |
| Font target hasil | Toolbar Word pada paragraf target `font_sesudah.docx` menunjukkan Times New Roman 12 pt | PASS terverifikasi operator untuk font/ukuran target hasil; nilai Arial 11 pada file sebelum tetap didukung tes otomatis, belum dikonfirmasi terpisah melalui toolbar oleh operator |
| Bold, Italic, Justify | Ketiganya tetap terlihat pada paragraf target hasil | PASS terverifikasi operator untuk tiga format tersebut; spasi 1,0, indentasi 1 cm dan seluruh pembungkusan teks masih PENDING MANUAL REVIEW |
| Margin hasil | Page Setup `margin_sesudah.docx`: Left 4 cm, Right 3 cm, Top 3 cm, Bottom 3 cm, Gutter 0 cm, Portrait, Multiple pages Normal | PASS terverifikasi operator untuk pengaturan yang dilaporkan; cakupan setiap section dan ukuran kertas belum dikonfirmasi terpisah |
| Heading, teks, tabel, gambar | Operator menyatakan terlihat pada screenshot sebelum/sesudah tanpa kerusakan yang jelas | Pengamatan visual dasar tercatat; bukan PASS pemeriksaan seluruh objek atau seluruh halaman |
| Jumlah halaman / pagination | Operator belum memberikan angka; penghitungan Word COM berikutnya memverifikasi font 1/1 dan margin 2/2 | Jumlah halaman terverifikasi Word COM; pagination visual rinci PENDING MANUAL REVIEW |
| Objek kompleks | Belum ada hasil pemeriksaan rinci field PAGE, header/footer, footnote, persamaan, hyperlink atau objek kompleks lain | PENDING MANUAL REVIEW |
| Acceptance tesis nyata | Belum ada hasil acceptance tesis nyata | PENDING MANUAL REVIEW |

Hambatan pembukaan fixture pengganti terselesaikan menurut bukti operator.
Temuan ini tidak menentukan cacat mana yang menjadi satu-satunya penyebab error
file lama dan tidak menjamin kompatibilitas seluruh dokumen Word. Margin tesis
dengan gutter/mirror tetap di luar persetujuan fixture ini dan tetap perlu review.

Pembaruan ini hanya mengubah laporan ini dan `WORK_PROGRESS.md`. Tidak ada kode,
aturan JSON, fixture atau dokumen asli yang diubah. Tidak ada panggilan API,
pull, commit atau push. Pytest tidak diulang untuk pembaruan dokumentasi ini;
regresi terakhir tetap **274 passed** dari tahap perbaikan fixture.

## Perbaikan fixture setelah error pembukaan Word — 25 November 2026

Operator melaporkan `font_sebelum.docx` lama gagal dibuka dengan pesan
**"Word experienced an error trying to open the file."** Ini bukti kegagalan
pembukaan file lama. Pada tahap regenerasi, pembukaan pengganti masih PENDING.
Laporan operator terbaru di atas kemudian mengonfirmasi keempat pengganti
terbuka tanpa error; font dan margin hasil PASS dalam cakupan yang dilaporkan.
Checklist di bawah berlaku untuk file pengganti.

### Diagnosis yang terbukti

| File lama | Ukuran (byte) | ZIP CRC / parsing semua XML | Cacat tambahan yang ditemukan |
|---|---:|---|---|
| `font_sebelum.docx` | 36214 | Lulus | `word/document.xml` memuat `<w:fldSimple/>` tanpa `w:instr` |
| `font_sesudah.docx` | 36237 | Lulus | Field tanpa `w:instr` yang sama tetap terbawa |
| `margin_sebelum.docx` | 36984 | Lulus | `word/media/image1.png`: CRC internal chunk `IDAT` salah |
| `margin_sesudah.docx` | 36972 | Lulus | CRC PNG salah yang sama tetap terbawa |

Content Types, tipe utama DOCX, target internal relationships, referensi
relationship XML, dan keberadaan document/body/section diperiksa pada keempat
file. Tidak ditemukan target paket yang hilang pada pemeriksaan tersebut.
CRC ZIP yang benar tidak mendeteksi CRC internal gambar yang salah.

`tests/test_pilot.py:sample()` membuat field kosong yang sama dengan fixture
font lama. Generator khusus empat fixture lama tidak ditemukan pada sumber
Python repository yang diperiksa; asal tepat proses ad hoc sebelumnya tidak
dapat dibuktikan. Sampel tes tersebut sekarang menyertakan instruksi PAGE.
[Dokumentasi Microsoft tentang simple field](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.simplefield?view=openxml-3.0.1)
menjelaskan instruksi field; [skema field yang dipublikasikan Microsoft](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oi29500/34477fff-355a-497e-a2bf-4b9c3f80b093)
menandai atribut `instr` sebagai wajib.

Dua cacat tersebut terbukti pada fixture. Hubungan sebab-akibat tunggal dengan
pesan error Word tetap belum dapat dipastikan secara terpisah; operator kini
mengonfirmasi file pengganti dapat dibuka.
Tidak ada kesimpulan bahwa Microsoft Word rusak, dan tidak ada pengaturan
keamanan Word yang diubah.

### Cadangan dan regenerasi

Sebelum mengganti file, keempat versi lama disalin ke:

`private_tests/t13_word_validation/backup_20261125_233230_899476/`

Folder ini berisi empat DOCX asli dan `manifest.json` dengan ukuran serta
SHA-256. Hash seluruh cadangan diverifikasi terhadap sumber sebelum penggantian
dan diperiksa lagi setelahnya. Tidak ada fixture lama yang dihapus tanpa cadangan.

Generator yang dapat diulang tersedia di `scripts/t13_fixtures.py`:

```powershell
.\.venv\Scripts\python.exe -B -m scripts.t13_fixtures
```

Generator menggunakan `Document.save()` untuk kedua input sintetis baru,
kemudian formatter yang sudah ada untuk hasilnya. Seluruh paket pengganti
lulus pemeriksaan struktur sebelum file lama diganti. Setiap pemanggilan ulang
membuat folder cadangan baru. Tidak ada kode aplikasi/formatter produksi atau
aturan JSON yang diubah.

Pasangan font mempertahankan 6 paragraf, 1 tabel dan header; paragraf 3
Arial 11 bold/italic dikoreksi menjadi Times New Roman 12, spasi 1,0,
indentasi pertama 1 cm dan justified. Field PAGE memiliki instruksi dan hasil
tersimpan `1`, dikunci pada fixture untuk perbandingan stabil. Field ini
bukan pengujian pembaruan nomor halaman Word. Teks kedua versi pengganti sama,
termasuk hasil field, dan paragraf field tidak diubah oleh formatter.

Pasangan margin mempertahankan 3 paragraf, 2 section, 1 tabel, 1 gambar inline,
header dan footer. Section pertama tetap 20 x 28 cm, margin 2 cm sebelum
menjadi kiri 4 serta kanan/atas/bawah 3 cm; section kedua A4 bermargin sesuai
aturan tetap dipertahankan. Ukuran kertas section pertama sengaja bukan target
koreksi pada tes margin ini. Tabel sintetis baru dibuat selebar 10 cm agar muat
pada bidang tulisan setelah koreksi. PNG dibuat dengan zlib dan CRC chunk
yang benar, 32 x 32 piksel, ditampilkan selebar 1 cm agar dapat diperiksa.
Ukuran gambar lama sangat kecil; gambar/tabel baru setara untuk pengujian
perlindungan objek, bukan salinan visual persis fixture lama. Pasangan
sebelum/sesudah pengganti mempertahankan XML tabel serta byte gambar identik.

| Pengganti di `private_tests/t13_word_validation/` | Ukuran (byte) | Paket otomatis | Pembukaan Word menurut operator |
|---|---:|---|---|
| `font_sebelum.docx` | 36240 | Lulus pemeriksaan terarah | PASS terverifikasi operator: terbuka tanpa error |
| `font_sesudah.docx` | 36265 | Lulus pemeriksaan terarah | PASS terverifikasi operator: terbuka tanpa error |
| `margin_sebelum.docx` | 37023 | Lulus pemeriksaan terarah | PASS terverifikasi operator: terbuka tanpa error |
| `margin_sesudah.docx` | 37011 | Lulus pemeriksaan terarah | PASS terverifikasi operator: terbuka tanpa error |

### Verifikasi otomatis dan batasnya

`tests/test_t13_word_fixtures.py` mencakup empat paket, integritas teks/tabel,
byte seluruh komponen selain `word/document.xml`, perlindungan field,
font/paragraf/margin yang ditargetkan, idempotensi kedua pasangan, dan cadangan
sebelum penggantian. Tes negatif menolak instruksi field hilang, referensi
relationship hilang, target relationship hilang, ID relationship duplikat,
tipe utama keliru, XML rusak, part wajib hilang, serta PNG rusak meski CRC ZIP
benar. Pemeriksa ini khusus fixture T13, bukan validator skema OOXML lengkap.

Perintah dan hasil akhir:

- `.\.venv\Scripts\python.exe -B -m pytest tests/test_t13_word_fixtures.py -q -p no:cacheprovider`: **15 passed** (2,91 detik).
- `.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider`: **274 passed** (142,86 detik), termasuk tes pilot dan acceptance lama.
- Validasi ulang keempat file di disk: pemeriksaan paket terarah lulus; keempat cadangan cocok dengan hash manifest. Pemeriksa baru menolak masing-masing file lama sesuai dua cacat yang dilaporkan.
- `git diff --check`: lulus. Percobaan awal tes baru menemukan kesalahan unpack nilai balik
`format_margins` pada generator, diperbaiki sebelum regenerasi; tidak ada
fixture asli diganti pada percobaan gagal itu.

Word tidak diotomasi ulang pada tahap regenerasi (penghitungan COM yang berhasil dilakukan kemudian dicatat di atas); ekspor/render visual juga
tidak dijalankan. Pemeriksaan paket bukan bukti kompatibilitas Word. Bukti
pembukaan dan pengamatan visual yang diterima setelah regenerasi dicatat pada
bagian bukti operator di atas; checklist tetap memisahkan komponen yang belum
diperiksa. Pemeriksaan lanjutan menggunakan salinan read-only tanpa menyimpan
ulang sumber atau menonaktifkan keamanan Word.

## Dokumen dan operasi

Empat salinan sintetis tersedia di `private_tests/t13_word_validation/` (folder tidak masuk Git): `font_sebelum.docx`, `font_sesudah.docx`, `margin_sebelum.docx`, dan `margin_sesudah.docx`.

| Pasangan | Operasi formatter yang tercatat | Halaman sebelum / sesudah | Verifikasi visual |
|---|---|---|---|
| Font dan paragraf | Paragraf 3: LAY-005 Arial 11 menjadi TNR 12; LAY-017, 018 dan 019 memperbaiki spasi, indentasi dan perataan | 1 / 1 (Word COM) | PASS terverifikasi operator: TNR 12, Bold, Italic, Justify; spasi/indentasi masih PENDING MANUAL REVIEW |
| Margin | Section 1: LAY-008 kiri 2 ke 4 cm; LAY-009–011 kanan, atas dan bawah 2 ke 3 cm | 2 / 2 (Word COM) | PASS terverifikasi operator: margin hasil dan pengaturan Page Setup yang dilaporkan |

Operasi formatter dan integritas berikut merupakan bukti teknis; bukti visual operator kini tersedia hanya untuk cakupan yang dinyatakan di atas. Fixture font mempertahankan 6 paragraf, teks identik dan 1 tabel; fixture margin mempertahankan 3 paragraf, teks identik, 1 tabel dan 1 gambar inline. Seluruh komponen ZIP selain `word/document.xml` identik untuk masing-masing pasangan. Pengujian ini tidak menjamin tampilan gambar atau tabel.

## Percobaan Word

Bagian ini mencatat percobaan sesi sebelumnya. Pada pembaruan 25 November
2026 di workspace PC rumah (HEAD `e525e57`), Word tidak diotomasi atau dibuka
ulang. Saat checklist disiapkan, hasil pemeriksaan visual operator belum diberikan.
Laporan error pembukaan yang diterima kemudian dicatat pada bagian perbaikan di atas.

Word COM tidak dapat diinisialisasi di sesi ini: `0x80070520`, sesi logon tidak tersedia. Karenanya tidak ada pembukaan read-only melalui COM, hitungan halaman Word, atau PDF hasil ekspor. Tidak ada klaim bahwa pengaturan pencegahan macro/tautan berhasil diterapkan pada proses Word yang gagal dibuat.

Word terbuka lewat antarmuka dan memunculkan salinan Dummy Master berstatus **AutoRecovered**, bukan keempat fixture di atas. Salinan pemulihan tidak disimpan atau diubah. Fokus dialog pembukaan fixture tidak dapat diverifikasi secara andal, sehingga perbandingan tidak dilanjutkan. Tampilan AutoRecovered tersebut bukan bukti perbandingan sebelum/sesudah.

Tesis privat tidak dibuka pada sesi ini dan tidak dimodifikasi. Salinan hasil Beta tesis tidak ditemukan dalam `private_tests`; tidak ada panggilan API ulang. Margin tesis dengan gutter dan mirror tetap tidak diubah. LibreOffice tidak tersedia.

## Pemeriksaan operator yang masih diperlukan

### Checklist empat fixture — 25 November 2026

Repository berawal pada `main`, commit `e525e57`, dengan working tree dan
staging bersih. Keempat fixture ditemukan secara lokal. Pemeriksaan keberadaan
file tidak membuktikan tampilan di Word. Checklist kini diperbarui dari laporan
operator; PASS dibatasi pada font target, Bold/Italic/Justify, margin hasil
dan pembukaan empat file. Status lain tetap terpisah.

Buka setiap file melalui **Open Read-Only**, gunakan **Print Layout**, dan
bandingkan pasangan sebelum/sesudah pada versi Word serta pengaturan tampilan
yang sama. Tunggu Word selesai menghitung halaman. Jangan menyimpan ulang
fixture atau dokumen asli. Jika muncul AutoRecovered atau dialog perbaikan,
catat nama file dan pesan tersebut; jangan menganggapnya sebagai fixture yang
sudah diperiksa.

| File | Versi Word / tanggal / operator | Jumlah halaman Word | Hasil visual |
|---|---|---|---|
| `font_sebelum.docx` | Visual: pengguna, versi/tanggal uji belum diberikan; jumlah halaman: Word 16.0 build 16.0.20625, 25 November 2026 | 1 (Word COM) | Pembukaan PASS terverifikasi operator; cakupan visual lihat tabel komponen |
| `font_sesudah.docx` | Visual: pengguna, versi/tanggal uji belum diberikan; jumlah halaman: Word 16.0 build 16.0.20625, 25 November 2026 | 1 (Word COM) | Pembukaan PASS terverifikasi operator; cakupan visual lihat tabel komponen |
| `margin_sebelum.docx` | Visual: pengguna, versi/tanggal uji belum diberikan; jumlah halaman: Word 16.0 build 16.0.20625, 25 November 2026 | 2 (Word COM) | Pembukaan PASS terverifikasi operator; cakupan visual lihat tabel komponen |
| `margin_sesudah.docx` | Visual: pengguna, versi/tanggal uji belum diberikan; jumlah halaman: Word 16.0 build 16.0.20625, 25 November 2026 | 2 (Word COM) | Pembukaan PASS terverifikasi operator; cakupan visual lihat tabel komponen |

Isi hasil setiap komponen dengan halaman dan pengamatan yang spesifik. Nilai
harapan berasal dari operasi formatter; status dan catatan membedakan bukti
operator yang sudah diterima dari rincian yang belum diperiksa.

| Komponen | Pasangan font: sebelum dibanding sesudah | Status pasangan font | Pasangan margin: sebelum dibanding sesudah | Status pasangan margin |
|---|---|---|---|---|
| Font dan ukuran | Toolbar paragraf target hasil menunjukkan Times New Roman 12 pt; Bold/Italic tetap terlihat. Font sebelum belum dikonfirmasi tersendiri melalui toolbar | PASS terverifikasi operator untuk target hasil | Periksa font dan ukuran tidak berubah tanpa operasi yang tercatat | PENDING MANUAL REVIEW |
| Paragraf | Justify terlihat pada target hasil; spasi 1,0, indentasi 1 cm dan pembungkusan belum diverifikasi rinci | PASS terverifikasi operator untuk Justify; sisanya PENDING MANUAL REVIEW | Periksa format paragraf tetap sesuai; pembungkusan dapat berubah akibat lebar bidang tulisan | PENDING MANUAL REVIEW |
| Margin dan kertas | Periksa margin, ukuran kertas dan orientasi tidak berubah | PENDING MANUAL REVIEW | Page Setup hasil: kiri 4 cm, kanan/atas/bawah 3 cm, gutter 0 cm, Portrait, Multiple pages Normal; ukuran kertas dan pemeriksaan setiap section belum dilaporkan | PASS terverifikasi operator untuk pengaturan hasil yang dilaporkan; sisanya PENDING MANUAL REVIEW |
| Tabel | Operator: tabel terlihat tanpa kerusakan jelas; rincian seluruh sel/pemisahan halaman belum diperiksa | PENDING MANUAL REVIEW | Operator: tabel terlihat tanpa kerusakan jelas; rincian posisi/sel/pemisahan halaman belum diperiksa | PENDING MANUAL REVIEW |
| Gambar | Laporan struktur menyebut tidak ada gambar; konfirmasi di Word, tidak membuktikan dukungan gambar | PENDING MANUAL REVIEW | Operator: gambar terlihat tanpa kerusakan jelas; proporsi, clipping dan posisi pada seluruh halaman belum diverifikasi rinci | PENDING MANUAL REVIEW |
| Jumlah halaman dan pagination | Word COM: 1 halaman sebelum dan 1 sesudah; page break, halaman kosong, clipping/overlap masih perlu review | Jumlah halaman terverifikasi Word COM; visual rinci PENDING MANUAL REVIEW | Word COM: 2 halaman sebelum dan 2 sesudah; posisi tabel/gambar dan pemisahan halaman masih perlu review | Jumlah halaman terverifikasi Word COM; visual rinci PENDING MANUAL REVIEW |
| Elemen lain | Periksa heading, subheading, caption, header/footer dan nomor halaman jika ada; nyatakan bila tidak ditemukan | PENDING MANUAL REVIEW | Periksa heading, subheading, caption, header/footer dan nomor halaman jika ada; nyatakan bila tidak ditemukan | PENDING MANUAL REVIEW |

Format hasil operator yang dapat disalin untuk masing-masing file:

```text
File:
Tanggal / operator / versi Word:
Dibuka Read-Only dan Print Layout:
Jumlah halaman setelah pagination selesai:
Font dan ukuran (halaman / hasil):
Paragraf (halaman / hasil):
Margin, kertas dan orientasi (section / hasil):
Tabel (halaman / hasil):
Gambar (halaman / hasil, atau tidak ditemukan):
Heading/caption/header/footer/nomor halaman (halaman / hasil, atau tidak ditemukan):
Page break, halaman kosong, teks terpotong/bertumpuk (halaman / hasil):
Komponen yang belum diperiksa:
```

PASS hanya dapat dicatat untuk komponen yang secara eksplisit telah diperiksa
dan didukung pengamatan operator atau bukti visual yang terkait file serta
halaman. Pernyataan umum seperti "file terbuka" tidak meluluskan seluruh
komponen. Perubahan jumlah halaman bukan otomatis FAIL atau PASS: penyebabnya
harus diperiksa. Elemen yang dipastikan tidak ada dicatat sebagai tidak ada /
tidak teruji, bukan PASS. Temuan masalah dicatat beserta halaman dan cakupannya;
komponen yang belum diperiksa tetap **PENDING MANUAL REVIEW**.

### Cakupan acceptance yang masih terbuka

Lulus pada dua pasangan sintetis ini saja belum menutup T13. Checklist umum
di `T13_WORD_CHECKLIST.md`, perbandingan Dummy Master, review halaman 4 S2,
serta acceptance dokumen nyata anonim dalam `T13_REPORT.md` masih menunggu
bukti. Fixture sederhana tidak membuktikan keamanan semua struktur Word.

1. Buka pasangan fixture sebagai **Open Read-Only** di Word; jangan menyimpan ulang sumber.
2. Catat jumlah halaman dan periksa apakah perubahan posisi teks dan pembungkusan sesuai operasi yang tercatat.
3. Periksa font/ukuran, heading, subheading, caption, tabel, gambar, header, footer dan nomor halaman. Fixture font tidak memiliki gambar; fixture margin memiliki gambar sintetis kecil, sehingga Dummy Master juga perlu diperiksa.
4. Periksa pemisahan halaman, teks terpotong atau bertumpuk, serta tabel/gambar yang bergeser. Dokumentasikan nomor halaman dan penyebab yang diduga jika ditemukan masalah.
5. Untuk tesis, gunakan salinan read-only dan periksa halaman bertabel/bergambar; jika hasil Beta asli tersedia, bandingkan dengannya tanpa mengulang API. Jangan memperbaiki margin ambigu sebelum interpretasi gutter/mirror disetujui.

Status visual terbaru: operator tidak melihat kerusakan yang jelas pada heading, teks, tabel dan gambar yang dibandingkan. Temuan ini tidak menutup pemeriksaan rinci objek kompleks atau seluruh halaman. Regresi otomatis terakhir **274 passed** pada tahap perbaikan fixture; pytest tidak diulang untuk pencatatan bukti operator. T13 tetap **PARTIAL**.

Pembaruan checklist awal 25 November 2026 hanya menambahkan checklist dan status bukti pada
dokumentasi. Tidak ada fixture atau tesis yang diubah, tidak ada percobaan
Word COM ulang, dan tidak ada pull, commit, push atau panggilan OpenAI API.
