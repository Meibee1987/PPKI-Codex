# Peta struktur AI-first — evaluasi read-only

## Hasil dan batas bukti

Tesis privat diuji secara lokal tanpa panggilan API, perubahan DOCX, atau isi
tesis dalam laporan. Lima judul BAB yang diberikan operator cocok setelah
normalisasi spasi dan tanda baca. Lokasi berikut adalah indeks paragraf body;
akhir rentang disimpulkan dari BAB berikutnya atau kandidat daftar pustaka,
belum diverifikasi secara visual di Microsoft Word.

| BAB | Rentang paragraf | Kandidat isi | Bukti identitas lokal | Sampel mock | Nilai terukur | Kandidat perubahan | Sudah sesuai | Review |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| I | 292–334 | 14 | 11 | 5 | 10 | 0 | 10 | 10 |
| II | 335–387 | 35 | 34 | 5 | 10 | 0 | 10 | 10 |
| III | 388–411 | 11 | 10 | 5 | 11 | 0 | 11 | 9 |
| IV | 412–761 | 134 | 125 | 5 | 10 | 1 | 9 | 10 |
| V | 762–830 | 4 | 2 | 4 | 8 | 1 | 3 | 12 |

Sampel berjumlah 24 paragraf: lima kandidat pertama per BAB jika tersedia,
empat pada BAB V. Empat usulan per paragraf menghasilkan 96 keputusan: dua
kandidat pratinjau, 43 sudah sesuai, 51 review. Mock menyatakan seluruh sampel
sebagai teks isi untuk menguji gerbang, bukan hasil model sungguhan atau acuan
manual. Empat puluh label operator yang tersedia masih kosong; tidak ada dasar
menghitung akurasi atau false positive sampel. Kandidat isi berjumlah 198;
182 memiliki bukti identitas lokal menurut heuristik, bukan jaminan identitas.
Kolom nilai terukur menghitung pasangan paragraf dan aturan dengan nilai format
yang diketahui, bukan jumlah paragraf. Dari 96 keputusan mock, 49 nilai terukur
dan 47 belum diketahui; empat nilai yang terukur tetap review karena bukti
identitas paragraf belum cukup kuat.

## Perbandingan 30 kandidat awal

Pada 60 usulan untuk LAY-005 dan LAY-017, sebelum pemetaan maupun sesudahnya
hasil tetap 60 review. Sebelumnya seluruh 30 paragraf terhalang larangan global
multi-section dan tidak memiliki bukti identitas yang cukup. Peta baru memberi
bukti tambahan pada 27 paragraf dan memetakan kedua section portrait satu kolom.
Tetapi pada 60 pemeriksaan ini seluruh nilai format belum diketahui: 30 font
memiliki properti yang belum pasti dan 30 spasi tidak memiliki nilai efektif
yang dapat diverifikasi. Tidak ada perubahan teknis yang dapat disimpulkan aman.
Kedua aturan berlaku untuk S2 dan berstatus Auto; applicability dan kebijakan
Confirm/Manual bukan penyebab untuk sampel ini. Bagian kompleks dilindungi dan
tidak dikirim sebagai kandidat; hasil 60 baris bukan evaluasi seluruh objek.

## Implementasi

Peta read-only mencatat rentang BAB, bagian awal/akhir, subbab, kandidat isi,
caption, objek dan section berdasarkan lokasi. Kandidat hubungan caption dan
objek memakai kedekatan dan selalu memerlukan review. Sel tabel dipetakan ke
objek tabel, bukan menjadi teks isi. Heading Roman hanya diberi batas kandidat
terdeteksi jika terdapat urutan mulai I, minimal tiga BAB, kandidat isi di
antara BAB, dan tidak ada entri style daftar isi di antara kandidat. Heading
yang memuat drawing dapat membantu menentukan batas tetapi tetap dilindungi.
Duplikasi, urutan tidak lengkap, field/hyperlink/revisi heading, serta struktur
section yang tidak dapat dipetakan tetap memerlukan review.

Pemeriksaan section dilakukan per paragraf pada jalur pratinjau AI: batas
section, landscape, multi-kolom, struktur section ambigu, tabel, field,
footnote, hyperlink, gambar, revisi dan objek kompleks tetap ditolak. Tidak ada
perubahan pada izin formatter lama. Format harus diketahui, salah, sesuai rule,
dan diizinkan Auto; hasil yang sudah sesuai bukan usulan perubahan. Model saja
tidak dapat mengesampingkan salah satu gerbang tersebut.

## Keterbatasan dan tindak lanjut

Peta adalah heuristik: heading dan teks isi dapat memiliki kesalahan identitas,
halaman hasil render tidak dapat disimpulkan, relasi caption/objek belum pasti,
dan nilai font tema atau format yang tidak eksplisit tetap memerlukan review.
Evaluasi nyata dengan label operator serta pemeriksaan Word masih diperlukan.
Peta siap diuji secara terbatas dengan satu panggilan API berikutnya hanya
setelah persetujuan eksplisit, tetapi hasilnya belum menjadi izin format otomatis.
Pengujian tersebut tidak dilakukan pada tahap ini.

File yang berubah untuk tahap ini: `core/structure.py`, `core/ai_planner.py`,
`app.py`, `tests/test_structure_map.py` dan laporan ini. Tidak ada perubahan
rules JSON, T14, atau formatter. Regresi `python -m pytest -q`: **202 passed**,
termasuk Streamlit AppTest.
