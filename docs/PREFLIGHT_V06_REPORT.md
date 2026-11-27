# Preflight otomatis v0.6 - risiko overflow gambar

**Acceptance akhir 27 November 2026: PASS TERBATAS.** Alur yang diwajibkan
berhasil pada browser nyata terisolasi yang mengakses Streamlit lokal, dan
DOCX unduhannya berhasil dibuka read-only serta dirender oleh Microsoft Word.
Tidak ada perubahan kode/tes produksi pada acceptance ini; hasil pytest
terakhir tetap **299 passed, 0 failure/error/skip**, tidak dijalankan ulang.
Bagian di bawah menjadi acuan terkini; catatan pengembangan sebelumnya
dipertahankan sebagai riwayat. T13 tetap PASS TERBATAS tanpa perlu dibuka ulang.

## Acceptance aplikasi dan Word sebelum commit

Aplikasi benar-benar dijalankan dari interpreter `.venv` proyek:
`python -B -m streamlit run app.py --server.address 127.0.0.1 --server.port 8507 --server.headless true --browser.gatherUsageStats false`.
Tidak ada consent/tombol AI diaktifkan. Hanya fixture sintetis S2 dan salinan
lokal digunakan. Browser membatasi request ke server lokal; tidak ada request
eksternal teramati pada skenario yang selesai.

### Pemisahan sumber bukti

| Metode | Bukti aktual | Batas klaim |
|---|---|---|
| Unit/AppTest sebelumnya | 299 pytest dan 30 tes terfokus terakhir, JUnit/log tersimpan; hash kode/tes sekarang masih sama | Tidak diklaim sebagai pemeriksaan antarmuka desktop/manual |
| Browser aplikasi nyata | Microsoft Edge headless melalui Playwright, HTTP/WebSocket Streamlit nyata; unggah input, keyboard/click, scroll tabel, screenshot, unduh CSV dan DOCX | Pengujian browser otomatis, bukan AppTest/mock atau pemeriksaan manual operator; tidak memakai state internal aplikasi untuk menentukan hasil |
| Microsoft Word | Word 16.0 build 16.0.20625 benar-benar membuka pasangan salinan read-only; repaginate/count; ekspor PDF output | Word COM dan review render mesin Word, bukan mock, LibreOffice, hitung page-break atau klaim operator melakukan pemeriksaan baru |
| Review visual | Ketiga halaman PDF keluaran Word dirender Poppler 1400 px lalu ditinjau; screenshot browser ditinjau terpisah | Tidak mengklaim pengujian GUI Word manual atau semua konstruksi DOCX |

### Matriks alur Streamlit nyata

| Pemeriksaan | Hasil | Status |
|---|---|---|
| S2 14,2 cm | NEEDS_REVIEW sebelum apply; 1 gambar, paragraf 26/section 1, dimensi dan alasan dapat dibaca pada tabel dengan scroll | PASS TERBATAS |
| Margin direncanakan | Tabel nyata memperlihatkan bidang awal sekitar 16,5012 cm, bidang setelah rencana sekitar 14,0 cm dan selisih +0,2 cm; warning bukan karena gambar sudah overflow pada margin awal | PASS TERBATAS |
| Review belum disetujui | Unduhan laporan memperlihatkan kiri 2,5 -> 2,5 cm dan kanan 2 -> 2 cm, status uncertain dengan alasan PREFLIGHT | PASS TERBATAS |
| Operasi aman tetap berjalan | Atas 2,5 -> 3 cm dan bawah 3,5 -> 3 cm diterapkan; dua operasi saja. DOCX diunduh melalui tombol aplikasi | PASS TERBATAS |
| Pembatalan review | Checkbox dapat diubah dengan keyboard; check/uncheck menghapus keluaran lama yang konteks review-nya berubah | PASS TERBATAS |
| Dokumen A/B | A yang direview diganti B dengan geometri sama tetapi bytes berbeda; checkbox B tidak disetujui | PASS TERBATAS |
| Perubahan jenjang | S2 -> S1 -> S2 membatalkan persetujuan lama setelah rerender selesai | PASS TERBATAS |
| Perubahan rencana | Review umum ditandai, rencana diubah ke heading-only lalu dikembalikan; review umum tidak terbawa | PASS TERBATAS |
| S2 13,9 cm | PASS lebar sederhana, 1 gambar/0 perlu review, tidak ada checkbox risiko. Empat margin sudah sesuai; 0 diterapkan dan tidak ada DOCX perubahan ditawarkan | PASS TERBATAS |
| Resize otomatis | Gambar unduhan 14,2 cm tetap 14,2 cm; media dan XML objek identik | Tidak dilakukan, sesuai batas |

Review di dalam skenario browser adalah tindakan uji sintetis oleh agen, bukan
persetujuan operator baru untuk keluaran pelanggan atau izin resize. Tidak ada
penerapan margin berisiko pada dokumen yang belum direview dalam keluaran Word
yang dinilai di sini.

### Bukti Word atas unduhan browser

Pasangan lokal:
`private_tests/preflight_v06/acceptance_20261127/S2_source_readonly_copy.docx`
dan `S2_browser_held_horizontal.docx` pada folder yang sama. Hash source
sintetis masih cocok dengan fixture T13. SHA-256 output unduhan browser:
`13bcfe19c26151c704e768f712b42151db6301fd841a40cb5d6a32ba1e5a3aea`.

- Word membuka keduanya tanpa error: **3 -> 3 halaman**, 1 section portrait,
  1 tabel dan 1 gambar inline. ReadOnly true; hash tetap setelah ditutup tanpa
  penyimpanan.
- DOCX: **32 -> 32 paragraf**, tabel 18x5 dan seluruh XML tabel sama. Seluruh
  bagian paket selain document.xml identik; setelah hanya atribut margin
  atas/bawah disisihkan, seluruh XML utama identik. Teks, caption, hyperlink,
  header/footer, field, section dan gambar tidak diubah.
- Word mengonfirmasi kiri 70,85 pt dan kanan 56,7 pt tetap, atas/bawah 85,05 pt.
  Lebar/tinggi gambar tetap 402,5/209,3 pt. Ini bukti margin yang ditahan tidak
  diterapkan diam-diam, bukan klaim keempat margin PPKI telah diperbaiki.
- Semua tiga halaman output ditinjau: heading/teks terbaca; tabel header dan
  R-01 sampai R-17 lengkap pada halaman 2; gambar utuh pada halaman 3;
  tidak teramati clipping atau overlap baru. Footer tercetak Halaman 1/2/3.
- Caption gambar tetap halaman 2, gambar halaman 3 pada kedua file Word.
  Pemisahan ini **sudah ada pada input**, tidak diperkenalkan preflight;
  fitur ini tidak memperbaiki hubungan caption/gambar otomatis.
- PDF Word mengonfirmasi bbox gambar halaman 3 x=103,48-505,98 pt berada dalam
  bidang horizontal yang dipertahankan. Pemeriksaan ukuran saja tidak
  menggantikan bukti posisi aktual ini.

### Artefak, keterbatasan driver dan kesiapan sinkronisasi

Bukti privat pada `private_tests/preflight_v06/acceptance_20261127/`:
`acceptance_summary.json`, `browser_output_integrity.json`, `word_acceptance.json`,
CSV unduhan, DOCX, PDF/PNG Word serta screenshot/teks browser. Skenario browser
awal yang tidak selesai tetap tersimpan; hasil lengkap direkonsiliasi dari
empat pemeriksaan `browser_attempt3/browser_acceptance_3.json` dan tiga
pemeriksaan `browser_remaining4/browser_remaining4.json`. Tidak diklaim
bahwa seluruh skrip eksplorasi sempat lulus satu run tanpa kendala.

Opera yang dipakai bersama memiliki fokus berubah, sehingga tidak dipakai
sebagai dasar acceptance. Pada driver Edge, input checkbox berlapis label
memerlukan keyboard Space; selectbox memakai pencarian keyboard; assertion
menunggu rerender untuk menghindari membaca widget lama sementara. Ini
penyesuaian harness, bukan perbaikan aplikasi. Toolbar dataframe Download as
CSV tidak menghasilkan event unduhan headless dalam 30 detik; penyebab belum
dikonfirmasi dan ekspor toolbar opsional ini belum diluluskan. Tombol laporan
margin CSV/DOCX aplikasi berhasil diunduh dan digunakan sebagai bukti.

Tidak ditemukan blocker pada cakupan preflight/penahanan yang diwajibkan.
**Siap untuk tahap review diff dan commit/push aman atas instruksi terpisah**,
dengan hanya kode/tes/dokumentasi aman. Remote belum dibandingkan pada tugas
ini dan tidak ada pull/commit/push. Semua data privat/artefak tetap diabaikan
Git. Risiko floating/tabel/gutter/mirror/posisi kompleks tetap perlu Word;
PASS bukan jaminan semua layout atau seluruh 317 aturan terpenuhi. Konfirmasi
review juga bukan perbaikan gambar: override margin tetap perlu keputusan
operator dan pemeriksaan hasil.


## Riwayat implementasi dan regresi v0.6

**Status 27 November 2026: SELESAI TEKNIS, 299 passed.** Regresi penuh terakhir
lulus tanpa failure/error/skip setelah perbaikan konfirmasi lintas dokumen.
Tes terfokus terakhir 30 passed. Tidak ada kegagalan yang masih terbuka.
Acceptance Word untuk alur v0.6 adalah langkah berikutnya; T13 sebelumnya
tetap PASS TERBATAS, tidak diulang atau diperluas.

Implementasi lokal menggunakan arsitektur audit/rencana/formatter/Streamlit
yang ada. Tidak menambah dependensi atau mengubah aturan PPKI. Pemeriksaan
berdasarkan struktur DOCX, bukan mesin layout Word. T13 tetap PASS TERBATAS
pada korpus yang diterima; fitur baru ini mempunyai pengujian tersendiri.

## Cara kerja

`core.preflight.image_preflight(data, planned_changes)` membaca bytes input,
memvalidasi paket dengan pengamanan T14, lalu menghitung ukuran halaman dan
bidang tulisan setiap section berdasarkan perubahan yang benar-benar menjadi
kandidat formatter. Target menggunakan mapping PAGE_RULES yang sudah ada,
bukan nilai generik atau perubahan JSON. Pembulatan mengikuti satuan twip
penyimpanan DOCX. Tanpa rencana, ukuran saat ini yang diperiksa.

Setiap drawing inline, anchor dan gambar legacy VML pada body didaftar dengan
lokasi dan section jika pasti. Header/footer/footnote/endnote yang memuat
objek juga diperiksa secara konservatif tanpa menebak section-nya. Laporan
memuat lebar gambar, bidang sebelum/sesudah, bidang paragraf, selisih dan
alasan. Isi penelitian tidak disalin ke laporan.

PASS hanya untuk satu gambar inline biasa pada paragraf tersendiri dengan
geometri satu kolom yang dapat ditentukan; indentasi nonnegatif yang diketahui
diperhitungkan. Toleransi satu twip (0,05 pt) hanya untuk pembulatan nilai,
bukan toleransi clipping. Pemeriksaan ini tidak menentukan pagination, posisi
vertikal, pemisahan caption atau seluruh tampilan Word.

| Status | Arti |
|---|---|
| PASS | Tidak ditemukan pelanggaran lebar pada kasus sederhana yang dihitung; bukan penerimaan visual seluruh dokumen |
| NEEDS_REVIEW | Potensi overflow, atau ukuran/posisi/konteks tidak pasti; periksa di Word |
| NOT_APPLICABLE | Tidak ada gambar/drawing relevan yang ditemukan pada story yang diperiksa |

Gutter/mirror, section continuous, kolom khusus, gambar dalam tabel/textbox,
floating/anchor/VML, gambar bercampur teks/field/tab/daftar, indentasi khusus,
rotasi/efek, extent tidak valid dan story yang section-nya tidak diketahui
memerlukan review. Nilai bidang/selisih yang tidak dapat ditentukan dilaporkan
kosong, bukan dijadikan hasil pengukuran pasti. Lebar bidang halaman yang
tercatat tidak dianggap sebagai lebar sel tabel.

## Integrasi dan kebijakan margin

`candidate_changes` mempertahankan pemilihan kandidat handler lama.
`plan_changes` dan `format_docx` kini memeriksa kandidat tersebut dengan
preflight. Secara default, hanya perubahan horizontal terkait (ukuran halaman,
margin kiri/kanan) pada section berisiko yang ditahan. Margin atas/bawah,
section aman dan operasi paragraf lain tetap mengikuti pengamanan sebelumnya.

`image_reviewed_sections` adalah konfirmasi eksplisit per section pada
pemanggilan formatter, bukan perubahan aturan Auto/Confirm/Manual. Konfirmasi
ini tidak melewati perlindungan gutter, mirror, landscape atau pengamanan
T14 dan tidak mengubah NEEDS_REVIEW menjadi PASS. Menyetujui risiko tidak
memperbaiki gambar. Tidak ada resize/crop/move atau perubahan caption otomatis.

Streamlit menampilkan hasil otomatis sebelum tombol margin deterministik,
serta hasil untuk rencana umum termasuk ukuran kertas sesudah audit. Pengguna
melihat jumlah gambar, jumlah perlu review, lokasi, ukuran dan alasan, beserta
saran pemeriksaan Microsoft Word. Review margin dan umum terpisah dan terikat
hash sumber serta laporan/rencana; perubahan input/rencana atau pembatalan
review menghapus keluaran terkait yang sudah tidak sesuai konteks.

## Hasil S2 lokal

Deteksi baru dijalankan pada sumber sintetis S2 dan salinan manual 13,9 cm
yang sudah diterima. Tidak ada penyimpanan ulang atau render Word baru.

| Input | Rencana/kondisi | Hasil |
|---|---|---|
| PPKI_T4B_02_Tesis_S2_Tabel_Gambar.docx, paragraf 26 / section 1 | Gambar 14,2 cm; empat kandidat margin; bidang sesudah sekitar 13,999986 cm | NEEDS_REVIEW, selisih +0,200014 cm |
| S2_manual_image_13_9cm_experiment.docx, paragraf 26 / section 1 | Gambar 13,9 cm; margin sudah 4/3/3/3; bidang sekitar 13,999986 cm | PASS lebar sederhana, sisa sekitar 0,099986 cm |

Hash keduanya cocok dengan bukti T13 dan tetap sama setelah preflight
berulang. Bukti hanya lokal di
`private_tests/preflight_v06/s2_detection_20261126.json`. Penerimaan manual S2
sebelumnya tidak diubah menjadi izin resize otomatis atau persetujuan untuk
semua dokumen. Default pada sumber S2 menahan kiri/kanan, dapat memperbaiki
atas/bawah; empat margin tetap dapat dijalankan setelah review eksplisit.

## Pengujian dan batas dukungan

Tes sintetis mencakup lebar 14,2/13,9, tanpa gambar, gutter/mirror, kolom,
continuous, tabel, anchor, header, indentasi, teks campuran, extent hilang,
VML/rotasi, pemetaan section, integritas media/paket, idempotensi laporan,
penahanan selektif dan review eksplisit. AppTest memeriksa tampilan, konfirmasi,
pembatalan review, pergantian input dan kemandirian dua alur. T5 handler lama
juga diuji dengan simulasi review eksplisit; ini bukan persetujuan operator baru.

### Kelanjutan regresi - 27 November 2026

Workspace diverifikasi di PC rumah, branch `main`, commit dasar `44a606a`.
Seluruh perubahan implementasi/tes sebelumnya masih ada. Sesi terhenti karena
usage limit; implementasi tidak dimulai ulang. Catatan kegagalan tersedia pada
output percakapan sebelumnya: **5 failed, 293 passed** dari 298 tes.
Tidak ditemukan log regresi penuh tersimpan sebelum sesi lanjutan ini.
Cache `lastfailed` berisi `{}` dan tidak dipakai sebagai daftar kegagalan:
regresi sebelumnya dijalankan dengan `-p no:cacheprovider`.

| Tes yang pernah gagal | Klasifikasi dan akar penyebab | Perbaikan yang dipertahankan |
|---|---|---|
| test_streamlit_beta_consent_and_download | Regresi nyata; kondisi alur Beta membaca margin_preflight_key sebelum variabel dibuat | Syarat preflight diletakkan hanya pada tombol margin; alur Beta memakai validasi semula |
| test_master_beta_result_rerun_and_stale_state_are_safe | Regresi nyata dengan akar NameError yang sama | Perbaikan kondisi yang sama; assertion rerun dan stale-state tetap |
| test_incomplete_operation_report_never_produces_download | Regresi nyata dengan akar NameError yang sama | Perbaikan kondisi yang sama; assertion penolakan hasil tidak lengkap tetap |
| test_streamlit_displays_diagnostics_without_body_confirmation | Ekspektasi UI lama: dataframe[1] sekarang adalah tabel preflight, bukan findings audit | Pilih tabel melalui kolom rule_code/status/message; assertion diagnostik tidak dilonggarkan |
| test_master_streamlit_checkboxes_are_independent_of_body_style | Ekspektasi indeks dataframe yang sama | Pemilihan tabel berdasarkan kolom; assertion konfirmasi heading tetap |

Perbaikan tersebut sudah tersimpan dan lima tes lulus sebelum sesi terputus.
Sesi lanjutan memeriksa diff dan menjalankan kembali hanya kelimanya bersama
24 kasus preflight: **29 passed in 45.79s**. Kelima kegagalan lama selesai tanpa perubahan tambahan. Pemeriksaan berikutnya
menemukan satu celah review terpisah yang dijelaskan di bawah. Perubahan pada T5 menggunakan
simulasi review section secara eksplisit agar kemampuan handler historis
tetap diuji; kebijakan default tanpa review diuji terpisah di test_preflight.
Tidak ada tes dinonaktifkan. Tidak ada bukti kegagalan lingkungan/tidak stabil
atau kegagalan belum terklasifikasi dari lima kegagalan ini. Peringatan cache
pada run 72 tes awal tidak menyebabkan kegagalan dan cache lama tidak dihapus.

Regresi pada keadaan yang diwarisi: **298 passed in 174.90s**. Setelah itu,
satu celah berikut direproduksi dan diperbaiki sebelum hasil akhir dinyatakan:

- Tes baru `test_streamlit_review_does_not_transfer_to_other_document_with_same_geometry`
  membuktikan konfirmasi checkbox dapat terbawa ke dokumen lain ketika laporan
  geometri sama. Sebelum perbaikan: **1 failed**, tersimpan pada
  `private_tests/preflight_v06/review_hash_reproduction_20261127.log`.
- Ini regresi nyata pada cakupan persetujuan, bukan perubahan ekspektasi tes.
  Perbaikan empat baris pada `app.py`: kunci widget kini mencakup **SHA-256
  sumber, jenjang, laporan/rencana dan alur**. Dua dokumen berbeda tidak berbagi
  review, termasuk ketika ukuran dan lokasi gambar sama. Penanganan gambar,
  aturan serta formatter OOXML tidak diubah oleh perbaikan ini.
- Kelima tes lama dan seluruh 25 kasus preflight sesudah perbaikan:
  **30 passed in 45.25s**. Review dapat dibatalkan dan alur umum/margin tetap
  terpisah. Tes baru tetap dipertahankan sebagai regresi.

Regresi penuh final sesudah perbaikan hash: **299 passed in 179.79s**,
**0 failed, 0 errors, 0 skipped**, diverifikasi dari JUnit. Tidak ada kegagalan
yang belum diselesaikan. Baseline sebelum v0.6 adalah 274 tes; kini ada 25
kasus preflight tambahan. Pengulangan full suite mempunyai alasan teknis
nyata: kode berubah untuk menutup bug yang dibuktikan tes baru, bukan
mengulang tes hijau tanpa perubahan.
Log baru dan JUnit disimpan hanya di folder privat yang diabaikan Git:

- `private_tests/preflight_v06/targeted_resume_20261127.log` dan `.xml`.
- `private_tests/preflight_v06/regression_final_20261127.log` dan `.xml`: 298 tes sebelum perbaikan hash.
- `private_tests/preflight_v06/targeted_hashfix_20261127.log` dan `.xml`: 30 tes sesudah perbaikan.
- `private_tests/preflight_v06/regression_hashfix_final_20261127.log` dan `.xml`: regresi akhir sesudah perbaikan hash.

Perintah terfokus: `pytest tests/test_preflight.py` beserta lima node ID pada
tabel di atas, `-q -p no:cacheprovider`. Regresi final:
`.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider --junitxml=private_tests/preflight_v06/regression_hashfix_final_20261127.xml`.
Satu regresi penuh final dijalankan setelah perbaikan hash dan tes terfokus lulus; run 298 tes sebelumnya tetap disimpan sebagai riwayat.

Hash sumber S2 dan salinan manual masih cocok dengan bukti deteksi sebelumnya;
hasil S2 digunakan kembali, tidak merender ulang Word atau tesis. Tidak ada
perubahan JSON, DOCX sumber, tesis, atau acceptance T13. Git pull/commit/push
dan API berbayar tidak dilakukan.

Preflight tidak mengubah field/TOC, endnote, objek kompleks atau gambar.
Dukungan manipulasi tersebut tetap belum tervalidasi. Ukuran/posisi yang
bergantung layout Word tetap membutuhkan operator; tidak ada klaim seluruh
317 aturan PPKI dipenuhi atau semua keluaran otomatis aman secara visual.

Langkah berikutnya: acceptance Word terfokus untuk alur UI preflight dan
keluaran margin pada fixture S2, dengan hash input/output serta keputusan
review yang dicatat. Tidak perlu merender ulang tesis 86 halaman.


## File v0.6 yang berubah

- Kode: `core/preflight.py` (baru), `core/formatter.py`, `app.py`.
- Tes: `tests/test_preflight.py` (baru), `tests/test_t5_fixtures.py`,
  `tests/test_citation_diagnostics.py`, `tests/test_heading_audit.py`.
- Dokumentasi: laporan ini, `docs/WORK_PROGRESS.md`, `docs/TASKS.md`.

Perubahan T13_WORD_VISUAL_ACCEPTANCE_REPORT.md yang sudah ada adalah progres
acceptance sebelum v0.6; tetap dipertahankan dan tidak ditulis ulang pada
kelanjutan ini. Tidak ada perubahan rules atau fixture DOCX. Semua bukti privat,
log dan hasil eksperimen tetap di private_tests yang diabaikan Git.


## Kesiapan commit dan batas rilis

Kode/tes/dokumentasi v0.6 sudah layak menjadi kandidat commit secara teknis:
299 tes lulus, perubahan terfokus dan diff diperiksa. Sinkronisasi GitHub
memerlukan instruksi terpisah serta pemeriksaan remote dan isi staged saat
itu; pull, commit atau push tidak dilakukan pada tugas ini. private_tests,
DOCX privat, log serta hasil eksperimen tetap dikecualikan. Hash sumber S2,
hasil manual, tesis/varian 71 dan rules tetap cocok dengan catatan sebelum
verifikasi ini.

Kesiapan commit bukan penerimaan visual seluruh layout atau rilis produksi
umum. Gutter/mirror, floating, tabel, rotasi dan posisi yang tidak pasti tetap
konservatif; manipulasi objek, update field/TOC/endnote dan resize otomatis
tidak diluluskan. Tahap berikutnya tetap acceptance Word terfokus alur S2.
