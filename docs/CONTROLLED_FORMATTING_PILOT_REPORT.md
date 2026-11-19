# Pilot formatting terkontrol

## Ruang lingkup dan hasil

Pilot bekerja pada salinan di memori, terpisah dari tombol AI. Operator harus
memilih dan mengonfirmasi setiap paragraf; prediksi classifier atau mock AI
tidak menjadi izin. Keputusan per paragraf–aturan membedakan nilai sesuai,
nilai tidak sesuai, nilai tidak diketahui, kelayakan normalisasi dan alasan
penolakan. Nilai tidak diketahui tidak disebut sebagai pelanggaran.

Penetapan nilai tidak diketahui hanya didukung untuk properti paragraf yang
validator pastikan sederhana dan tidak memiliki nilai eksplisit. Font dengan
nilai, theme, simbol, atau run yang tidak aman tetap dilewati. Target berasal
dari rules JSON dan mapping formatter yang telah divalidasi. Aturan non-Auto,
section tidak aman, objek, serta paragraf di luar cakupan dilewati.

| Dokumen | Kandidat isi | Paragraf dikonfirmasi | Nilai sesuai | Nilai tidak sesuai | Nilai tidak diketahui | Perubahan | Normalisasi nilai tak diketahui | Dilewati |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dummy Master | 26 | 26 (simulasi operator pada fixture sintetis) | 84 | 5 | 15 | 3 | 0 | 17 |
| Tesis privat S2 | 198 | 0 | 314 | 11 | 467 | 0 | 0 | 792 |

Jumlah merupakan pasangan kandidat–aturan, sehingga kategori nilai dan
penolakan dapat tumpang tindih. Nilai sesuai pada kandidat yang belum
dikonfirmasi bukan bukti kepatuhan PPKI dalam konteks dokumen. Tesis tidak
memakai label mock sebagai konfirmasi; semua 792 keputusan ditolak karena
identitas belum disetujui operator. Dari jumlah itu, 197 juga memiliki font
ambigu dan 108 memiliki format tak diketahui yang belum aman dinormalisasi.
Kandidat khusus yang tidak dipilih sebagai isi tidak dihitung sebagai 792.

Dummy Master menghasilkan tiga perubahan pada satu paragraf: LAY-017 dari 1,5
menjadi 1,0, LAY-018 dari 0 menjadi 1 cm, dan LAY-019 dari left menjadi
justified. LAY-005 yang struktur atau font-nya ambigu dilewati. Hasil dibuka
kembali dan audit ulang membuktikan ketiganya sesuai. Sebanyak 17 keputusan
lain dilewati karena font/theme/struktur run tidak pasti, field/objek, atau
teks menyerupai heading. DOCX asli Dummy Master dan tesis tetap identik menurut
hash. Salinan dummy tersimpan lokal di `private_tests/dummy_pilot_formatted.docx`
dan diabaikan Git; UI juga menyediakan unduhan setelah validasi.

## Integritas dan render

Validasi input T14 tetap dipanggil. Seluruh komponen ZIP selain
`word/document.xml` dipertahankan byte-per-byte, dan struktur XML utama
dibandingkan setelah hanya properti yang diizinkan dikecualikan. Hasil dibuka
ulang dan setiap properti yang diterapkan diaudit ulang sebelum tersedia.
Tes sintetis membuktikan teks, tabel, header, paragraf lain, field, hyperlink,
footnote, drawing, section, bold, italic, superscript, subscript, simbol dan
idempotensi pada kasus yang diuji. Bookmark dipertahankan pada output dan
hanya diabaikan pada salinan analisis saat audit ulang.

Microsoft Word terpasang, tetapi otomasi COM dari sandbox gagal dengan sesi
logon tidak tersedia; percobaan tersembunyi berikutnya tidak menyelesaikan
ekspor. PDF sebelum/sesudah tidak dihasilkan. **Render dan pemeriksaan visual
Word PENDING**, termasuk pagination, gambar, tabel, footer dan section. Tidak
ada hasil visual yang diklaim lulus.

## Cakupan, risiko, dan langkah berikut

Kasus sintetis membuktikan normalisasi indentasi dari nilai tak diketahui yang
aman setelah konfirmasi per paragraf; pada Dummy Master atau tesis belum ada
normalisasi nilai tak diketahui yang diterapkan. Tesis masih membutuhkan
verifikasi operator terhadap 198 kandidat isi; AI dapat membantu sebagai
diagnostik kelak, tetapi tidak memberi izin perubahan. Font theme, simbol dan
struktur kompleks masih memerlukan review. Dokumen nyata dan hasil pilot perlu
ditinjau di Word. Pilot **belum siap** diintegrasikan ke tombol perbaikan AI:
akurasi klasifikasi, persetujuan cakupan, render dan acceptance dokumen nyata
belum tervalidasi.

File tahap ini: `core/pilot.py`, `app.py`, `tests/test_pilot.py`, dan laporan
ini, serta petunjuk pilot pada `README.md`. Tidak ada perubahan rules JSON atau
formatter sebelumnya. Regresi `python -m pytest -q`: **218 passed**, termasuk
Streamlit AppTest.
