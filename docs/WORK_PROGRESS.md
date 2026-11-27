# Progres Automatic Safe Formatting

27 November 2026 - **Acceptance akhir Preflight v0.6: PASS TERBATAS.**
Aplikasi dijalankan dari .venv pada 127.0.0.1:8507. Edge headless/Playwright
benar-benar mengakses Streamlit, tanpa AppTest/mock: 14,2 cm -> NEEDS_REVIEW
terhadap bidang rencana 14 cm (awal 16,5012 cm), lokasi/ukuran/selisih/alasan
terlihat melalui tabel. Review belum disetujui menahan kiri/kanan; atas/bawah
tetap diterapkan. CSV/DOCX benar-benar diunduh dari tombol aplikasi.

Review dapat dibatalkan, keluaran lama hilang; A -> B dengan geometri sama,
jenjang S2/S1/S2, dan perubahan rencana heading-only membatalkan review lama.
Fixture 13,9 cm -> PASS lebar sederhana; margin sudah sesuai, 0 perubahan dan
tidak ada DOCX perubahan. Tindakan checkbox adalah simulasi uji sintetis agen,
bukan persetujuan operator untuk dokumen pelanggan.

Unduhan S2_browser_held_horizontal.docx dibuka Word COM read-only: 3 -> 3
halaman, 32 paragraf, 1 tabel 18x5, 1 gambar 14,2 cm, 1 section portrait;
kiri/kanan tetap 2,5/2 cm dan atas/bawah 3/3 cm. Semua part selain XML utama
identik, XML utama hanya berbeda dua atribut margin top/bottom. Seluruh tiga
halaman render Word ditinjau: tidak teramati clipping/overlap baru, tabel/
gambar/header/footer dan nomor 1/2/3 terjaga. Caption 2/gambar 3 tetap seperti
input, bukan pemisahan baru. Ini Word COM + review render, bukan klaim GUI
Word manual/operator. Hash sumber, tesis, rules dan kode yang diuji tetap sama.

Penyesuaian driver browser (label checkbox, navigasi combobox, menunggu
rerender) tidak mengubah aplikasi. Toolbar dataframe CSV tidak menghasilkan
event download headless; tidak diluluskan, sedangkan tombol laporan margin
CSV/DOCX aplikasi berhasil. Detail kendala dan bukti gabungan tersimpan agar
tidak mengklaim skrip eksplorasi yang gagal sebagai PASS.

Bukti hanya privat di private_tests/preflight_v06/acceptance_20261127,
terutama acceptance_summary.json, word_acceptance.json dan browser_output_integrity.json.
Laporan v0.6 dan TASKS diperbarui. **299 pytest passed terakhir tetap berlaku**,
tidak diulang karena tidak ada perubahan kode/tes produksi. T13 tetap PASS
TERBATAS, acceptance varian 71 dan pengecualian 11 tidak berubah. Tidak ada
resize otomatis, API berbayar, pengubahan JSON/tesis, render86, pull/commit/push.
Prioritas berikutnya: review diff/staged data dan sinkronisasi GitHub aman
hanya setelah instruksi; semua private_tests tetap dikecualikan. Ini bukan
rilis umum atau klaim pemenuhan semua 317 aturan.

27 November 2026 - melanjutkan v0.6 Preflight yang terhenti karena usage limit.
Workspace/branch main dan seluruh diff sebelumnya dipertahankan; tidak memulai
implementasi ulang. Preflight sudah terhubung ke rencana formatter serta
Streamlit margin dan umum; review per section dapat dibatalkan dan tidak
mengubah gambar. S2 14,2 cm -> NEEDS_REVIEW (selisih sekitar +0,200014 cm),
13,9 cm -> PASS pemeriksaan lebar sederhana pada bidang sekitar 13,999986 cm.
Bukti deteksi/hash lama masih cocok; DOCX tidak disimpan atau dirender ulang.

Regresi sebelumnya 5 failed / 293 passed: tiga AppTest Beta mengalami
NameError karena kondisi membaca margin_preflight_key sebelum dibuat;
dua tes sitasi/heading mengambil dataframe berdasarkan indeks yang bergeser
oleh panel baru. Perbaikan minimal sudah tersimpan: syarat preflight hanya
pada alur margin, dan pemilihan findings berdasarkan kolom dengan assertion
lama tetap. Kelima tes sempat lulus sebelum sesi putus. Verifikasi lanjutan
kelimanya bersama 24 kasus preflight kini **29 passed in 45.79s**. Kelima
kegagalan tersebut selesai tanpa perubahan tambahan. Namun review berikutnya
menemukan bug cakupan konfirmasi untuk dua dokumen dengan geometri sama:
tes baru mereproduksi kebocoran konfirmasi (1 failed), lalu empat baris app.py
diperbaiki agar widget terikat SHA-256 sumber/jenjang/rencana/alur. Test tetap
dipertahankan. Setelah perbaikan, **30 tes terkait lulus in 45.25s**.

Regresi awal keadaan diwarisi **298 passed in 174.90s**. Karena bug cakupan
konfirmasi kemudian terbukti dan kode berubah, satu regresi final sesudah
perbaikan hash selesai **299 passed in 179.79s**, 0 failed/error/skip;
pengulangan mempunyai alasan teknis konkret. v0.6 **SELESAI TEKNIS**, tidak
ada kegagalan tersisa. Baseline 274 bertambah 25 kasus preflight. Siap menjadi
kandidat commit kode/tes/dokumentasi, belum merupakan rilis produksi umum;
sinkronisasi GitHub tidak dilakukan dan perlu instruksi terpisah.
Log/JUnit baru disimpan di private_tests/preflight_v06 dengan nama
targeted_resume_20261127, regression_final_20261127, targeted_hashfix_20261127
dan regression_hashfix_final_20261127; reproduksi bug pada review_hash_reproduction_20261127.log. Cache lastfailed kosong
tidak dipakai untuk menebak daftar gagal; detail klasifikasi ada di laporan
PREFLIGHT_V06_REPORT.md. Baseline 274 passed tetap catatan sebelum v0.6.

Gutter/mirror tetap dilindungi; floating/anchor, tabel, posisi ambigu dan
konteks kompleks tetap NEEDS_REVIEW. Perubahan horizontal pada section
berisiko ditahan sampai review eksplisit, operasi aman lain tetap tersedia.
Tidak ada resize otomatis, perluasan 317 aturan atau klaim layout Word penuh.
T13 tetap ditutup PASS TERBATAS dan acceptance 71/pengecualian 11 tetap sah.
Tahap berikutnya: acceptance Word terfokus alur preflight S2; bukan mengulang
render 86 halaman. Tidak ada API, pull, commit atau push pada sesi ini.

26 November 2026 - **T13 DITUTUP: PASS TERBATAS** pada korpus dan operasi
acceptance yang disepakati. Operator telah memeriksa hasil manual S2 di Word
dan menerima `S2_manual_image_13_9cm_experiment.docx` sebagai **ACCEPTED FOR
TESTING**, terbatas pada salinan uji tersebut. SHA-256 kembali cocok dengan
manifest dan bukti Word:
`4e13c23cf6b9e3d682cd8d70801e0f436c47ee87664cef4e4a68087b5bc0c299`.
Keputusan akhir terikat hash disimpan pada
`private_tests/t13_s2_image_resize_20261126/operator_final_limited_acceptance_20261126.json`.
Tidak ada klaim screenshot/Word baru pada tahap pencatatan ini.

Penerimaan varian tesis 71 tetap berlaku; hash cocok dengan keputusan akhir
sebelumnya. Seluruh operasi pada 11 paragraf ambigu termasuk 401 tetap
dikecualikan. Beta 82 tidak menjadi output final yang diterima. Tesis tetap
86 halaman menurut bukti Word yang tersedia, Master 9 -> 9, S2 3 -> 3.
Koreksi gambar S2 13,9 cm masuk bidang tulisan dan diterima sebagai langkah
manual, bukan kemampuan resize otomatis. Output margin-only lama tetap
PARTIAL/NEEDS_REVIEW untuk overflow, tidak ditimpa atau diluluskan retroaktif.

Matriks final pada laporan T13 merekonsiliasi bukti fixture font/margin,
integritas dan visual tesis, preservasi objek Master serta hasil manual S2.
T5 historis tetap SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE melalui opsi A;
output historis/jenis penomorannya tidak diklaim ditemukan. Tidak ada blocker
wajib tersisa untuk scope terbatas ini. Riwayat PENDING/PARTIAL sebelumnya
tetap disimpan, dengan status terkini pada bagian penutupan laporan.

Batas wajib: normalisasi hanya pada paragraf/konteks tervalidasi; struktur
ambigu dipertahankan; objek kompleks dilindungi, bukan diperbaiki otomatis.
Manipulasi objek kompleks, pembaruan field/TOC, endnote dan resize gambar
otomatis belum tervalidasi. Aturan tanpa handler/manual.not-implemented
belum didukung. Ini bukan kelulusan 317 aturan atau izin otomatis bagi
seluruh skripsi/tesis/disertasi maupun rilis produksi umum.

Prioritas berikutnya dicatat di TASKS: implementasi PREFLIGHT risiko overflow
gambar terhadap bidang setelah rencana perubahan margin, termasuk posisi dan
konteks ambigu; hasil NEEDS_REVIEW dengan lokasi/ukuran/alasan. Tidak silent
resize/crop/move; media, caption, input dan isi harus tetap. Desain dan kasus
uji tersedia pada laporan; implementasi belum dikerjakan pada tugas ini.

Dokumentasi T13/WORK_PROGRESS/TASKS dan keputusan privat diperbarui. Hash
DOCX sumber/hasil, kode dan aturan dilindungi. Tidak ada API, pull, commit,
push, pytest ulang atau render ulang. Regresi terakhir **274 passed** tetap
hasil historis, bukan pengujian baru.

26 November 2026 - finalisasi matriks T13 dan persiapan keputusan akhir S2.
**T13 tetap PARTIAL**, hanya penerimaan final operator atas file manual S2
ber-hash yang masih terbuka untuk penutupan dengan batas cakupan eksplisit.
Belum ada persetujuan S2 dicatat. Setelah keputusan itu diberikan, bukti
mendukung **PASS TERBATAS untuk korpus/operasi terdaftar**, bukan semua aturan
atau produksi umum. Tidak meminta ulang ACCEPTED FOR TESTING varian 71.

Hash varian 71, Master, sumber S2, output margin-only dan resize dicocokkan
kembali; 172 PNG pasangan Beta 82, tujuh sampel varian 71, ringkasan Word/
integritas serta render Master/S2 masih tersedia. Tidak membuat klaim render
penuh varian 71: 82 halaman pixel-identik milik pasangan Beta 82; varian 71
mempunyai 7 sampel visual dan acceptance operator. Sisa nilai awal geometri
PENDING di manifest resize dijelaskan oleh bukti Word akhir terikat hash
serta bounding box PDF; tidak mengulang tes atau menimpa manifest riwayat.

Kandidat keputusan: `private_tests/t13_s2_image_resize_20261126/` file
`S2_manual_image_13_9cm_experiment.docx`, SHA-256 sintetis
`4e13c23cf6b9e3d682cd8d70801e0f436c47ee87664cef4e4a68087b5bc0c299`.
Teknis manual S2 **PASS TERBATAS**: gambar 13,9 x 7,228 cm, rasio tetap,
x114,82-508,76 pt masuk bidang x113,40-510,25 pt; Word 3 -> 3 halaman,
caption/gambar halaman 3, tabel halaman 2, footer 1/2/3 dan non-target utuh.
Seluruh halaman telah ditinjau, tidak ada clipping/distorsi/overlap baru
teramati. Penerimaan eksperimen tidak disamakan dengan penerimaan operator.
Output margin-only tetap PARTIAL/NEEDS_REVIEW karena overflow; tidak diubah.

Opsi A tetap sah; T5 historis **SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE**.
Artefak output historis tidak diklaim ditemukan dan bukan blocker lagi.
Preservasi Master/tesis/S2 yang diuji dipisahkan dari konstruksi yang tidak ada
atau belum didukung. Endnote, update field/TOC dan manipulasi objek kompleks
tetap di luar klaim; koreksi gambar masih manual; struktur ambigu dan gutter/
mirror dilindungi. Tidak ada klaim 317 aturan terpenuhi.

Tahap berikutnya disiapkan sebagai desain PREFLIGHT read-only: evaluasi batas
gambar terhadap bidang setelah margin yang direncanakan; lokasi/ukuran dan
ketidakpastian posisi dicatat; overflow/ambigu menghasilkan NEEDS_REVIEW.
Tidak silent resize/crop, tidak mengubah media/caption. Kasus uji implementasi
kelak mencakup lebar berlebih, posisi offset dan konteks ambigu. Preflight
belum ada pada produksi dan bukan blocker tambahan acceptance manual T13.
Rincian matriks/status dan rancangan pada bagian finalisasi laporan T13.

Hanya laporan T13 dan progres diperbarui pada tugas ini. TASKS dan perubahan
lokal sebelumnya dipertahankan. Tidak mengubah tesis/kode/aturan atau DOCX;
tidak ada API, commit/push, render ulang atau pytest. Regresi terakhir
**274 passed** tetap bukti historis.

26 November 2026 — eksperimen koreksi gambar S2 benar-benar dilaksanakan.
Posisi aktual Word/PDF membuktikan overflow: gambar x113,40–515,90 pt,
batas teks x113,40–510,25 pt (kanan lebih 5,65 pt atau sekitar 0,199 cm).
Hanya dimensi gambar pada salinan baru diubah dari 14,2 ke **13,9 cm**, tinggi
**7,228 cm**, rasio tetap. Hasil pada
`private_tests/t13_s2_image_resize_20261126/S2_manual_image_13_9cm_experiment.docx`;
source/margin-only lama tidak ditimpa. Seluruh media, teks, caption, tabel,
hyperlink, section/margin, header/footer dan XML selain empat atribut dimensi
identik. Word read-only mengukur **3 → 3 halaman**; batas gambar aktual sesudah
**114,82–508,76 pt**, seluruhnya di dalam bidang teks. Semua tiga halaman
hasil diperiksa: 1/2 identik pixel dengan margin-only; 3 memperlihatkan gambar
lebih kecil dan reflow teks yang diharapkan tanpa clipping/distorsi/overlap
baru. Caption+gambar tetap halaman 3, tabel halaman 2, footer 1/2/3.
**Koreksi manual S2 pada salinan: PASS TERBATAS**, bukan fitur resize otomatis.
Bukti lengkap pada folder eksperimen, terutama `manual_resize_manifest.json`,
`word_position_before/after.json` dan `word_pdf_image_bounds.json`.
T13 tetap **PARTIAL** sampai penerimaan akhir hasil manual dan batas penutupan
tercatat; varian 71 tidak dibuka ulang. Output margin-only asli tetap mempunyai
overflow dan tidak diluluskan retroaktif. PREFLIGHT read-only direkomendasikan
sebagai task terpisah: analisis batas bidang sesudah margin yang direncanakan,
lokasi/ukuran/anchor gambar dan posisi Word bila tersedia; beri NEEDS_REVIEW
untuk overflow/ambigu, jangan otomatis resize. Belum diimplementasikan.
Tidak ada perubahan formatter/rules/tesis, API, commit/push, pytest ulang atau
render besar. Regresi terakhir **274 passed**. Catatan TASKS S2 sebelumnya
merujuk hasil margin-only; lihat laporan terbaru untuk eksperimen manual ini.

26 November 2026 — opsi A disetujui; item T5 historis kini **SUPERSEDED BY
REPRODUCIBLE S2 ACCEPTANCE**, catatan artefak/penomoran lama tidak ditemukan
tetap tersimpan. S2 input identik dengan sumber commit 4ef1bbd; empat margin
LAY-008/009/010/011 diterapkan pada salinan melalui handler margin-only lama,
audit ulang dan idempotensi lulus. Seluruh teks/XML paragraf, tabel 18x5,
media, hyperlink, header/footer dan properti section non-target terjaga.
Pasangan privat di `private_tests/t13_s2_replacement/`, dengan hash input/output
pada `acceptance_manifest.json` dan laporan T13. Word read-only mengukur
**3 → 3 halaman**; footer teramati 1/2/3 dicatat terpisah dari indeks fisik.
Semua halaman sebelum/sesudah ditinjau. Tabel tetap halaman 2; caption gambar
2 → 3 dan gambar 3 → 3, celah 1 → 0: pemisahan berasal dari input dan tidak
diperburuk. Tidak terlihat crop/overlap baru, tetapi temuan geometri terukur:
gambar tetap **14,2 cm**, bidang teks baru sekitar **14,0 cm**, selisih lebar
sekitar **0,2 cm**. Penyebabnya penyempitan bidang oleh margin sementara ukuran
gambar dilindungi. Tidak diam-diam mengubah gambar/formatter. Subpemeriksaan
preservasi/empat margin lulus, tes pengganti **PARTIAL** sampai disposisi
lebar gambar (pengecualian eksplisit atau koreksi salinan yang diizinkan).
T13 **PARTIAL**; varian 71 ACCEPTED FOR TESTING tetap berlaku. Blocker bukan
lagi pencarian artefak historis, melainkan temuan layout S2 dan batas akhirnya.
Manipulasi objek, update field/TOC/endnote belum teruji dan aturan tanpa handler
tetap di luar klaim. TASKS diberi catatan penggantian; tidak ada perubahan tesis,
formatter atau JSON, API, pull, commit, push, render tesis86 atau pytest ulang.
Regresi terakhir **274 passed**; bukti Word/PDF/PNG baru hanya fixture kecil S2.

26 November 2026 — disposisi halaman 4 S2: **UNRESOLVED LEGACY REFERENCE**.
Source fixture historis pada commit 4ef1bbd dan input saat ini terbukti
identik byte-per-byte; hash sintetis dicatat di laporan. Output/screenshot,
versi hasil dan jenis nomor halaman yang dimaksud tetap tidak diketahui.
Baseline Word S2 yang tersedia 3 halaman, tabel halaman 2, caption 2/gambar 3;
bukan bukti asal nomor 4. Tidak ada artefak atau hasil pengujian yang dibuat-buat.
Usulan **S2-PRESERVATION-01**: input tetap ber-hash, output margin-only baru
bernama eksplisit di private_tests (belum dibuat/hash masih PENDING), empat
margin LAY-008/009/010/011, pertahankan 32 paragraf/1 tabel 18x5/1 gambar/
1 hyperlink/1 section; ukur indeks fisik Word dan nomor footer terpisah,
catat perubahan pagination serta posisi tabel/caption/gambar. Usulan caption
preservasi mempertahankan urutan dan tidak menambah celah baseline 1 halaman,
bukan klaim memperbaiki kepatuhan caption. Tidak meminjam halaman Master.
Pilihan operator: **A** setujui penggantian kriteria dan kemudian jalankan
pemeriksaan S2 yang dapat direproduksi; **B** tetap jadikan referensi historis
blocker sampai artefak ditemukan. A/B belum dipilih. Usulan JSON privat pada
`private_tests/t13_complex_acceptance_20261126/s2_legacy_disposition_proposal.json`.
Matriks akhir memisahkan preservasi PASS TERBATAS, endnote tidak ada/N/A,
update field/manipulasi objek di luar scope, legacy unresolved, dan kriteria
pengganti PROPOSED. Persetujuan varian 71 tetap berlaku. T13 **PARTIAL**;
A saja tidak cukup, pengganti harus lulus dengan hash/hasil Word yang nyata
sebelum PASS TERBATAS untuk scope yang disepakati. Tidak ada tes/render/
formatter baru, perubahan tesis/kode/aturan, API, pull, commit atau push.
Regresi terakhir **274 passed**, tidak diulang. Dua laporan diperbarui.

26 November 2026 — rekonsiliasi objek kompleks T13: bukti PC rumah tersedia.
Varian 71 tetap ACCEPTED FOR TESTING; tidak diminta approval ulang. Inventaris
Master mengonfirmasi 1 footnote aktif, 1 OMML, field, header/footer dan section
5 landscape; seluruh endnote aktif 0. Pasangan Master/pilot tersimpan memiliki
teks/tabel/subtree math-field/section sama dan semua part selain XML utama
identik. Celah visual ditutup terfokus di Word read-only: **9 → 9 halaman**,
hanya fisik **3,4,8** sebelum/sesudah diekspor. Halaman 3/8 identik pixel;
4 menunjukkan reflow dari paragraf target 44, footnote dan persamaan tetap
utuh tanpa clipping baru yang terlihat. Bukti privat tersimpan di
`private_tests/t13_complex_acceptance_20261126/` (`word_evidence.json`,
`integrity_visual_summary.json` dan enam PDF/PNG terpilih).
Matriks laporan: tabel/gambar/header/footer, footnote/OMML/landscape Master
dan preservasi field/caption **PASS TERBATAS**. Endnote **NOT APPLICABLE**
pada korpus, dukungan umum belum teruji; update field/TOC **PENDING**, di luar
klaim acceptance. Tidak ada FAIL baru akibat formatter yang ditemukan.
Asal T5 "halaman 4 S2" ditemukan di commit lokal **4ef1bbd** saat T5_REPORT
ditambahkan. Nama sumber fixture S2 jelas, tetapi versi hasil/hash/screenshot
serta fisik/tercetak tidak disebut. Angka empat halaman di paragraf S3 bukan
bukti untuk S2. S2 baseline sebelumnya 3 halaman, tidak diuji ulang; item
historis tetap **UNRESOLVED/PENDING**, bukan halaman fisik 4 tesis privat.
T13 **PARTIAL** sampai item S2 diselesaikan dan batas penutupan eksplisit:
preservasi contoh yang diuji diterima, manipulasi objek kompleks/endnote/
update field tetap dikecualikan atau butuh bukti terfokus jika hendak diklaim.
Langkah berikut paling bermanfaat: disposisi artefak/checklist halaman 4 S2.
Tidak ada formatter, tesis, JSON aturan, API, pull, commit atau push; hanya
matriks dokumentasi dan bukti privat diperbarui. Tidak ada render 86 halaman
atau pytest ulang; regresi terakhir **274 passed**.

26 November 2026 — persetujuan akhir terbatas operator: varian 71 telah
diperiksa langsung di Microsoft Word dan diterima sebagai **ACCEPTED FOR
TESTING** hanya untuk salinan tesis uji ini. Identitas/hash file cocok dengan
manifest eksperimen, bukti Word dan acceptance teknis; sumber tetap utuh.
Penerimaan akhir file yang sebelumnya PENDING kini selesai dalam batas
pengujian ini; tidak perlu diminta ulang tanpa perubahan/temuan baru.
Seluruh operasi 11 ambigu termasuk 401 tetap dikecualikan dan format sumber
dipertahankan. Beta 82 bukan hasil final; tidak ada izin generik untuk
dokumen lain atau otomatisasi produksi. Nama file eksperimen historis tidak
diubah; status terbaru terikat hash pada manifest privat
`experiment_71_only/operator_final_limited_acceptance_20261126.json` dalam
folder `private_tests/t13_real_acceptance_20261125_235720/`.
Acceptance teknis **PASS TERBATAS**, T13 keseluruhan **PARTIAL**. Sisa:
acceptance objek kompleks/field atau batas cakupan yang eksplisit; klarifikasi
artefak historis T5 halaman 4 S2; rekonsiliasi matriks penutupan. Tidak ada
klaim PPKI memenuhi 317 aturan. Prioritas berikut T13: pemeriksaan terfokus
matriks objek kompleks dan S2 memakai artefak yang sudah tersedia, tanpa
mengulang gerbang acceptance tesis yang sudah diterima.
Hanya dokumentasi dan manifest keputusan privat diperbarui. Tesis, varian,
formatter dan JSON aturan tidak berubah. Tidak ada API, pull, commit atau
push; tidak ada Word/render/pytest ulang. Regresi terakhir **274 passed**.

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
