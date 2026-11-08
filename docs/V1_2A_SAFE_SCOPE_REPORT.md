# v1.2A — Pratinjau cakupan formatting read-only

## Cakupan dan perlindungan

Fungsi `safe_format_scope` pada [structure.py](../core/structure.py) hanya
menghasilkan baris lokasi, jenis, keputusan, aturan dan alasan; tidak mengubah
DOCX atau rencana formatter lama. Kosong, pemisah section, objek/field kompleks,
heading, caption, daftar, tabel, pustaka, lampiran dan bagian khusus yang
dikenali dikeluarkan dari cakupan teks isi. Konteks yang belum pasti masuk
`needs_review`. `protected` berarti tidak diproses oleh cakupan teks isi;
beberapa paragraf isi yang kompleks juga masuk kategori ini.

`auto_safe` adalah **label eksperimental dry-run**, bukan otorisasi formatter.
Kandidat dibatasi pada struktur sederhana, style Body Text dalam konteks BAB
yang terdeteksi, serta properti aturan Auto yang dapat diperiksa oleh validator
yang tersedia. Nama style sendiri tidak membuktikan identitas isi. Aturan font,
spasi, indent dan alignment diperiksa terpisah; aturan yang tidak dapat
diverifikasi atau tidak Auto tidak dicantumkan. Hitungan usulan perubahan hanya
meliputi paragraf dengan status `fail` yang memenuhi kriteria tersebut. Tidak
ada keputusan heading otomatis.

## Pengukuran read-only

Hitungan mencakup paragraf body kosong dan paragraf sel tabel yang terdeteksi;
lokasi sel gabungan dihitung sekali. Tesis diuji sebagai S2. Sumber diperiksa
dengan hash sebelum/sesudah dan tidak berubah.

| Dokumen | auto_safe | needs_review | protected | Paragraf dengan usulan perubahan |
| --- | ---: | ---: | ---: | ---: |
| Dummy Master | 0 | 16 | 661 | 0 |
| Tesis lokal | 0 | 42 | 1644 | 0 |

Untuk kedua dokumen jumlah `auto_safe` per jenis dan per aturan LAY-005,
017, 018 dan 019 adalah **0**. Tes sintetis terpisah menunjukkan bahwa paragraf
isi sederhana dengan properti eksplisit dapat masuk `auto_safe` dan aturan
perubahan dipisahkan per properti. Hasil tersebut tidak mengukur akurasi pada
dokumen nyata.

## Sampel dan kesalahan

Pada tesis, lima BAB acuan, lima entri daftar isi acuan, ringkasan, summary,
caption contoh, sel tabel, heading pustaka dan lampiran contoh tidak masuk
`auto_safe`. Tidak ditemukan false positive `auto_safe` pada sampel tersebut;
ini bersifat trivial karena seluruh tesis menghasilkan nol kandidat otomatis,
bukan estimasi precision. Contoh kandidat isi dari BAB I–V masing-masing adalah
paragraf 294, 337, 390, 414 dan 764: empat `protected` karena struktur kompleks
dan satu `needs_review` karena konteks. Ini menunjukkan cakupan yang dapat
terlalu konservatif; tanpa acuan manual keselamatan untuk setiap aturan, jumlah
false negative **belum diketahui**. Contoh risiko lain: paragraf yang menyerupai
teks isi dapat sebenarnya berupa kutipan atau bagian khusus; identitas semantik
tidak dapat dipastikan dari style dan konteks saja.

## Pengujian dan keputusan

Baseline: **137 passed**. Regresi setelah perubahan: **141 passed**, termasuk
Streamlit AppTest, uji bagian khusus, field, tabel, aturan per properti,
determinisme dan file sumber yang tetap utuh. Tidak ada API atau dependency baru.

**Belum cukup dapat dipercaya untuk mengaktifkan formatter otomatis v1.2B.**
Kandidat sintetis bukan acuan keselamatan dokumen nyata, dan dua dokumen sampel
belum menghasilkan cakupan otomatis. Sebelum aktivasi, buat label acuan manual
per paragraf dan per aturan pada beberapa dokumen anonim, ukur false positive
dan false negative, serta verifikasi integritas dan render Word setelah uji
terkendali. Sampai itu selesai, pertahankan konfirmasi lama dan dry-run ini.

File berubah: [structure.py](../core/structure.py), [app.py](../app.py),
[test_safe_scope.py](../tests/test_safe_scope.py), [README.md](../README.md),
[TASKS.md](TASKS.md), dan laporan ini. Pemeriksaan akhir Word tetap PENDING.
