# Progres Automatic Safe Formatting

26 November 2026 — handoff aman ke laptop: kode generator, tes fixture,
koreksi field sintetis dan laporan acceptance disiapkan untuk sinkronisasi
GitHub. Beta v0.5.1 sudah ada di baseline Git, tidak diimplementasikan ulang.
Nama berkas beridentitas pribadi, path profil Windows dan fingerprint DOCX
privat disamarkan pada laporan repository. Laporan lengkap sebelum penyamaran
dicadangkan di `private_tests/github_sync_original_reports_*`.
Seluruh tesis, varian 71, CSV/PNG/PDF/JSON bukti dan keputusan lokal di
`private_tests/` tidak ikut Git. .venv, cache, .env dan secrets juga dikecualikan.
Laptop perlu salinan privat yang dipindahkan pemilik secara terpisah untuk
melanjutkan acceptance berbasis artefak; jangan menganggap path laporan
sebagai file yang tersedia dari clone GitHub. Regresi historis 274 passed,
T13 keseluruhan tetap PARTIAL, penerimaan akhir file masih terbuka.

26 November 2026 — operator menerima terbatas cakupan 71 paragraf untuk
acceptance tesis uji, menahan semua format 11 ambigu dan mengecualikan semua
operasi 401. Tidak menerima Beta 82 sebagai hasil final atau mengizinkan
otomasi generik. Penerimaan akhir file tetap dipisahkan dari persetujuan scope.
Varian 71 tersimpan diverifikasi ulang: **71 spasi + 3 indentasi** pada
386/410/414; semua 11 dan seluruh 825 paragraf non-target identik XML sumber.
Teks/tabel/media/section/header/footer dan XML di luar properti target terjaga.
Word read-only mengonfirmasi kembali **86 halaman, 2 section, 29 tabel,
15 gambar inline** tanpa menyimpan. Render tersimpan 29/31/33/34 diperiksa
visual; 29/33/34 menunjukkan perubahan diharapkan, 31 identik sumber.
Tiga sampel tambahan saja (17,74,76) diekspor Word dan identik pixel dengan
sumber; tidak teramati clipping/overlap atau pergeseran objek baru pada tujuh
sampel. **Acceptance teknis varian 71: PASS TERBATAS**; 79 halaman lain tidak
diluluskan sebagai identik tanpa render/bukti baru. Varian SHA-256 tetap
`[hash tersedia pada manifest privat]`.
Keputusan terbatas dan bukti akhir ada pada folder eksperimen:
`limited_scope_final_technical_acceptance.json`, `final_word_check.json`,
`final_sample_comparison.json` serta tiga PDF/PNG tambahan. Label filename
awal NOT_OPERATOR_APPROVED dipertahankan untuk menjaga artefak/hash; status
cakupan terkini dicatat terpisah, final file belum diberi sign-off operator.
T13 **PARTIAL**: penerimaan akhir file, artefak halaman 4 S2, cakupan objek
kompleks/field yang belum ditutup dan batas review visual tetap terbuka.
Langkah berikut: sign-off operator untuk varian 71 terikat hash dan batas
buktinya. Tidak ada formatter/rules/dokumen diubah, API, pull, commit, push,
pytest ulang atau render penuh. Regresi terakhir **274 passed**; dua laporan
diperbarui dan perubahan lokal sebelumnya dipertahankan.

26 November 2026 — persiapan keputusan operator T13: rekomendasi bersyarat
71 narasi dan pengecualian sementara 11 pengantar/enumerasi, seluruh keputusan
masih PENDING. LAY-018 dari JSON menyebut 1 cm secara umum tetapi tidak
menentukan perlakuan khusus pengantar daftar 401; rekomendasi pertahankan
sumber, termasuk indentasi sekitar 0,926 cm dan spasi asalnya.
Varian privat **EXPERIMENT_NOT_OPERATOR_APPROVED.docx** berhasil dibuat pada
`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/`
dari sumber awal melalui handler pilot lama, hanya aturan 017/018 dan scope
sementara 71 untuk eksperimen yang diminta. Tidak ada state/label persetujuan
operator atau izin produksi diperbarui. Tepat **74 operasi**: 71 spasi dan
3 indentasi (386/410/414). Semua 11 paragraf tertahan dan seluruh 825 paragraf
di luar scope identik XML dengan sumber; teks/tabel/media/bagian paket lain
serta struktur non-target terjaga. Sumber dan Beta lama tidak diganti.
Word read-only mengukur varian secara independen: **86 halaman, 2 section,
29 tabel, 15 gambar inline**. Empat render terfokus: halaman 31 identik
sumber karena 401 dipertahankan; 29/33/34 identik hasil Beta lama. Halaman lain
varian tidak dirender ulang; tidak diwarisi klaim visual penuh dari Beta 82.
Bukti JSON/Word dan tabel privat `operator_decision_11_private.csv` dengan
cuplikan asli tersedia di folder eksperimen. Laporan tracked hanya memuat
ringkasan konteks, tanpa menyalin cuplikan privat.
T13 **PARTIAL**, review akhir operator varian masih PENDING; item halaman 4 S2
dan kasus objek kompleks yang belum teruji tetap terbuka. Tidak ada formatter,
JSON aturan, tesis atau output Beta asli diubah, API, pull, commit atau push.
Tidak ada render 86 halaman/pytest ulang; regresi terakhir **274 passed**.

26 November 2026 — review cakupan 82 paragraf T13 selesai sebagai audit,
bukan persetujuan operator. Seluruh 82 dikenali sistem sebagai teks_isi,
style Normal, tanpa heading/numPr/field/tabel/objek kompleks pada target.
Preservasi teknis 82/82 terbukti; rekomendasi fungsi: **71 narasi berisiko
lebih rendah layak diterima bersyarat**, **11 perlu review kelompok**
(8 pengantar daftar/proposisi, 3 enumerasi Pertama/Kedua/Ketiga), **0 salah
kategori struktural yang terbukti wajib dikecualikan**. Sebelas kasus
sementara ditahan dari rekomendasi izin otomatis. Operator approved tetap
0, pending 82; keputusan kelompok tidak mengubah izin formatter.
Delapan pengantar: 307,314,319,326,373,401,764,769; tiga enumerasi:
757–759. Paragraf 401 juga menerima indentasi dan perlu perhatian khusus.
Item daftar bernomor di dekatnya dan proposisi 374–376 tercatat protected,
tidak ikut berubah. Audit 82 baris per lokasi/aturan/format/bukti/alasan/
operator tersedia dalam `private_tests/t13_real_acceptance_20261125_235720/`
`scope_82_operator_audit.csv` dan `scope_82_review_summary.json`.
Konsisten: 82 operasi spasi + 4 indentasi = 86 operasi pada 82 paragraf;
78 spasi saja, 4 spasi+indentasi. Nilai spasi langsung sebelumnya tidak
eksplisit, bukan terbukti salah; hasil eksplisit 1,0 tidak memberi perubahan
raster tambahan. Hanya empat halaman 29/31/33/34 berubah sesuai indentasi.
T13 **PARTIAL**, acceptance teknis **PASS TERBATAS**. Rekomendasi operator:
putuskan tiga kelompok, bukan 82 review individual; tahan 11 ambigu dan
klarifikasi halaman 4 S2 yang sumber T5-nya belum spesifik. Persetujuan
71 paragraf tidak otomatis menyetujui file Beta yang masih mencakup 82.
Tidak ada formatter/rules/dokumen diubah, API, render ulang, pytest ulang,
pull, commit atau push. Regresi terakhir **274 passed**. Dua laporan
memuat hasil dan batasnya; perubahan lokal sebelumnya dipertahankan.

26 November 2026 — finalisasi T13 dari bukti sesi yang terhenti usage limit,
bukan kegagalan pengujian. Output Beta tesis dan CSV sebelumnya ditemukan di
Downloads, berakhiran `_beta_formatted.docx` dan `_beta_operations.csv` pada
nama `tesis_privat`. Sumber unduhan identik
dengan tesis privat. Hubungan sumber-output diperkuat oleh 73 bagian paket,
72 bagian identik, serta perubahan XML utama yang tepat cocok dengan CSV.
Run tersimpan: **86 operasi pada 82 paragraf** (82 spasi 1,0 dan 4 indentasi
1 cm); bukan 91 operasi pada laporan mock lama. Tidak dibuat output baru.
Acceptance teknis before/after tesis: **PASS TERBATAS**. Word read-only
memverifikasi **86 → 86 halaman**, 896 paragraf, 29 tabel, 15 gambar inline,
2 section. Seluruh teks, XML tabel, bagian media dan konten di luar properti
target tetap utuh. Perbandingan 86 pasangan render Word 1250 px menghasilkan
**82 halaman identik**; perbedaan fisik **29, 31, 33, 34** sesuai empat
koreksi indentasi paragraf **386, 401, 410, 414**. Tidak teramati clipping,
pergeseran objek, pemisahan caption atau kerusakan konten baru. Pagination
paragraf, rentang halaman tabel, serta halaman/ukuran gambar tetap sama.
Bukti privat pada `private_tests/t13_real_acceptance_20261125_235720/`
masih lengkap: dua DOCX/PDF, 172 PNG, empat perbandingan, CSV dan JSON bukti.
Finalisasi memverifikasi kembali file/hashes, kelengkapan 86 pasangan dan
paket/konten, tanpa Word, render, formatter, fixture atau pytest ulang.
T13 keseluruhan tetap **PARTIAL**: persetujuan operator atas cakupan otomatis
belum diberikan; kasus objek kompleks yang tidak ada pada tesis belum teruji;
item "halaman 4 S2" pada checklist berasal dari fixture sintetis dalam T5,
tetapi versi artefak dan jenis nomor halaman tidak dijelaskan. Item itu
**PENDING**, bukan otomatis halaman fisik keempat tesis privat. Rincian dan
batas klaim ada di `T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`.
Hanya dua laporan diperbarui. Perubahan lokal sebelumnya tetap ada dan HEAD
`e525e57` dipertahankan. Tidak ada perubahan tesis asli, aturan, T14 atau API;
tidak ada pull, commit, push, reset, clean, penghapusan artefak maupun uji
fixture ulang. Regresi terakhir tetap **274 passed**; `git diff --check` lulus.
Langkah berikut: review akhir operator atas pasangan tesis tersimpan dan
cakupan otomatisnya untuk menutup acceptance T13, beserta klarifikasi S2.
Entri berikut merupakan riwayat sebelum hasil ini.

25 November 2026 — T13 lanjutan: halaman kedua pasangan margin berasal dari
section NEW_PAGE kosong yang sengaja dibuat generator, dengan header/footer
terhubung ke section sebelumnya. Word memverifikasi 2 halaman/2 section baik
sebelum maupun sesudah; XML utama identik setelah empat margin section 1
disisihkan dan PNG halaman 2 identik per byte. **PASS terbatas:** formatter
tidak menambah halaman kosong baru. Fixture/formatter tidak diubah.
Baseline `private_tests/tesis_uji.docx` dibuka read-only melalui salinan lokal:
Word 16.0 build 16.0.20625 menghasilkan **86 halaman, 2 section portrait,
29 tabel, 15 inline shapes, 43 floating shapes, 201 field body**, tanpa footnote
aktif atau persamaan native. Gutter sekitar 1 cm dan mirror margins tetap
dipertahankan. Ekspor PDF Word lokal, contact sheet 86 halaman dan 19 halaman
individual ditinjau; tidak terlihat clipping jelas pada sampel. Review visual
baseline **PARTIAL**, bukan acceptance hasil formatter. Output Beta tesis
relevan tidak ditemukan di `private_tests`; before/after tesis **PENDING**.
Fixture S2 asli yang tersedia dirender menjadi **3 halaman**, bukan 4; item
halaman 4 S2 tetap **PENDING**. Caption gambar di baseline fixture S2 terpisah
antara halaman 2 dan gambar halaman 3; dicatat untuk review, tidak diperbaiki.
Halaman fisik 4 tesis privat kosong dan merupakan item berbeda dari checklist
halaman 4 fixture S2. Tidak ada FAIL baru formatter yang terbukti. T13 tetap
**PARTIAL**; acceptance tesis nyata/objek kompleks menyeluruh belum selesai.
Bukti privat: `private_tests/t13_baseline_20261125_234928/word_evidence.json`
dan `review_observations.json` beserta salinan/PDF/PNG. SHA-256 semua sumber
dan salinan cocok sebelum/sesudah; tesis asli tidak ditimpa. Hanya laporan
T13 dan progres diperbarui pada Git; tidak ada kode/rules diubah, API, pull,
commit atau push. Pytest tidak diulang; regresi terakhir **274 passed**.

25 November 2026 — jumlah halaman empat fixture T13 berhasil diverifikasi
melalui Microsoft Word COM versi 16.0 build 16.0.20625: font_sebelum **1**,
font_sesudah **1**, margin_sebelum **2**, margin_sesudah **2** halaman.
Metode: salinan sementara dengan SHA-256 identik, read-only terkonfirmasi,
`Repaginate()` lalu `ComputeStatistics(2, false)`; ditutup tanpa menyimpan.
Percobaan langsung awal terhambat pada fixture font yang sedang dipakai;
verifikasi final memakai salinan sementara untuk keempat file. Hash keempat
sumber sebelum/sesudah verifikasi final identik. Angka bukan hasil hitung
page break atau metadata DOCX. Rincian bukti dan cara Print Preview dicatat
di `T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`. Pagination visual rinci, objek
kompleks serta acceptance tesis nyata tetap **PENDING MANUAL REVIEW**;
T13 tetap **PARTIAL**. Hanya dokumentasi diperbarui; kode, fixture dan tesis
tidak disimpan ulang atau diubah. Tidak ada API, commit atau push. Pytest
tidak diulang; regresi terakhir tetap **274 passed**. Entri berikut adalah
riwayat sebelum penghitungan halaman ini.

25 November 2026 — bukti visual operator diterima setelah perbaikan fixture
T13: keempat DOCX pengganti terbuka tanpa error Microsoft Word. Font target
`font_sesudah.docx` menunjukkan Times New Roman 12 pt pada toolbar; Bold,
Italic dan Justify tetap terlihat: **PASS terverifikasi operator** dalam
cakupan tersebut. Page Setup `margin_sesudah.docx`: kiri 4 cm,
kanan/atas/bawah 3 cm, gutter 0 cm, Portrait, Multiple pages Normal:
**PASS terverifikasi operator** untuk pengaturan yang dilaporkan. Operator
menyatakan heading, teks, tabel dan gambar pada screenshot sebelum/sesudah
terlihat tanpa kerusakan jelas; screenshot tidak dilampirkan pada pesan ini
atau diperiksa langsung Codex. Jumlah halaman/pagination, spasi dan indentasi
rinci, pemeriksaan setiap section, objek kompleks serta acceptance tesis nyata
tetap **PENDING MANUAL REVIEW**. Versi Word dan tanggal uji belum diberikan.
T13 tetap **PARTIAL**, bukan PASS keseluruhan. Lihat rincian cakupan dan
checklist pada `T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`. Hanya dua file
dokumentasi diperbarui; kode, aturan dan dokumen asli tidak diubah pada tahap
ini. Perubahan lokal sebelumnya dipertahankan. Tidak ada API, pull, commit
atau push; pytest tidak diulang. Regresi terakhir tetap **274 passed** dari
tahap perbaikan fixture. Entri di bawah adalah riwayat sebelum bukti ini.

25 November 2026 — perbaikan fixture T13 setelah operator melaporkan
`font_sebelum.docx` gagal dibuka Word. Diagnosis membuktikan field `fldSimple`
tanpa `w:instr` pada dua fixture font dan CRC chunk IDAT PNG salah pada dua
fixture margin. ZIP/XML awal lolos; hasil itu tidak membuktikan kompatibilitas
Word. Generator baru `scripts/t13_fixtures.py` memakai penyimpanan python-docx,
field PAGE berinstruksi dan PNG dengan CRC benar. Sampel di
`tests/test_pilot.py` juga diperbaiki. Tidak ada formatter produksi diubah.
Empat fixture lama dicadangkan dan hash-nya diverifikasi pada
`private_tests/t13_word_validation/backup_20261125_233230_899476/`, beserta
`manifest.json`, sebelum keempat file pengganti disimpan pada lokasi semula.
Tes baru struktur paket, integritas, idempotensi dan backup: **15 passed**;
regresi penuh **274 passed** (142,86 detik) melalui
`.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider`.
Validasi ulang paket pengganti dan hash cadangan juga lulus. Detail ada di
`T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`. Word dan render visual belum diuji
ulang; penyebab tunggal pesan Word belum terkonfirmasi. Semua komponen visual
pengganti dan jumlah halaman tetap **PENDING MANUAL REVIEW**; T13 **PARTIAL**.
Tesis asli dan perubahan dokumentasi sebelumnya tetap dijaga. Tidak ada pull,
commit, push, panggilan OpenAI API atau perubahan keamanan Word.

25 November 2026 — kelanjutan PC rumah dari `e525e57` (`main`): checklist
per file dan per komponen untuk empat fixture di
`private_tests/t13_word_validation/` tersedia pada
`T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`, beserta format hasil operator.
Keempat file ditemukan; hasil pemeriksaan visual Word dari operator belum
diterima. Font, margin, paragraf, tabel, gambar dan jumlah halaman tetap
**PENDING MANUAL REVIEW**, tanpa PASS visual baru. T13 tetap **PARTIAL**;
Dummy Master, review halaman 4 S2 dan acceptance dokumen nyata anonim juga
belum ditutup. Working tree dan staging bersih sebelum pembaruan dokumentasi.
Tidak ada kode, aturan, fixture atau tesis diubah; tidak ada pull, commit,
push atau panggilan OpenAI API. Pytest tidak diulang untuk perubahan
dokumentasi ini; **259 passed** tetap hasil historis v0.5.1.

T13 visual Word: **PARTIAL**. Dua pasangan fixture sintetis sudah disiapkan
dan integritas strukturalnya diperiksa. Word COM gagal karena sesi logon
`0x80070520`; Word GUI membuka dokumen AutoRecovered, tetapi fixture belum
dapat dibandingkan secara visual. Halaman dan layout masih PENDING MANUAL
REVIEW. Lihat `T13_WORD_VISUAL_ACCEPTANCE_REPORT.md`. Tidak ada perubahan kode
atau pengujian; regresi otomatis terakhir tetap 259 passed dari v0.5.1.

Beta v0.5.1: branch remote `main` sama dengan commit lokal awal `8e0f2de`;
pekerjaan PC kantor tidak ditemukan sebagai branch remote yang terpisah.
Font `docDefaults` eksplisit kini diperiksa setelah format langsung dan style;
theme ambigu tetap review. Tesis S2: 2 section dengan gutter/mirror tetap
review, 0 section atau run font diubah tanpa cakupan tervalidasi. Detail dan
batasan tersedia di `AI_BETA_V051_EFFECTIVE_MARGIN_FONT_REPORT.md`.
Baseline sebelum perubahan: **254 passed**. Regresi akhir: **259 passed**;
50 tes terfokus formatter/pilot termasuk AppTest juga lulus.

Beta v0.5: koreksi margin deterministik memakai formatter yang ada dan tidak
memanggil AI. Tesis S2 memiliki gutter 1 cm dan mirror margins pada kedua
section; keduanya ditahan untuk review. Tanpa cakupan Beta yang tersimpan,
font tidak dinormalisasi secara otomatis. Render LibreOffice dan Word tahap
ini PENDING. Regresi 254 passed; tes terfokus margin dan Beta juga lulus.
Lihat `AI_BETA_V05_MARGIN_FONT_REPORT.md`.

Perbaikan KeyError Beta: hasil kini memiliki kontrak terversi dan status
validasi eksplisit; laporan operasi diverifikasi sebelum disimpan maupun
ditampilkan. State lama/tidak lengkap dibatalkan tanpa panggilan API ulang;
modul yang tidak memiliki versi kontrak dimuat ulang. Kode saat ini selalu
menghasilkan `operations`; versi modul atau state lama adalah kemungkinan,
tetapi penyebab pada proses pengguna sebelumnya tidak dapat dipastikan tanpa
snapshot proses tersebut. Uji memakai mock, tidak ada panggilan API nyata.
Regresi akhir: **247 passed**; AppTest Dummy Master memproses 23 kandidat,
menerapkan 3 operasi, mempertahankan hasil pada rerun, dan menolak hasil
tanpa laporan. AppTest terfokus setelah penyesuaian tampilan juga lulus.

Final Beta Safety: keputusan konservatif kini dipakai di evaluasi dan Beta;
laporan operasi dibuat setelah audit ulang dan integritas sukses. Uji mock:
Dummy Master 3 applied, tesis privat 91 applied dalam memori; label mock
bukan ground truth. Pengujian AI nyata dan visual Word masih PENDING. Lihat
`FINAL_BETA_SAFETY_REPORT.md`.

Pembaruan validasi 20 sampel: label operator berhasil dicocokkan berdasarkan
ID/BAB/kelompok. Prediksi CSV: 15 cocok dan 5 tidak sesuai; pembandingan
konservatif: 15 keputusan cocok dan 5 tidak pasti. Impor CSV hanya untuk
evaluasi; label tidak menjadi izin formatter. Lihat `VALIDASI_20_SAMPEL_REPORT.md`.

Pembaruan v0.4: sampel evaluasi read-only hingga 20 elemen kini mencakup
kandidat lolos, kandidat tertahan dan bagian khusus; hasilnya tidak dapat
digunakan sebagai izin formatter. Pada 99 kandidat BAB IV, indentasi kiri
tercantum langsung pada paragraf; maksud format belum diketahui. Label tesis,
uji API nyata dan pemeriksaan Word masih PENDING. Lihat
`AI_BETA_V04_EVALUATION_REPORT.md`.

Pembaruan v0.3: panel evaluasi AI tanpa formatter tersedia dengan persetujuan
pengiriman tersendiri, maksimal 15 sampel dan label operator opsional dalam sesi.
Tesis: 110 kandidat tertahan terdiri dari 104 indentasi dan 6 pola sitasi
panjang; ground truth, API nyata dan pemeriksaan Word masih PENDING. Lihat
`AI_BETA_V03_VALIDATION_REPORT.md`.

Pembaruan v0.2: batching penuh dan perkiraan anggaran telah ditambahkan untuk
pengujian mock. Tesis lokal: 88 kandidat setelah penyaringan risiko khusus,
3 batch mock; akurasi AI nyata dan pemeriksaan Word masih PENDING. Lihat
`AI_BETA_V02_REPORT.md`. Estimasi biaya bukan batas tagihan yang dijamin.

Pembaruan AI-assisted beta: alur eksperimental berbasis persetujuan dokumen dan
mock tersedia. Hasil mock bukan validasi keamanan semantik untuk tesis; evaluasi
API nyata dan pemeriksaan visual Word tetap PENDING. Lihat
`AI_AUTOMATIC_BETA_REPORT.md`. Uraian berikut adalah baseline sebelum beta.

Status: **belum selesai — gerbang identitas belum terbukti aman**.

- Pilot terkonfirmasi tetap tersedia; file asli dan aturan tidak diubah.
- Pemeriksaan sintetis menunjukkan kutipan khusus dengan style Body Text dapat
  menerima flag teknis `safe_to_apply=true`; tes di
  `tests/test_automatic_scope_safety.py` menjaga agar pilot tanpa konfirmasi tidak mengubahnya.
- Tesis lokal: 198 kandidat, 0 keputusan diizinkan tanpa konfirmasi, 0 perubahan.
- Regresi: 219 passed; tes keamanan terbaru juga lulus secara terpisah.
- Belum dibuat tombol `Perbaiki Otomatis` atau izin `auto_verified`; mengaktifkan
  keduanya dari heuristik yang ada berisiko mengubah bagian khusus.
- Pemeriksaan visual salinan Dummy Master masih PENDING. Lihat laporan dan
  checklist di `AUTOMATIC_SAFE_FORMATTING_REPORT.md`.

Untuk melanjutkan, tentukan dan uji bukti identitas yang benar-benar dapat
membedakan teks isi dari bagian khusus, ukur false positive pada label operator,
kemudian implementasikan jalur otomatis hanya untuk kasus yang lolos. Pertahankan
validasi T14, audit ulang, dan pemeriksaan integritas serta jangan gunakan mock
atau klasifikasi AI sebagai satu-satunya izin.
