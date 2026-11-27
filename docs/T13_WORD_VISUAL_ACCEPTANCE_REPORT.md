# T13 — Validasi Visual Microsoft Word

**Status terkini: PASS TERBATAS - T13 ditutup untuk cakupan acceptance yang
disepakati, 26 November 2026.** Operator telah memeriksa hasil manual S2 di
Microsoft Word dan menerima file ber-hash di bawah sebagai **ACCEPTED FOR
TESTING**. Penerimaan varian tesis 71 tetap berlaku. Semua gerbang acceptance
terbatas pada matriks ini terpenuhi; tidak ada blocker wajib yang masih terbuka
dalam cakupan tersebut. Ini bukan kelulusan seluruh checklist, semua jenis
DOCX, seluruh 317 aturan atau kesiapan produksi umum.

## Keputusan akhir operator dan penutupan terbatas - 26 November 2026

Persetujuan operator berasal dari pernyataan eksplisit pada percakapan setelah
pemeriksaan langsung di Word, bukan disimpulkan dari izin eksperimen. Hash
file S2 cocok dengan `manual_resize_manifest.json` dan
`word_position_after.json`; hash varian 71 tetap cocok dengan keputusan
sebelumnya. Tidak ada Word/render baru atau penyimpanan DOCX pada tahap ini.

Catatan keputusan terikat hash disimpan privat pada
`private_tests/t13_s2_image_resize_20261126/operator_final_limited_acceptance_20261126.json`.
Persetujuan ini hanya untuk salinan pengujian S2 tersebut, bukan izin otomatis
mengubah ukuran gambar dokumen lain. Seluruh operasi pada 11 paragraf ambigu,
termasuk 401, tetap dikecualikan; Beta 82 tetap bukan output final yang diterima.

Referensi historis T5 tetap **SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE** sesuai
opsi A yang sudah disetujui. Artefak output historis tidak diklaim ditemukan.
Output S2 margin-only yang masih overflow disimpan sebagai bukti diagnosis,
bukan diberi PASS retroaktif. Yang diterima adalah hasil dengan koreksi manual.

Manipulasi objek kompleks, pembaruan field/TOC, endnote dan resize gambar
otomatis **belum tervalidasi dan di luar acceptance**. Bukti preservasi objek
yang diuji tetap PASS TERBATAS. PREFLIGHT menjadi prioritas pengembangan
berikutnya, belum diimplementasikan dan bukan blocker penutupan ini.

## Matriks acceptance final - 26 November 2026

Bagian ini adalah acuan status terbaru. Catatan bertanggal sama pada bagian
historis di bawah, checklist awal dan manifest lama dipertahankan sebagai
riwayat. Status PENDING penerimaan S2/T13 PARTIAL lama telah diselesaikan oleh
keputusan akhir ini; cakupan yang belum diuji tetap tidak diberi PASS.

### Kelengkapan bukti yang diverifikasi kembali

Pemeriksaan kali ini hanya pembacaan artefak dan pencocokan SHA-256. Hash
varian 71 cocok dengan keputusan operator akhir; hash pasangan Master,
input S2 sintetis, output margin-only dan output resize cocok dengan manifest
masing-masing. Sebanyak 172 PNG pasangan Beta 82 serta tujuh PNG sampel varian
71 masih tersedia; ringkasan perbandingan, bukti Word, manifest integritas dan
render terfokus Master/S2 tersedia. Tidak ada pengujian Word, render atau
perbandingan pixel baru yang diklaim pada finalisasi ini.

Angka **82/86 halaman identik** dan perbedaan 29/31/33/34 adalah bukti pasangan
Beta 82, bukan hasil render penuh varian 71. Varian 71 memiliki bukti Word
86 halaman, integritas seluruh dokumen, tujuh sampel visual 17/29/31/33/34/74/76
dan penerimaan operator yang sudah tercatat. Sebanyak 79 halaman varian itu
tidak diklaim telah dirender ulang. Tidak perlu meminta penerimaan varian 71
kembali atau mengganti file final yang diterima dengan Beta 82.

Ada sisa nilai awal `geometry_after_word: PENDING` di manifest eksperimen S2.
Itu bukan kekurangan pengujian posisi terkini: `word_position_after.json`
terikat SHA-256 output yang sama, dan `word_pdf_image_bounds.json` serta
`image_within_text_bounds_after: true` merekam hasil selesai. Manifest riwayat
tidak ditulis ulang; bukti selesai tersebut menjadi rujukan geometri akhir.
Demikian pula daftar blocker lama pada keputusan varian 71 merujuk keadaan
sebelum pengujian Master dan penggantian S2, bukan keputusan baru operator.

### Matriks acceptance akhir pada cakupan eksplisit

| Komponen/kriteria | Bukti dan batas aktual | Status terkini / dampak penutupan |
|---|---|---|
| Fixture font dan margin | Dibuka Word, target font TNR 12/Bold/Italic/Justify dan Page Setup diverifikasi operator; Word font 1 -> 1, margin 2 -> 2. Halaman kedua margin berasal dari desain section, bukan halaman kosong baru | PASS TERBATAS untuk pemeriksaan yang tercatat; rincian checklist yang tidak diperiksa terpisah tidak diluluskan |
| Tesis varian 71 | 71 spasi LAY-017 dan 3 indentasi LAY-018; teks, 29 tabel, 15 gambar inline, 896 paragraf/2 section terjaga; Word 86 -> 86; tujuh sampel visual; penerimaan operator terikat hash | Teknis PASS TERBATAS; ACCEPTED FOR TESTING sudah diberikan untuk salinan ini |
| Pengecualian 11 paragraf, termasuk 401 | Semua properti format sumber dan XML dipertahankan; tidak ada operasi spasi/indentasi pada yang ditahan | Terpenuhi; Beta 82 bukan hasil final yang diterima |
| Tabel, gambar, caption, hyperlink | Struktur/isi/media terjaga pada pasangan yang diuji; sampel tesis/Master dan seluruh halaman S2 ditinjau; merged cells/landscape table Master masuk bukti preservasi | PASS TERBATAS untuk preservasi dan layout yang diperiksa, bukan perbaikan otomatis objek/caption |
| Header/footer, nomor halaman, section | Bagian paket dan konfigurasi non-target terjaga; contoh Master dan S2 tampak; S2 fisik 1/2/3 dicatat terpisah dari nomor footer | PASS TERBATAS; konfigurasi gutter/mirror tesis dilindungi |
| Footnote, persamaan, landscape Master | Satu footnote aktif dan satu persamaan native; section 5 landscape. Word 9 -> 9; halaman 3/4/8 ditinjau, 3/8 identik pixel, reflow halaman 4 sesuai perubahan paragraf | PASS TERBATAS preservasi contoh yang diuji; bukan manipulasi objek tersebut |
| Field/PAGE/TOC | Struktur, cached content dan tampilan teramati dipertahankan; tidak ada pengujian update field atau pembuatan TOC | PASS TERBATAS preservasi saja; update/validitas seluruh hasil field di luar cakupan |
| Endnote, chart Word native/OLE atau konstruksi yang tidak ada pada korpus | Tidak ada contoh aktif yang dapat dipakai menguji kemampuan tersebut | NOT APPLICABLE pada input yang tidak memuatnya; belum tervalidasi secara umum, tidak diberi PASS |
| T5 historis "halaman 4 S2" | Opsi A sudah disetujui; sumber cocok commit 4ef1bbd, output historis/jenis nomor tetap tidak teridentifikasi | SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE; bukan blocker pencarian artefak lagi |
| S2-PRESERVATION-01, output margin-only | Empat margin 4/3/3/3 cm dan integritas lulus; Word 3 -> 3; seluruh halaman diperiksa. Caption/gambar dari terpisah di input menjadi bersama di halaman 3. Gambar lama overflow aktual 5,65 pt | Output ini tetap PARTIAL/NEEDS_REVIEW dan disimpan sebagai diagnosis; tidak diluluskan retroaktif |
| Hasil S2 setelah intervensi manual | Salinan ber-hash di bawah: gambar 13,9 cm, rasio tetap, posisi masuk bidang teks; 3 -> 3 halaman; seluruh halaman ditinjau, objek/non-target terjaga | Teknis PASS TERBATAS; operator ACCEPTED FOR TESTING untuk file ini, bukan izin resize otomatis |
| Regresi dan pengamanan | Hasil terakhir 274 passed; tidak ada perubahan kode/aturan atau pelepasan pengamanan T14 | Bukti regresi terakhir digunakan; bukan hasil tes ulang hari ini |
| Penutupan T13 | Gabungan bukti di atas dan persetujuan akhir S2; terbatas pada korpus/operasi/versi hasil yang tercatat | PASS TERBATAS; ditutup pada cakupan eksplisit ini, bukan seluruh aturan atau produksi umum |

### Identitas file S2 yang diterima operator

File yang diterima adalah **hasil koreksi manual**, bukan output margin-only:

`private_tests/t13_s2_image_resize_20261126/S2_manual_image_13_9cm_experiment.docx`

SHA-256 sintetis yang diverifikasi kembali:
`4e13c23cf6b9e3d682cd8d70801e0f436c47ee87664cef4e4a68087b5bc0c299`.

- Word 16.0 build 16.0.20625: **3 -> 3 halaman fisik**, 1 section portrait;
  footer menampilkan Halaman 1, 2, 3. Empat margin tetap kiri 4 cm,
  kanan/atas/bawah 3 cm.
- Gambar **14,2 -> 13,9 cm**, tinggi 7,228 cm, rasio tetap. Posisi aktual dari
  PDF Word akhir x=114,82-508,76 pt berada dalam bidang x=113,40-510,25 pt.
- Caption dan gambar tetap halaman 3; tabel 18x5 tetap halaman 2. Media, teks,
  caption, tabel, hyperlink, margin/section dan header/footer tidak diubah.
  Hanya empat atribut dimensi gambar berubah dari output margin-only.
- Semua tiga halaman hasil telah ditinjau pada pengujian sebelumnya; 1/2
  identik pixel dengan margin-only, halaman 3 berubah sesuai ukuran gambar
  dan reflow teks di bawahnya. Tidak teramati clipping, distorsi atau overlap
  baru. Sumber dan output sebelumnya dipertahankan.

**Keputusan operator: ACCEPTED FOR TESTING.** Operator menyatakan telah
memeriksa file S2 manual ini di Microsoft Word dan menyetujui salinan pengujian
tersebut. Penerimaan dan hash dicatat dalam keputusan privat di atas. Izin
resize otomatis untuk dokumen lain tidak diberikan.

Gerbang penerimaan akhir telah terpenuhi. Tidak ada kegagalan teknis atau
persyaratan wajib yang belum didisposisi dalam cakupan acceptance terbatas
yang disepakati, sehingga **T13 ditutup sebagai PASS TERBATAS**. Rincian yang
belum diuji tetap dinyatakan belum diuji; penutupan terbatas tidak mengubahnya
menjadi PASS. Pengujian luas endnote, update field atau variasi objek lain
hanya diperlukan bila kelak cakupan dukungan diperluas.

### Batas kemampuan yang harus menyertai penutupan

1. Normalisasi hanya pada paragraf, aturan dan konteks yang tervalidasi;
   keputusan 71 berlaku pada salinan tesis ini. Struktur ambigu dipertahankan,
   termasuk semua operasi pada 11 paragraf dan 401.
2. Objek kompleks dilindungi. Bukti preservasi bukan izin otomatis mengubah
   isi tabel/gambar, caption, footnote, persamaan atau layout kompleks.
3. Pembaruan field/TOC, endnote aktif dan konstruksi tidak tercakup belum
   tervalidasi; aturan tanpa handler/manual.not-implemented tetap belum didukung.
4. Resize gambar S2 masih koreksi manual pada salinan. Formatter margin-only
   dapat membuat bidang lebih sempit tanpa mengubah gambar yang dilindungi;
   karena itu tidak ada klaim output otomatis bebas overflow atau siap untuk
   semua dokumen pelanggan. Gutter/mirror tidak dipaksakan berubah.
5. PASS TERBATAS adalah acceptance korpus dan operasi terdaftar; bukan
   kepatuhan semua 317 aturan atau generalisasi ke seluruh S1/S2/S3.

### Rancangan tahap berikutnya: PREFLIGHT gambar setelah rencana margin

Status **DESAIN SAJA**, belum diimplementasikan. Ini prioritas berikutnya
setelah penutupan terbatas T13, bukan kemampuan yang sudah diluluskan:

| Tahap | Perilaku yang direncanakan |
|---|---|
| Input audit | Baca DOCX dan rencana perubahan margin tanpa menyimpan input. Petakan gambar ke section, paragraf/sel/kolom serta inline/floating; gunakan margin hasil rencana dan orientasi/ukuran kertas, indentasi/alignment, gutter/mirror bila dapat ditentukan |
| Analisis batas | Bandingkan dimensi dan posisi yang dapat diturunkan secara aman dengan bidang tersedia. Lebar saja hanya indikator risiko; gambar kecil dengan offset dapat keluar bidang. Jika anchor/wrapping/kolom/gutter tidak dapat dipastikan, jangan simpulkan muat |
| Hasil | NEEDS_REVIEW untuk indikasi overflow atau posisi/bidang ambigu; sertakan lokasi gambar/section, ukuran, bidang sebelum/sesudah rencana, dasar perhitungan/ketidakpastian dan alasan. Bedakan estimasi struktur dari verifikasi posisi aktual Word |
| Keputusan operator | Tampilkan peringatan pada rencana sebelum apply; tindakan terkait yang berisiko memerlukan review, bukan silent resize/crop/move. Pertahankan media, caption, teks dan input. Penanganan manual selalu pada salinan |
| Verifikasi opsional | Jika Word lokal tersedia, ukur bounding box layout terhadap batas teks dan catat toleransi/unit. Tanpa Word/posisi pasti tetap NEEDS_REVIEW, bukan klaim kompatibilitas visual |
| Pengujian saat implementasi kelak | Sintetis 14,2 cm versus bidang 14,0 cm memicu warning; 13,9 cm pada posisi yang terbukti muat tidak false alarm overflow; gambar lebih kecil tetapi bergeser keluar bidang tetap warning; konteks ambigu memicu review; hash input/media dan isi tidak berubah |

Tidak ada resize otomatis atau perluasan aturan JSON dalam rancangan ini.
Tidak ada API, perubahan formatter, pytest ulang atau render besar pada
finalisasi dokumentasi. Regresi terakhir tetap **274 passed**.

## Riwayat sebelum persetujuan akhir

Catatan berikut merekam keadaan pada saat masing-masing pemeriksaan. Status
PARTIAL/PENDING penerimaan S2 di riwayat ini digantikan keputusan akhir di
atas; keterbatasan atau kegagalan output lama tidak dihapus.

## Eksperimen koreksi manual gambar S2 — 26 November 2026

**PASS TERBATAS untuk eksperimen koreksi manual pada salinan.** Pengguna
secara eksplisit meminta pengukuran posisi aktual dan mengizinkan resize
hanya jika overflow terbukti. Eksperimen benar-benar dilaksanakan, bukan
hanya rekomendasi, dan bukan implementasi kemampuan formatter otomatis.
T13 keseluruhan tetap **PARTIAL** sampai penerimaan/batas hasil S2 dengan
intervensi manual ini difinalkan. Tidak meminta ulang acceptance varian 71.

### Posisi aktual sebelum resize

Salinan `private_tests/t13_s2_image_resize_20261126/S2_before_image_resize.docx`
identik dengan output margin-only sebelumnya. Word 16.0 build 16.0.20625
membukanya read-only, print layout, repaginate dan menggulir range gambar
ke tampilan. Range awal/akhir gambar memberi posisi relatif halaman sekitar
113,25 dan 515,25 pt, sementara batas kanan teks 510,25 pt. Posisi range/caret
Word mengalami pembulatan; tidak dianggap sebagai tepi gambar presisi penuh.

Sebagai konfirmasi independen posisi objek yang benar-benar dilayout,
bounding box gambar diekstrak dari PDF hasil ekspor Word, bukan dihitung
hanya dari lebar DOCX. Tepi gambar aktual **x=113,40 sampai 515,90 pt**,
bidang teks **113,40 sampai 510,25 pt**. Overflow kanan **5,65 pt**, sekitar
**0,199 cm**. Jadi gambar benar-benar melewati batas bidang tulisan.
Utilitas pdftohtml tidak tersedia; bukti koordinat diperoleh melalui
pdfplumber bawaan runtime atas PDF Word, tanpa memasang dependensi proyek.

### Koreksi terbatas yang dilakukan

Input: `private_tests/t13_s2_replacement/S2_margin_only_after.docx`.
Output baru, tidak menimpa file mana pun:

`private_tests/t13_s2_image_resize_20261126/S2_manual_image_13_9cm_experiment.docx`

SHA-256 output eksperimen sintetis:
`4e13c23cf6b9e3d682cd8d70801e0f436c47ee87664cef4e4a68087b5bc0c299`.

Lebar gambar **14,2 → 13,9 cm**; tinggi disesuaikan proporsional menjadi
**7,228 cm**, dengan kesalahan pembulatan rasio kurang dari 0,000001. Hanya
empat atribut dimensi cx/cy pada extent gambar inline dan transform gambar
yang berubah. Media gambar asli identik byte-per-byte, tidak di-crop atau
digambar ulang. Caption, teks, tabel, hyperlink, section, margin dan semua
format selain dimensi target dipertahankan. Seluruh bagian paket selain XML
utama identik; setelah empat atribut dimensi target disisihkan, seluruh XML
utama sama. Tidak ada perubahan formatter, aturan JSON atau tesis privat.

### Word dan review seluruh halaman hasil

Word membuka output eksperimen **read-only**, menghitung ulang layout,
mengekspor tiga halaman dan menutup tanpa menyimpan. Hash input lama, salinan
input dan output eksperimen tetap sesuai manifest sebelum/sesudah pemeriksaan.

| Pemeriksaan | Sebelum margin-only / sesudah resize | Status |
|---|---|---|
| Halaman fisik Word | **3 / 3**; tidak diasumsikan dari hasil sebelumnya | PASS TERBATAS |
| Lebar/tinggi | 14,2 cm menjadi 13,9 cm; rasio sumber dipertahankan | PASS TERBATAS |
| Posisi gambar aktual pada PDF Word | x=113,40–515,90 pt menjadi **114,82–508,76 pt** | PASS TERBATAS, hasil seluruhnya di dalam batas 113,40–510,25 pt |
| Caption dan gambar | Tetap bersama pada halaman fisik 3, caption tetap sebelum gambar | PASS TERBATAS |
| Tabel | Tetap halaman 2; seluruh XML dan data 18 baris/5 kolom sama | PASS TERBATAS |
| Header/footer/nomor | Part identik, nomor tercetak tetap 1/2/3 sesuai indeks fisik yang dicatat terpisah | PASS TERBATAS |
| Halaman 1 dan 2 | PNG identik pixel dengan output margin-only pada skala 1400 px; ditinjau visual | PASS TERBATAS |
| Halaman 3 | Ditinjau seluruhnya: gambar sedikit lebih kecil, caption tetap, teks sesudah gambar bergeser naik sesuai pengurangan tinggi | Reflow diharapkan; tidak teramati clipping, distorsi atau overlap baru |
| Section/margin/isi lainnya | 1 section portrait, 4/3/3/3 cm tetap; semua teks/media/relasi dan properti non-target sama | PASS TERBATAS |

Koordinat PDF memakai point dan tidak sama dengan koordinat pixel PNG.
Ukuran DOCX akhir tepat 13,9 cm; pembulatan display Word/PDF dapat berbeda
sedikit dalam unit point. Bukti geometris akhir adalah batas gambar aktual,
bukan mengasumsikan objek muat hanya karena lebarnya di bawah 14 cm.

Bukti privat: `word_position_before.json`, `word_position_after.json`,
`word_pdf_image_bounds.json`, `manual_resize_manifest.json`, DOCX/PDF baru
serta tiga PNG pada `private_tests/t13_s2_image_resize_20261126/`.
Tidak ada klaim hasil PDF sebelum resize dibuat oleh tool ekstraksi; PDF
before berasal dari ekspor Word output margin-only pada pengujian sebelumnya.

### Status acceptance dan batasnya

- **S2 sesudah koreksi manual pada salinan: PASS TERBATAS** untuk preservasi,
  empat margin, geometri gambar yang kini muat, pagination serta review semua
  halaman pada contoh ini. Tidak ada kegagalan baru teramati.
- **Output margin-only yang belum di-resize tetap mempunyai overflow** dan
  tidak diberi PASS retroaktif. File itu tetap disimpan sebagai bukti diagnosis.
- **T13 keseluruhan: PARTIAL.** Hasil eksperimen ini belum dianggap sebagai
  persetujuan akhir operator atas alur S2 dengan koreksi manual atau izin
  memperluas cakupan. Setelah penerimaan hasil/batas ini dicatat, matriks dapat
  difinalkan untuk penutupan terbatas; tidak perlu mengulang varian 71.
- Legacy "halaman 4 S2" tetap **SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE**;
  artefak historis tidak diklaim ditemukan. Endnote belum teruji, pembaruan
  TOC/field dan manipulasi objek kompleks tetap di luar kemampuan yang diluluskan.

### Rekomendasi PREFLIGHT — belum diimplementasikan

Usulkan task terpisah untuk audit **read-only** sebelum penerapan margin:

1. Petakan gambar ke section/kolom dan hitung bidang tulisan berdasarkan
   **margin yang direncanakan**, bukan hanya margin awal. Perhitungkan
   indentasi paragraf, alignment, gutter/mirror dan konteks tabel jika jelas.
2. Bila lebar/anchor/wrapping tidak dapat dipastikan, atau dimensi menunjukkan
   risiko setelah margin dipersempit, keluarkan **NEEDS_REVIEW** dengan lokasi,
   ukuran gambar, batas bidang yang diperkirakan dan alasan. Perbandingan lebar
   saja adalah indikator risiko, bukan bukti posisi aktual.
3. Bila layout Word tersedia, bandingkan x0/x1 aktual dengan batas bidang teks
   (dan y0/y1 bila relevan), dengan toleransi pengukuran yang dinyatakan.
   Layout floating, multi-kolom atau gutter ambigu tetap perlu review.
4. Tahan tindakan terkait yang berisiko sampai operator memilih penanganan.
   Tawarkan koreksi manual pada salinan; jangan resize otomatis, mengubah
   caption atau menganggap gambar yang lebih sempit pasti berada di posisi aman.

Ini rancangan diagnostik, bukan fitur yang sudah ada, perubahan JSON atau
bukti bahwa handler margin-only produksi kini mendeteksi overflow. Kebutuhan
preflight dipisahkan dari acceptance eksperimen manual yang sudah lulus.

`git diff --check` lulus. Tidak ada pytest, render besar, API, pull, commit
atau push. Regresi terakhir tetap **274 passed**. Hanya laporan/progres dan
artefak eksperimen privat ditulis; semua sumber, output lama dan kode tetap utuh.

## Eksekusi pengganti S2 setelah persetujuan opsi A — 26 November 2026

**Opsi A disetujui eksplisit oleh operator.** Persetujuan tersebut mengganti
kriteria, bukan menyatakan tes PASS. Referensi T5 "halaman 4 S2" sekarang
**SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE**. Catatan bahwa output/screenshot
historis dan jenis nomor halamannya tidak ditemukan tetap dipertahankan.
Artefak Master tidak dipakai sebagai pengganti pengujian S2 ini.

**Hasil pengganti S2-PRESERVATION-01: PARTIAL.** Empat margin, integritas dan
subkriteria caption lulus; ditemukan masalah lebar gambar terhadap bidang
teks baru yang belum mempunyai disposisi. T13 keseluruhan tetap PARTIAL.

### Identitas dan eksekusi

| Artefak sintetis | Lokasi / SHA-256 |
|---|---|
| Input sumber | `tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx` |
| Hash input | `59eb7139d159adc40787a247ea28c4a6e9c00894d9580e13e0b54b5aa5668c77` |
| Salinan input | `private_tests/t13_s2_replacement/S2_before_reference.docx`; hash identik sumber |
| Output pengujian | `private_tests/t13_s2_replacement/S2_margin_only_after.docx` |
| Hash output | `1b151b01f528f21601ce49065c3c5944e9f960bb5cdcdf4614f886fa1af63faa` |

Input cocok byte-per-byte dengan sumber pada commit `4ef1bbd`. Handler
`format_margins` yang sudah ada dijalankan pada salinan, jenjang S2, tanpa
konfirmasi body/heading dan tanpa AI. Hasil baru disimpan ke path privat;
sumber tidak ditimpa. T14, validasi struktur dan audit ulang tetap aktif.

| Operasi di section 1 | Sebelum (cm, dibulatkan) | Sesudah (cm, dibulatkan) | Audit ulang |
|---|---:|---:|---|
| LAY-008 kiri | 2,5 | 4 | PASS |
| LAY-009 kanan | 2 | 3 | PASS |
| LAY-010 atas | 2,5 | 3 | PASS |
| LAY-011 bawah | 3,5 | 3 | PASS |

Tepat empat operasi tersebut berstatus applied. Tidak ada format body, font,
heading, caption, tabel, gambar atau hyperlink yang diubah. Pengulangan
formatter dalam memori tidak menghasilkan perubahan tambahan (idempotensi);
ini pemeriksaan hasil S2, bukan menjalankan ulang seluruh pytest.

### Integritas dan hasil Word aktual

| Aspek | Bukti aktual |
|---|---|
| Teks | Seluruh teks paragraf dan seluruh XML paragraf body identik |
| Tabel | 1 tabel, 18 baris termasuk header, 5 kolom; seluruh XML/isi identik |
| Gambar/media | 1 inline image; byte media, ukuran/drawing dan bagian paket terkait tetap sama |
| Hyperlink | 1 hyperlink; struktur, teks dan relasi terjaga, tidak diklik/diuji jaringan |
| Header/footer/field | Seluruh part dan instruksi/ref terkait identik; tampilan footer diperiksa pada semua halaman |
| Section | 1 section portrait/A4; hanya empat atribut margin berubah, properti non-target utuh |
| Paket | Semua bagian selain `word/document.xml` identik; struktur XML utama identik setelah hanya empat margin disisihkan |
| Sumber/output | Hash sumber sebelum/sesudah identik; hash kedua salinan juga tetap setelah Word |

Word **16.0 build 16.0.20625** membuka pasangan read-only, melakukan
Repaginate dan ComputeStatistics, lalu menutup tanpa menyimpan. Jumlah
halaman fisik aktual **3 → 3**, bukan dipaksakan menjadi tiga atau empat.
Seluruh enam halaman (3 sebelum + 3 sesudah) diekspor Word dan dilihat sebagai
PNG pada skala maksimum 1400 px. Tidak ada render tesis 86 halaman.

| Indeks fisik | Footer tercetak sebelum | Footer tercetak sesudah |
|---:|---|---|
| 1 | Halaman 1 | Halaman 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

Nomor footer di atas dibaca dari render, terpisah dari indeks fisik. Metadata
Word AdjustedPageNumber juga 1/2/3. Tidak ada pembaruan/rebuild field/TOC yang
dipanggil atau diklaim didukung.

### Review visual seluruh halaman

| Pasangan halaman | Sebelum / sesudah yang diamati | Penilaian |
|---|---|---|
| 1 | Judul, heading BAB I/subbab dan BAB II tetap ada; margin lebih lebar membuat wrapping lebih sempit dan BAB II bergeser lebih bawah | Reflow sesuai perubahan margin; tidak terlihat teks terpotong/bertumpuk |
| 2 | Tabel tetap seluruhnya di halaman 2, header dan data R-01 sampai R-17 terlihat; paragraf dari halaman 1 berlanjut ke sini; heading BAB III tetap terlihat | Tabel utuh, tanpa pemisahan sel/overlap baru yang terlihat |
| 3 | Gambar dan hyperlink terlihat; caption gambar yang semula di akhir halaman 2 kini di halaman 3 tepat sebelum gambar | Caption dan gambar kini satu halaman; tidak terlihat crop/overlap, tetapi ada temuan lebar bidang teks di bawah |

XML tidak menambahkan page break eksplisit; batas halaman berubah melalui
layout/reflow biasa. Caption tabel tetap di halaman 2. Caption gambar
**2 → 3**, gambar **3 → 3**: celah halaman **1 → 0**, urutan caption sebelum
gambar tetap. Pemisahan caption/gambar berasal dari input, tidak diperkenalkan
formatter, dan justru berkurang pada output. Ini hasil reflow margin, bukan
fitur formatter caption atau jaminan kepatuhan seluruh aturan caption.

### Temuan layout terukur — belum diselesaikan

Gambar dipertahankan selebar **14,2 cm**. Bidang teks sumber sekitar
**16,501 cm**; setelah margin kiri 4 dan kanan 3 cm, bidang teks menjadi
**13,999986 cm**. Gambar sekarang lebih lebar daripada bidang teks sekitar
**0,200014 cm**. Paragraf gambar center; jumlah selisih lebar tersebut bukan
pengukuran offset kiri/kanan persis pada render.

Ukuran gambar tidak rusak atau diubah, dan tidak terlihat crop/overlap pada
halaman fisik. Namun, hubungan gambar terhadap bidang tulisan baru berubah:
gambar yang muat pada bidang semula kini melebihi lebarnya. Karena pemeriksaan
margin/posisi objek diminta, masalah geometri nyata ini tidak diabaikan atau
disebut sudah lulus kepatuhan margin seluruh konten.

Penyebab terverifikasi: koreksi section mempersempit bidang teks, sementara
ukuran inline image tetap dilindungi. Tidak diubah formatter produksi atau
ukuran gambar untuk menyembunyikan temuan. **Subpemeriksaan preservasi dan
nilai margin: PASS TERBATAS; penerimaan layout hasil S2: PENDING**, sehingga
hasil keseluruhan tes pengganti **PARTIAL**, bukan PASS atau korupsi DOCX.

Tindak lanjut yang benar-benar tersisa ialah disposisi gambar ini: apakah
ukuran yang dipertahankan diterima sebagai pengecualian eksplisit pada
acceptance preservasi, atau diperlukan koreksi manual yang diizinkan pada
salinan dan pemeriksaan ulang bagian yang berubah. Tidak ada opsi tersebut
dianggap disetujui. Tidak perlu memunculkan kembali blocker artefak historis
atau meminta persetujuan varian 71 yang sudah selesai.

### Matriks T13 setelah penggantian

| Bagian | Status sekarang |
|---|---|
| Varian tesis 71 dan pengecualian 11 termasuk 401 | ACCEPTED FOR TESTING; teknis PASS TERBATAS, tetap berlaku |
| Preservasi objek Master yang sudah diuji | PASS TERBATAS, bukti tetap dipakai tanpa mengulang |
| Referensi historis halaman 4 S2 | SUPERSEDED BY REPRODUCIBLE S2 ACCEPTANCE; artefak asli tetap tidak teridentifikasi, bukan klaim tes lama PASS |
| Pengganti S2: empat margin/integritas/caption/pagination | Subpemeriksaan lulus; Word 3 menjadi 3; caption/gambar tidak terpisah lagi |
| Pengganti S2: gambar 14,2 cm versus bidang 14,0 cm | PENDING disposisi, tes pengganti PARTIAL |
| Endnote aktif | Tidak ada pada korpus; NOT APPLICABLE pada input, tidak ada klaim dukungan umum |
| Manipulasi objek kompleks, update TOC/field, aturan tanpa handler | Tetap di luar acceptance otomatis/tidak didukung, bukan PASS |
| T13 keseluruhan | PARTIAL; belum ada dasar penutupan sampai temuan S2 didisposisikan dan batas akhirnya tercatat |

Bukti aktual privat: `private_tests/t13_s2_replacement/acceptance_manifest.json`
(operasi, hash, invarian dan hasil visual), `word_evidence.json`, pasangan
DOCX, dua PDF dan enam PNG. Tidak ada data tesis privat yang disalin ke laporan
tracked; fixture S2 adalah sintetis.

`docs/TASKS.md` diberi catatan penggantian kriteria dan hasil terbaru, tanpa
menghapus laporan historis T5. Tidak ada perubahan tesis asli, formatter,
317 aturan, keputusan varian 71, API, pull, commit atau push. Regresi terakhir
**274 passed** tidak diulang; `git diff --check` lulus.

## Disposisi usulan referensi historis halaman 4 S2 — 26 November 2026

**Status catatan: UNRESOLVED LEGACY REFERENCE. Status T13: PARTIAL.**
Sumber fixture historis ditemukan, tetapi artefak hasil/screenshot dan jenis
nomor halaman yang dimaksud tidak dapat diidentifikasi dengan bukti cukup.
Bagian ini adalah usulan kriteria pengganti, **belum disetujui operator dan
belum dijalankan**. Persetujuan varian 71 tidak dibuka ulang.

### Hasil penelusuran yang dapat dipastikan

`git show 4ef1bbd:docs/T5_REPORT.md` memuat catatan "Review halaman 4" pada
baris fixture S2. Sumber fixture di commit yang sama benar-benar tersedia:

`tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx`

Byte sumber historis dan sumber saat ini **identik**. SHA-256 fixture
**sintetis, bukan dokumen tesis privat**:

`59eb7139d159adc40787a247ea28c4a6e9c00894d9580e13e0b54b5aa5668c77`

Dengan demikian, keluarga/nama dan identitas **input** tidak lagi ambigu.
Yang tetap tidak diketahui adalah file output/versi yang ditinjau, hash hasil,
screenshot masalah dan apakah "4" merupakan indeks fisik atau nomor tercetak.
Dokumen turunan T13/checklist mengulang catatan tanpa menambah identitas.
Pernyataan empat halaman pada paragraf S3 dalam T5 bukan bukti untuk S2.

Baseline S2 yang sudah diukur Word 16.0 build 16.0.20625 berjumlah **3 halaman
fisik**, satu section. Hash baseline privat cocok dengan sumber saat ini.
PDF/PNG dan `word_evidence.json` tersedia pada
`private_tests/t13_baseline_20261125_234928/`. Tabel terlihat di halaman 2;
caption gambar di 2 dan gambar di 3. Hasil itu tidak menjelaskan nomor historis
4, dan tidak membuktikan catatan historis salah. Item tersebut belum dapat
diterapkan secara reproducible pada fixture saat ini sebagai "cek halaman 4".
Tidak diciptakan file, screenshot atau hitungan halaman untuk menutupnya.

### Usulan pengganti: S2-PRESERVATION-01

Tujuan hanya acceptance preservasi objek ketika **empat margin yang sudah
didukung** diperbaiki pada fixture S2 ini. Ini bukan tugas membuat formatter
caption/objek dan bukan pembuktian kepatuhan semua aturan.

| Parameter/kriteria | Definisi konkret | Bukti yang sudah ada / yang harus dilengkapi |
|---|---|---|
| Input | Nama fixture dan SHA-256 di atas; S2, salinan baru, input tidak ditimpa | Input/hash terverifikasi termasuk kesamaan dengan commit T5 |
| Output usulan | `private_tests/t13_s2_replacement/S2_margin_only_after.docx` | **BELUM DIBUAT**; hash wajib dicatat setelah pembuatan, tidak boleh ditebak |
| Mode | Handler margin-only yang sudah ada; tanpa konfirmasi body/heading dan tanpa AI | Baru diusulkan, tidak memanggil formatter pada tahap disposisi |
| Operasi | Tepat LAY-008/009/010/011; kiri 2,5 ke 4 cm, kanan 2 ke 3, atas 2,5 ke 3, bawah 3,5 ke 3 | Rencana konsisten dengan T5 dan properti input; empat hasil harus lolos audit ulang |
| Non-target | 32 paragraf body, 1 tabel (18 baris termasuk header, 5 kolom), 1 gambar inline, 1 hyperlink, 1 section portrait/A4 | Inventaris saat ini terverifikasi; jumlah/isi/media/relasi dan properti non-target output wajib tetap sama |
| Integritas | Teks/isi tabel/media/header-footer/field/hyperlink dan struktur XML selain empat margin dipertahankan; hash input sebelum/sesudah identik | Output dan bukti before/after baru masih PENDING |
| Penomoran | Indeks fisik Word/PDF mulai 1 sebagai acuan utama; nomor yang tampil di footer dicatat terpisah | Jangan menganggap nomor tercetak sama dengan indeks tanpa memeriksanya |
| Pagination Word | Buka pasangan read-only, Repaginate, ComputeStatistics; catat versi/build, jumlah halaman kedua file, dan hash DOCX | Baseline **3** terverifikasi; jumlah halaman output **PENDING**, bukan dipaksakan 3 atau 4 |
| Objek/visual | Tinjau seluruh halaman fixture kecil ini, khususnya lokasi tabel, caption, gambar, hyperlink serta header/footer/PAGE; catat lokasi fisik sebelum/sesudah dan clipping/overlap | Sampel baseline tersedia; hasil output belum tersedia. Reflow yang sesuai perubahan margin dicatat sebagai perubahan diharapkan |
| Caption-gambar | Teks/urutan/objek terkait terjaga. Baseline caption 2, gambar 3; celah 1 halaman merupakan kondisi awal | Usulan preservasi: caption tetap mendahului gambar, celah halaman tidak bertambah dari 1, dan tidak ada clipping/overlap baru. Celah memburuk menjadi blocker; baseline terpisah tidak diklaim sudah memenuhi aturan caption |
| Laporan | Simpan manifest sumber/output/hash, empat operasi, audit ulang, lokasi objek dan hasil Word di folder privat tersebut | Manifest hasil belum dibuat; tidak menggunakan halaman Master sebagai bukti hasil S2 |

Perubahan jumlah halaman boleh terjadi akibat empat margin; yang diterima
adalah reflow yang terdokumentasi tanpa kehilangan/kerusakan objek, bukan
angka halaman tertentu. Jika dibutuhkan caption dan gambar harus selalu
satu halaman, itu kriteria lebih ketat yang perlu keputusan tersendiri;
tidak dipenuhi dengan diam-diam mengubah caption melalui formatter yang
belum mendukungnya.

Usulan terstruktur tersimpan privat pada
`private_tests/t13_complex_acceptance_20261126/s2_legacy_disposition_proposal.json`.
Field output hash/jumlah halaman dan pilihan operator masih kosong/PENDING.
Artefak usulan bukan artefak T5 lama dan tidak diberi label hasil uji lulus.

### Pemisahan matriks akhir

| Kelompok bukti | Status aktual | Penggunaan dalam penutupan |
|---|---|---|
| Tesis varian 71, pengecualian 11 termasuk 401 | ACCEPTED FOR TESTING; teknis PASS TERBATAS | Sudah diterima, tidak meminta persetujuan ulang atau membuka kasus yang selesai |
| Preservasi tabel/gambar/header-footer/field/caption | PASS TERBATAS pada pasangan/sampel yang sudah dicatat | Bukan izin memodifikasi objek atau klaim semua variasi sudah aman |
| Footnote/persamaan native/landscape Master | PASS TERBATAS pada contoh dan halaman terfokus 3/4/8 | Bukti Master tetap diberi nama Master; tidak menggantikan acceptance S2 |
| Endnote aktif | NOT APPLICABLE pada korpus yang diperiksa | Dukungan umum belum diuji; di luar klaim, bukan PASS |
| Update TOC/field, manipulasi objek kompleks dan aturan tanpa handler | Belum didukung/tidak termasuk acceptance yang diuji | Tetap dikecualikan; `manual.not-implemented` tetap `not_supported` |
| Artefak halaman 4 S2 historis | UNRESOLVED LEGACY REFERENCE | Tetap blocker saat ini; bukan klaim FAIL formatter |
| S2-PRESERVATION-01 | PROPOSED — menunggu pilihan A/B, belum dijalankan | Tidak dihitung sebagai PASS sebelum disetujui dan dibuktikan |

### Pilihan operator yang disiapkan

**A — Setujui penggantian.** Setujui S2-PRESERVATION-01 beserta batas
preservasi di atas sebagai pengganti blocker yang tidak dapat direproduksi.
Catatan T5 asli tetap disimpan sebagai UNRESOLVED LEGACY REFERENCE dengan
status *digantikan untuk acceptance*, bukan dinyatakan terbukti selesai.
Setelah A dipilih, jalankan hanya pemeriksaan S2 kecil yang diperlukan dan
lengkapi output/hash/hasil Word; A saja belum meluluskan tes pengganti.

**B — Pertahankan blocker historis.** Tidak mengganti kriteria; T13 tetap
PARTIAL sampai output/screenshot T5 yang dimaksud berhasil diidentifikasi,
jenis nomor halaman diketahui dan pemeriksaan yang relevan selesai.

**Belum ada A atau B yang dianggap dipilih.** Ini keputusan atas disposisi
catatan S2, bukan permintaan ulang persetujuan varian 71.

### Kapan T13 dapat PASS TERBATAS

| Kondisi objektif | Status T13 yang dibenarkan |
|---|---|
| A/B belum diputuskan | PARTIAL |
| A disetujui, kriteria pengganti belum dijalankan atau bukti output/Word belum lengkap | PARTIAL |
| A disetujui, pengganti lulus seluruh kriteria yang disetujui, tidak ada kerusakan baru/masalah terbuka pada scope, matriks akhir eksplisit tentang preservasi/pengecualian dan bukti terlacak | Dapat ditutup PASS TERBATAS hanya untuk cakupan yang disepakati; bukan 317 aturan atau produksi otomatis umum |
| B dipilih, artefak historis masih tidak teridentifikasi | PARTIAL |
| B dipilih, artefak berhasil ditemukan dan pemeriksaan relevannya lulus, seluruh gerbang lain terpenuhi dengan batas eksplisit | Dapat ditutup PASS TERBATAS untuk scope yang disepakati |
| Ada FAIL baru atau hasil tidak konsisten pada cakupan yang diuji | Tetap PARTIAL sampai temuan relevan diselesaikan; jangan menutupi FAIL |

Rekomendasi **A** karena mengubah blocker tak terukur menjadi pemeriksaan
preservasi S2 yang dapat diulang, tetapi keputusan tetap milik operator.
Tidak diperlukan pengulangan tesis 86 halaman atau regresi untuk disposisi
ini. Langkah berikut setelah keputusan A adalah pemeriksaan S2 terfokus saja.
Saat ini belum siap ditutup; **T13 tetap PARTIAL**.

Tahap ini hanya membaca referensi Git lokal, mencocokkan hash/inventaris input,
dan menulis dua laporan serta satu usulan privat. Tidak ada formatter,
Word/render/pytest ulang, perubahan tesis/kode/aturan, API, pull, commit atau
push. Regresi terakhir **274 passed** tetap historis; `git diff --check` lulus.

## Rekonsiliasi acceptance objek kompleks dan S2 — 26 November 2026

Pemeriksaan dilakukan di **PC rumah**, bukan mengasumsikan bukti tersedia di
laptop. `private_tests/` dan keputusan akhir operator varian 71 ditemukan.
Persetujuan **ACCEPTED FOR TESTING** tetap berlaku; tidak diminta ulang.
Tidak ada formatter dijalankan atau dokumen baru diformat pada tahap ini.

### Sumber bukti dan pemeriksaan tambahan yang diperlukan

Bukti tesis 71 digunakan kembali: 29 tabel, 15 gambar inline, dua section
portrait, 201 field body menurut Word, tujuh sampel visual, integritas sumber/
output dan pengecualian 11 paragraf. Tidak dilakukan render ulang 86 halaman.

Bukti historis `T13_REPORT.md`, `CONTROLLED_FORMATTING_PILOT_REPORT.md` dan
assertion pada `tests/test_t13_acceptance.py` / `tests/test_t5_fixtures.py`
menunjukkan preservasi paket, teks, tabel, section, field dan idempotensi pada
fixture yang diuji. Angka regresi terakhir tetap **274 passed**, tidak diulang.
Bukti historis lulus teknis tidak diubah menjadi klaim visual tanpa render.

Inventaris read-only fixture dan salinan pilot lama mengonfirmasi:

- **Dummy Master**: 112 paragraf, 3 tabel, 2 gambar inline, 6 section dengan
  section 5 landscape; 1 footnote aktif, 1 persamaan native Word, field TOC,
  hyperlink dan PAGE, 6 part header dan 6 part footer; **0 endnote aktif**.
- **S3**: 3 section, section 3 landscape, 2 tabel, 1 gambar inline; tanpa
  footnote/endnote/persamaan aktif. Bukti skip landscape dan integritas sudah
  tercatat pada tes/laporan historis, tidak dijalankan ulang.
- **Tesis privat**: tanpa landscape, footnote/endnote aktif atau persamaan
  native; part footnotes hanya separator. Header berisi penomoran; tidak ada
  part footer berisi konten pada paket tesis. Karena itu contoh footer berisi
  konten menggunakan Master, bukan mengklaim footer kosong sebagai cakupan penuh.

Pasangan Master yang sudah tersedia:
`tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx` dan
`private_tests/dummy_pilot_formatted.docx`. Perbandingan ulang pasangan ini
membuktikan seluruh bagian ZIP selain XML utama identik, seluruh teks dan XML
tabel sama, subtree persamaan/field sama, serta XML seluruh section identik.
Hanya paragraf body 44 berubah pada pasangan pilot lama, sesuai konteks pilot;
pasangan ini bukan hasil mode umum sembilan operasi T13 dan tidak disamakan
dengan pengujian lain hanya karena nama fixture sama.

Celah bukti visual Master ditutup secara terfokus: dua salinan lokal byte-identik
dibuka **read-only** di Word 16.0 build 16.0.20625, direpaginate, diekspor hanya
halaman fisik **3, 4, 8**, lalu ditutup tanpa menyimpan. Kedua dokumen **9 halaman**.
Halaman 3 dan 8 identik pixel pada skala maksimum 1400 px. Halaman 4 berubah
aliran teks setelah properti paragraf target berubah; persamaan, penanda dan
isi footnote tetap terlihat utuh, tanpa clipping/overlap baru yang teramati.
Header/footer dan nomor tercetak terlihat pada ketiga halaman. TOC masih
menampilkan placeholder cache; tidak dipanggil update field dan tidak diklaim
bahwa daftar isi sudah benar atau lengkap.

Bukti privat baru:
`private_tests/t13_complex_acceptance_20261126/word_evidence.json` dan
`integrity_visual_summary.json`, dua salinan serta enam PDF/PNG halaman terpilih.
Hash sumber dan salinan sebelum/sesudah sesuai. Bukti lama tidak dihapus.

### Matriks acceptance per jenis objek

Status merupakan **preservasi pada pasangan yang dinyatakan**, bukan validator
kepatuhan atau kemampuan memformat objek. NOT APPLICABLE hanya berarti objek
aktif tidak ada pada input yang disebut, bukan seluruh dukungan sudah diuji.

| Objek | Ada di input mana | Bukti uji/integritas | Diubah formatter? | Visual dan batasnya | Status |
|---|---|---|---|---|---|
| Tabel | Tesis 29; Master 3; S2 1; S3 2 | XML seluruh tabel tesis/Master identik; tes historis T13/T5 mempertahankan isi dan paket | Isi/properti tabel tidak diubah; layout di luar objek dapat berpengaruh | Sampel tesis diterima operator; tabel lebar Master halaman 8 identik sebelum/sesudah | PASS TERBATAS |
| Gambar/grafik | Tesis 15 inline/43 floating; Master 2 inline | Seluruh media dan struktur drawing pada pasangan tesis/Master terjaga; grafik Master berupa gambar, bukan tes semua chart native | Tidak diubah | Sampel tesis dan gambar landscape Master diperiksa; seluruh variasi chart/OLE tidak diluluskan | PASS TERBATAS untuk preservasi yang diuji; PENDING di luar cakupan |
| Header/footer | Header tesis; Master 6 header/6 footer | Part dan referensi terkait identik; konfigurasi section terjaga | Tidak diubah | Master 3/4/8 memperlihatkan header dan footer/nomor yang sama; bukan tes seluruh variasi header/footer | PASS TERBATAS |
| Footnote | Master 1 aktif; tesis 0 | Part footnotes, referensi dan struktur terkait identik pada pasangan Master; bukti tes historis juga ada | Tidak diubah | Penanda dan catatan kaki terlihat pada halaman 4 sebelum/sesudah; posisi catatan tetap di bawah halaman | PASS TERBATAS pada 1 contoh; NOT APPLICABLE untuk tesis |
| Endnote | 0 aktif pada seluruh fixture dan tesis yang diinventaris | Tidak ada konten endnote aktif untuk dibandingkan | Tidak ada target | Tidak bisa menguji tampilan endnote dari separator/konstruk yang tidak ada | NOT APPLICABLE pada korpus ini; PENDING dukungan umum |
| Field Word | TOC/hyperlink/PAGE Master; field tesis TOC/PAGEREF/SEQ dan PAGE | Paragraf field/part terkait tetap utuh; jumlah serta metadata tesis terjaga; cache/display contoh tidak hilang | Tidak ada perubahan instruksi yang diizinkan atau update field eksplisit | Master halaman 3/4 memperlihatkan cache/hyperlink; PAGE terlihat di footer. Update/rebuild TOC/tautan belum diuji | PASS TERBATAS preservasi; PENDING perilaku update |
| Persamaan native | Master 1 OMML; tesis 0 | Subtree persamaan identik | Tidak diubah | Halaman 4: persamaan terlihat utuh; pergeseran vertikal mengikuti reflow paragraf sebelumnya, bukan perubahan isi persamaan | PASS TERBATAS pada 1 contoh; NOT APPLICABLE untuk tesis |
| Section landscape | Master section 5; S3 section 3; tesis 0 | XML section Master identik; tes historis S3 membuktikan section landscape di-skip dan tetap identik | Properti landscape dilindungi, tidak dikoreksi | Master halaman 8 landscape identik pixel, tabel/gambar/caption/footer tetap terlihat; bukan klaim visual semua section S3 | PASS TERBATAS untuk Master/skip struktural S3; NOT APPLICABLE untuk tesis |
| Caption/penomoran | Tesis, Master dan S2 | Caption/field terkait tidak ditulis ulang; lokasi kandidat caption tesis tetap; konfigurasi nomor section identik | Tidak diformat/dinomori ulang | Master 3 menampilkan iii; 4 dan 8 menampilkan 1 sesuai restart. Caption objek landscape terlihat. Baseline S2 memiliki caption halaman 2, gambar halaman 3 | PASS TERBATAS preservasi/display; PENDING kepatuhan/pemisahan historis S2 |

Tidak ditemukan **FAIL baru akibat formatter** pada pasangan dan sampel yang
baru diperiksa. Status bukan jaminan konten awal benar atau aturan yang belum
memiliki handler telah didukung. Grafik/objek tertanam yang tidak ditargetkan
memiliki bukti preservasi paket, bukan bukti seluruh perilaku aplikasinya.

### Penyelidikan asal item T5 halaman 4 S2

Riwayat Git lokal menemukan pengenalan catatan tersebut pada commit
**`4ef1bbd` (`fix T5`)**, saat `docs/T5_REPORT.md` pertama ditambahkan.
Tabel aslinya menautkan S2 ke
`tests/fixtures/PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx`, dengan tindak lanjut
"Review halaman 4; pemeriksaan akhir Microsoft Word: PENDING".
`T13_WORD_CHECKLIST.md` dan `T13_REPORT.md` meneruskan catatan itu;
`TASKS.md` mengarahkan ke laporan/checklist tanpa identitas artefak tambahan.

**Yang dapat diidentifikasi:** keluarga fixture/nama sumber S2 tersebut.
**Yang tidak dapat diidentifikasi:** file hasil yang dimaksud, hash/versi
input-output, screenshot, objek spesifik dan jenis penomoran (fisik atau
tercetak). Angka empat halaman pada paragraf lain laporan T5 secara eksplisit
membahas **S3**, sehingga tidak menjadi bukti nomor halaman S2.

Bukti Word S2 yang tersedia dari sesi sebelumnya adalah baseline 3 halaman,
1 section, tabel di halaman 2 dan gambar di 3; footer memuat nomor halaman
tercetak. Itu tidak menentukan maksud nomor historis "4". Halaman fisik keempat
tesis privat tidak berkaitan tanpa bukti tambahan. Fixture S2 tidak diformat
atau dirender ulang pada tahap ini untuk menciptakan halaman keempat.

**Status: UNRESOLVED / PENDING.** Tindak lanjut paling sempit: temukan artefak
hasil/screenshot pemeriksaan T5 yang dimaksud, atau catat keputusan eksplisit
pemilik untuk menutup/mengganti item historis dengan kriteria berbasis objek
(tabel, caption dan gambar) yang jelas serta bukti yang sesuai. Ini bukan
permintaan persetujuan ulang varian 71 dan tidak ditutup diam-diam.

### Rekonsiliasi akhir dan batas penggunaan

**Selesai:** acceptance operator varian 71; preservasi teks/tabel/media dan
11 pengecualian; operasi/pagination tesis; sampel visual tesis; preservasi
serta visual terfokus footnote, persamaan, field, header/footer dan landscape
pada Master. Status bagian-bagian tersebut **PASS TERBATAS**.

**Tidak tercakup / pengecualian yang disarankan:** perubahan isi/format tabel,
gambar, caption, nomor halaman, footnote/endnote, persamaan, chart/OLE dan
struktur section kompleks tetap di luar formatter otomatis yang diterima.
Update field/TOC tidak termasuk acceptance. Endnote aktif belum teruji.
Objek yang ada hanya dipertahankan pada contoh yang diuji; dokumen lain dengan
konstruksi tersebut tetap perlu audit dan review, bukan diasumsikan aman.
`manual.not-implemented` tetap `not_supported`, bukan PASS. Batas ini tidak
mengubah handler atau memperluas persetujuan operator.

**Masih terbuka:** item T5 S2 yang belum teridentifikasi dan pencatatan batas
cakupan penutupan T13 untuk kasus yang tidak diuji. Tidak ada kebutuhan
mengulang approval 71, seluruh 86 render atau regresi 274 untuk memperbarui
matriks ini.

T13 dapat dinyatakan **PASS hanya untuk cakupan yang eksplisit** setelah:

1. Item S2 diselesaikan dengan bukti artefak/halaman yang tepat, atau keputusan
   penggantian/penutupan item historis yang eksplisit dan terdokumentasi.
2. Matriks akhir memisahkan preservasi yang sudah diuji dari objek/perilaku
   yang dikecualikan, dan batas cakupan penutupan itu disepakati. Jika endnote
   atau update field ingin diklaim didukung, bukti terfokusnya harus ada;
   jika tidak, keduanya harus tetap di luar klaim, tanpa memaksakan tes baru.
3. Tidak ada FAIL baru yang belum terselesaikan pada cakupan tersebut, dan
   artefak/hash/keputusan operator dapat ditelusuri. Dua syarat terakhir ini
   tidak mengubah keputusan ACCEPTED FOR TESTING menjadi izin produksi umum.

Saat ini **T13 tetap PARTIAL**: cakupan sempit dapat direkomendasikan, tetapi
item unresolved dan pengecualian tidak boleh dianggap sudah disetujui untuk
mengubah kriteria T13. Satu langkah berikut paling bermanfaat adalah
**menyelesaikan disposisi item historis halaman 4 S2**, bukan menambah fixture
atau mengulang acceptance tesis yang sudah diterima.

Pemeriksaan tambahan hanya inventaris/komparasi read-only dan enam halaman
render terfokus Master (3 halaman sebelum + 3 sesudah). Tidak ada render
86 halaman, formatter atau pytest ulang. Hanya dua laporan dan bukti lokal
privat ditulis; tidak ada perubahan tesis asli, formatter produksi, 317
aturan, API, pull, commit atau push. Hash sumber/copy Master tetap sesuai;
`git diff --check` lulus. Regresi terakhir **274 passed**.

## Persetujuan akhir terbatas operator — 26 November 2026

**ACCEPTED FOR TESTING — varian 71 pada salinan tesis uji ini saja.**
Operator menyatakan sudah memeriksa varian tersebut secara langsung di
Microsoft Word dan menerima hasilnya dengan batas yang disebutkan di bawah.
Ini adalah bukti pernyataan operator; tidak diklaim sebagai screenshot baru
yang diperiksa Codex. Gerbang penerimaan akhir file yang sebelumnya PENDING
**telah dipenuhi untuk pengujian terbatas ini**. Tidak perlu meminta ulang
persetujuan cakupan atau penerimaan file yang sama.

### Identitas yang diverifikasi

File tetap di lokasi privat:

`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/EXPERIMENT_NOT_OPERATOR_APPROVED.docx`

Hash file saat pencatatan cocok dengan tiga bukti sebelumnya:
`experiment_evidence.json`, `limited_scope_final_technical_acceptance.json`
dan `final_word_check.json`. Tesis sumber juga masih cocok dengan hash asal.
Hash lengkap tetap hanya pada manifest privat, sesuai kebijakan penyamaran
laporan repository. Tidak ada DOCX yang dibuka ulang untuk penyimpanan,
diubah, diganti atau diberi nama baru. Nama NOT_OPERATOR_APPROVED adalah
label historis eksperimen, bukan status persetujuan terkini.

Keputusan terbaru yang terikat hash dan daftar paragraf disimpan lokal pada:

`private_tests/t13_real_acceptance_20261125_235720/experiment_71_only/operator_final_limited_acceptance_20261126.json`

Keputusan baru ini mengatasi status menunggu penerimaan file pada catatan
sebelumnya. Bukti/keputusan lama dipertahankan sebagai riwayat, tidak dihapus
atau dipalsukan menjadi persetujuan pada tanggal sebelumnya.

### Batas keputusan operator

| Aspek | Keputusan yang benar-benar diberikan |
|---|---|
| File/cakupan | Terima hasil 71 paragraf pada salinan tesis uji ini sebagai ACCEPTED FOR TESTING |
| Operasi | 71 normalisasi spasi LAY-017 dan 3 indentasi LAY-018 yang sudah diverifikasi; tidak menambah operasi |
| Kelompok tertahan | Semua properti sumber pada 307,314,319,326,373,401,757,758,759,764,769 tetap dipertahankan |
| Paragraf 401 | Kecualikan seluruh operasi, termasuk spasi dan indentasi |
| Beta 82 | Bukan output final yang disetujui |
| Dokumen lain/produksi | Tidak ada persetujuan generik untuk semua skripsi, tesis, disertasi atau pemrosesan produksi otomatis |
| Bukti teknis sebelumnya | Tetap PASS TERBATAS: 86 halaman; teks/tabel/media/section terjaga; tujuh sampel visual varian, tanpa klaim seluruh halaman identik |
| Status T13 | PARTIAL sampai sisa kriteria acceptance terpenuhi |
| Cakupan aturan | Tidak membuktikan kepatuhan terhadap 317 aturan; aturan tanpa handler/validasi tetap belum didukung |

### Syarat tersisa sebelum T13 dapat ditutup

1. **Tuntaskan acceptance objek kompleks yang relevan atau sepakati batas
   cakupan secara eksplisit.** Tesis ini tidak mempunyai footnote aktif,
   persamaan native atau section landscape; preservasi field tidak sama
   dengan pengujian perilaku update field. Pakai bukti/fixture yang sudah
   tersedia dan pemeriksaan terfokus, bukan mengulang semua pengujian.
   Bagian belum teruji tidak boleh diberi PASS hanya dari pengujian tesis ini.
2. **Selesaikan item historis T5 "halaman 4 S2".** Sumber merujuk fixture
   sintetis S2, tetapi versi input/output dan nomor fisik/tercetak tidak
   disebutkan. Identifikasi artefak yang dimaksud atau catat keputusan
   operator tentang penyelesaian/penggantian item beserta bukti yang tepat.
   Jangan menyamakannya dengan halaman fisik keempat tesis privat.
3. **Rekonsiliasi matriks penutupan T13 dengan batas di atas.** Penerimaan
   file 71 kini selesai untuk pengujian terbatas; jangan membuka ulang gerbang
   itu tanpa perubahan file/scope atau temuan baru. Pemeriksaan visual yang
   belum dilakukan di luar sampel tetap dicatat sebagai batas bukti, bukan
   diasumsikan PASS atau otomatis memerlukan render ulang 86 halaman.

### Tahapan pengembangan yang disarankan

Prioritas berikut tetap satu task: **T13 — review terfokus matriks acceptance
objek kompleks dan item S2 menggunakan artefak yang sudah ada**. Ini paling
langsung mengurangi sisa hambatan penutupan tanpa memperluas formatter.
Setelah kriteria T13 benar-benar dipenuhi, lakukan pilot lokal pada dokumen
representatif lain dengan scope yang dikonfirmasi per dokumen, audit ulang,
proteksi T14 dan pemeriksaan hasil. Peningkatan cakupan otomatis selanjutnya
harus berdasarkan kesalahan klasifikasi/pengecualian yang terukur, dimulai
dari aturan yang sudah didukung; hasil satu tesis ini bukan izin untuk
mengotomasi seluruh aturan atau struktur akademik.

Pada tahap pencatatan ini hanya dua laporan dan satu manifest keputusan
privat baru ditulis. Tidak ada perubahan tesis, varian, kode formatter atau
aturan JSON; tidak ada API, pull, commit atau push. Word, render dan pytest
tidak diulang karena identitas/bukti konsisten. Regresi terakhir tetap
**274 passed**. `git diff --check` lulus. Status keseluruhan **T13 PARTIAL**.

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
