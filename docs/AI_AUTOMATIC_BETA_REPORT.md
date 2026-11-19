# AI-Assisted Automatic Formatting Beta

Status: **beta eksperimental; belum tervalidasi untuk penggunaan pada dokumen nyata**.

Alur meminta satu persetujuan pengiriman potongan teks dan penerapan pada salinan. Responses API menggunakan Structured Outputs, maksimal 30 kandidat per permintaan. Respons tidak lengkap, ID berbeda, schema salah, atau kegagalan API membatalkan seluruh batch. Tes menggunakan mock; tidak ada panggilan API nyata. Rules, isi input dan pengamanan T14 tidak diubah.

AI hanya memilih fungsi paragraf; kode Python memeriksa konteks BAB, struktur, section, cakupan aturan dan keamanan operasi secara independen. Formatter pilot membatasi operasi ke LAY-005, 017, 018 dan 019 yang diizinkan rules, memeriksa ulang hasil dan integritas paket sebelum menyediakan unduhan. Kandidat terlindungi atau ambigu tidak diterapkan. Laporan CSV berisi pengecualian dan alasan per aturan yang dilewati. File masukan tidak ditimpa.

## Evaluasi lokal tanpa API

Mock secara sengaja memberi label `body` pada semua kandidat yang dikirim. Ini **bukan ground truth**, bukan hasil AI nyata, dan tidak membuktikan keselamatan perubahan pada tesis. Hasil disimpan hanya di memori; file sumber diverifikasi tidak berubah melalui hash.

| Dokumen | Kandidat lokal | auto_candidate mock | protected | uncertain | Belum dikirim | Operasi sesuai | Operasi diterapkan | Normalisasi nilai tidak diketahui | Operasi ditolak |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy Master | 23 | 23 | 638 | 16 | 0 | 80 | 3 | 0 | 9 |
| Tesis lokal S2 | 198 | 30 | 1440 | 216 | 168 | 60 | 30 | 30 | 30 |

Jumlah protected dan uncertain mencakup elemen tabel yang dilaporkan classifier, bukan hanya paragraf body. Angka operasi dihitung hanya untuk kandidat yang diberi label mock `body`. Validasi integritas dan audit ulang lulus pada salinan dalam memori; ini tidak mencakup pemeriksaan tampilan Microsoft Word.

## Pengujian dan batasan

- Tes sintetis menunjukkan perubahan DOCX tanpa konfirmasi per paragraf, normalisasi nilai yang tidak diketahui, pelestarian teks, tabel, bold dan italic, dan idempotensi. AppTest memeriksa persetujuan dan dua unduhan menggunakan mock.
- Kutipan bertanda dikenali dan dilindungi; kutipan tanpa penanda dapat menyerupai body. AI dapat salah dan belum memiliki acuan operator untuk mengukur kesalahannya. Jangan menganggap keluaran mock sebagai izin pada tesis nyata.
- Belum ada jalur deterministik yang membuktikan identitas isi tanpa dukungan AI atau operator. Pemilihan style saja tidak memadai untuk membedakan kutipan. Kandidat di luar 30 pertama tidak diproses.
- Font tema, simbol, field, hyperlink, revisi, gambar, tabel, section kompleks dan format ambigu dapat dilewati oleh pemeriksaan lokal. Perlindungan tidak berarti seluruh kemungkinan OOXML telah diuji.
- Pemeriksaan visual Microsoft Word dan evaluasi AI nyata masih PENDING. Sebelum menggunakan pada dokumen nyata, ukur kesalahan klasifikasi terhadap label operator dan periksa salinan di Word. Panggilan API berbayar berikutnya memerlukan persetujuan tersendiri.
- Pengujian lengkap: `python -m pytest -q` menghasilkan **232 passed**, termasuk Streamlit AppTest dengan mock.

File implementasi: `core/ai_beta.py`, `app.py`, `tests/test_ai_beta.py` dan laporan ini.
