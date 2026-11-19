# AI Beta v0.3 — validasi klasifikasi dan kesiapan

Status: **uji API terbatas siap disiapkan oleh operator; klasifikasi AI nyata dan kelayakan pemformatan tesis belum tervalidasi**. Tidak ada panggilan API nyata selama pengembangan atau pytest.

## Audit 198 menjadi 88

Perbandingan mengulang gerbang kandidat sebelumnya dan saat ini pada tesis lokal S2 secara read-only. Dari 198 kandidat lama, 88 tetap masuk dan 110 tertahan; tidak ada kandidat baru di luar himpunan awal. Jumlah berikut **hanya untuk 110 yang berubah status**, bukan seluruh elemen dokumen. Kategori adalah alasan gerbang, bukan ground truth fungsi paragraf.

| BAB | Indentasi kiri langsung positif | Panjang dan pola sitasi | Total ditahan |
|---|---:|---:|---:|
| I | 0 | 2 | 2 |
| II | 3 | 4 | 7 |
| III | 0 | 0 | 0 |
| IV | 99 | 0 | 99 |
| V | 2 | 0 | 2 |
| **Jumlah** | **104** | **6** | **110** |

Pada selisih ini tidak ada yang berpindah karena gerbang struktur Word atau konteks BAB ambigu: kedua gerbang tersebut sudah berlaku pada 198 kandidat awal. Indentasi atau pola sitasi tidak membuktikan kutipan. Kandidat mungkin terlalu konservatif ditahan, tetapi jumlah yang benar-benar teks isi belum diketahui tanpa label operator. Tidak ada yang dianggap sudah sesuai karena tertahan.

## Evaluasi klasifikasi

Sampel lokal tersusun deterministik secara bergiliran per BAB, maksimum 15 kandidat. Pada tesis ini distribusinya I–V adalah 4, 3, 3, 3, 2. Sampel hanya berisi kandidat yang lolos gerbang lokal, sehingga tidak representatif untuk menghitung false positive seluruh dokumen atau mengevaluasi 110 yang tertahan. Tidak ada label tesis yang diada-adakan. Penilaian operator pada panel evaluasi bersifat opsional dan hanya disimpan dalam sesi lokal; nilai PENDING dan belum yakin tidak dianggap label benar.

Pada subset sintetis berlabel kecil dari pengujian beta sebelumnya terdapat 1 true positive, 0 false positive, 0 false negative dan 1 kutipan ditahan untuk review; precision 1/1 hanya untuk subset ini dan tidak boleh digeneralisasi. Tes memeriksa heading, caption, daftar isi, pustaka, lampiran, field dan kutipan berindentasi tidak menjadi body. Kasus AI yang menyebut bagian terlindungi sebagai body ditolak oleh batas ID/cakupan lokal. Kutipan tanpa penanda maupun indentasi masih dapat menyerupai body dan keliru diterima: ini risiko serius yang belum diukur terhadap ground truth nyata.

## Mode evaluasi API

Panel **Uji Klasifikasi AI — Tanpa Mengubah DOCX** menampilkan maksimum 15 kandidat beserta konteks lokal dan perkiraan biaya sebelum persetujuan terpisah. Hanya klik pengiriman setelah persetujuan yang dapat memanggil Responses API; hasil menampilkan klasifikasi, alasan, token jika tersedia dan biaya perkiraan dari harga yang diisi. Mode ini tidak memanggil formatter. Error tidak memodifikasi input. Harga dan token perkiraan bukan jaminan batas tagihan, dan respons dapat memuat informasi privat dalam sesi lokal. API key yang pernah terekspos harus dirotasi sebelum digunakan.

Mode ini dapat dipakai untuk **satu uji klasifikasi terbatas** setelah operator memeriksa sampel, harga dan menyetujui pengirimannya. Hasil saja tidak membuktikan keamanan formatter atau mengizinkan pemakaian otomatis pada tesis. Perlu label pembanding dan pengujian risiko bagian khusus, serta acceptance visual sebelum menilai hasil format untuk penggunaan nyata.

## Integritas dan pemeriksaan Word

Formatter pilot mempertahankan validasi T14, pemeriksaan struktur, audit ulang dan pelestarian paket; tes yang ada mencakup teks, paragraf, tabel, gambar/drawing, field, hyperlink, section, bold, italic, superscript, subscript dan simbol pada kasus sintetis yang diuji. Ini bukan jaminan semua fitur OOXML atau layout visual aman. Tesis tidak diubah; hash tetap sama setelah pembacaan.

Microsoft Word **PENDING**: percobaan otomasi sebelumnya gagal dan tidak diulang. Untuk pemeriksaan manual, buka `tests/fixtures/PPKI_MASTER_Dummy_Uji_Lengkap_v1.docx` dan `private_tests/dummy_pilot_formatted.docx` di Word, gunakan View → Side by Side, lalu periksa pagination, margin/section, heading, tabel, gambar, caption dan nomor halaman. Kedua file tersedia lokal saat validasi ini; jangan mengubah file asli.

## Hasil tes dan file

Hasil regresi akhir: `python -m pytest -q` — **238 passed**, termasuk Streamlit AppTest. File yang diubah: `core/ai_beta.py`, `app.py`, `tests/test_ai_beta.py`, `docs/WORK_PROGRESS.md` dan laporan ini. Rules JSON, formatter, dokumen asli dan T14 tidak diubah.
