# Final Beta Safety Integration

Status: **jalur Beta telah diuji secara teknis dengan mock; validasi AI nyata dan pemeriksaan visual Word masih PENDING**. Ini bukan pernyataan siap produksi.

## Kesetaraan pengamanan

Evaluasi dan jalur Beta kini memakai fungsi keputusan konservatif yang sama. Proposisi dan lanjutan daftar yang dikenali dilindungi sebelum pemilihan kandidat. Label `quote` untuk bukti sitasi tanpa penanda kutipan menjadi `uncertain`; kutipan yang dikenali dan bagian terlindungi tetap dilindungi. Indentasi ambigu tidak memperoleh izin. Sampel evaluasi dan label CSV tidak dapat dipakai sebagai izin formatter. Formatter tetap memeriksa kembali identitas kandidat, aturan Auto, keselamatan operasi, integritas paket dan audit ulang.

Mock pada tesis dengan label pembanding menunjukkan dua false positive terdahulu berstatus `protected`; lima sampel yang sebelumnya masih perlu review berstatus `uncertain`. Label CSV tidak dipakai untuk membuat keputusan ini. Heuristik tidak menjamin semua kutipan, daftar atau struktur Word dapat dikenali.

## Hasil alur mock end-to-end

Jumlah berikut adalah **operasi per paragraf dan aturan**, bukan jumlah paragraf. Tabel dan elemen non-paragraf tidak dihitung sebagai operasi. `applied` hanya dikeluarkan setelah formatter, integritas dan audit ulang sukses; `already_compliant` berarti properti yang diperiksa tidak memerlukan penulisan. `failed` pada tabel adalah nol karena kedua hasil lulus validasi; kegagalan kritis membatalkan seluruh DOCX dan menyediakan CSV kegagalan untuk operasi yang sempat direncanakan, tanpa mengklaim hasil berhasil.

| Dokumen | Kandidat AI mock | applied | already_compliant | protected | uncertain | failed |
|---|---:|---:|---:|---:|---:|---:|
| Dummy Master | 23 | 3 | 80 | 292 | 73 | 0 |
| Tesis privat S2 | 88 | 91 | 171 | 2660 | 662 | 0 |

Mock memberi label `body` kepada setiap kandidat yang dikirim. Ini **bukan hasil AI nyata atau bukti kebenaran klasifikasi tesis**. Tesis diproses pada salinan dalam memori; hash input tetap sama dan output dapat dibuka serta lulus validasi paket dan audit ulang. Tidak ada API nyata dan tidak ada file tesis dimasukkan ke Git. Hasil salinan tidak digunakan sebagai dokumen siap pakai.

CSV operasi pada aplikasi memuat ID, rule_code, nilai sebelum/sesudah jika diperiksa, target, status dan alasan. Nilai yang tidak diperiksa ditandai demikian, bukan dianggap sesuai. Status `applied` bukan rencana: ia hanya muncul setelah pemeriksaan selesai. Jika validasi kritis gagal, hasil dan unduhan DOCX dibatalkan.

## Integritas dan batasan

Pilot mempertahankan isi XML di luar properti target serta seluruh bagian paket DOCX lain secara byte-per-byte. Tes sintetis mencakup teks, tabel, drawing/gambar, field, hyperlink, section, bold/italic, superscript/subscript dan simbol pada kasus yang diuji. Pemeriksaan ini tidak memastikan semua variasi Word atau layout visual; pemeriksaan Microsoft Word tetap PENDING. Klaim cakupan keseluruhan dokumen dan akurasi AI tidak dapat dibuat dari 20 sampel.

Satu uji API nyata **untuk klasifikasi terbatas** dapat dilakukan operator setelah persetujuan pengiriman dan pemeriksaan biaya. Uji Beta yang menghasilkan salinan tesis masih bersifat eksperimental dan belum direkomendasikan sebagai hasil siap pakai: kutipan tanpa penanda masih dapat salah diidentifikasi, ground truth terbatas, dan pemeriksaan visual belum dilakukan. File sumber harus tetap disimpan dan hasil diperiksa operator di Word.

Regresi akhir: `.\.venv\Scripts\python.exe -m pytest -q` — **245 passed**, termasuk Streamlit AppTest; saat integritas gagal hanya laporan kegagalan tersedia dan unduhan DOCX tidak ditampilkan.
