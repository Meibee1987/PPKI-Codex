# AI Beta v0.4 — evaluasi cakupan read-only

Status: **siap untuk uji klasifikasi AI terbatas dengan persetujuan; belum layak dipercaya untuk memformat tesis nyata tanpa validasi pembanding dan pemeriksaan Word**. Tidak ada API nyata yang dipanggil saat pengembangan atau pytest.

## 110 kandidat tertahan

Audit read-only mengulang selisih 198 ke 88 pada tesis lokal. Dari 99 kandidat berindentasi di BAB IV, **99 mempunyai indentasi kiri langsung** pada paragraf. Pemeriksaan tidak menemukan `w:numPr` langsung atau pada rantai style, indentasi kiri eksplisit pada rantai style, atau field, hyperlink, drawing, object dan footnote reference pada kelompok ini. Pemeriksaan metadata tersebut tidak membuktikan apakah indentasi sengaja dipakai sebagai kutipan, daftar, layout lain, atau format isi. Asal perubahan dan maksud penulis tidak dapat diketahui dari metadata ini. Hash file asli tetap sama.

Sebanyak 104 kandidat total ditahan karena indentasi langsung dan enam karena gabungan panjang paragraf dan pola sitasi. Semua **110 berpotensi** ditahan terlalu konservatif, tetapi jumlah yang benar-benar teks isi atau aman diformat **belum diketahui** tanpa label operator. Tidak ada aturan pemformatan yang dilonggarkan.

## Sampel evaluasi

Panel read-only menyiapkan paling banyak 20 sampel, dengan kuota 5 kandidat lolos, 7 indentasi, 3 pola sitasi, dan 5 bagian khusus bila tersedia. Pemilihan bergiliran antarbab dalam masing-masing kelompok. Pada tesis, 20 sampel tersedia dengan distribusi kelompok 5/7/3/5; distribusi BAB I–V 4/5/2/4/3, ditambah dua elemen di luar BAB yang dipetakan. Ini sampel terarah, bukan sampel acak atau estimasi populasi.

Panel menunjukkan teks dan konteks secara lokal, bukti struktur dan status lokal; pengiriman membutuhkan persetujuan khusus. Operator dapat memberikan label `teks_isi`, `bagian_khusus`, atau `tidak_pasti` sebelum pemanggilan AI; label disimpan hanya dalam sesi lokal. Respons AI, label dan bukti dapat dibandingkan melalui ID; TP, FP, FN dan kasus belum terukur dihitung hanya dari label yang ada. Label PENDING dan tidak pasti bukan ground truth. Tidak ada label tesis yang diberikan dalam pekerjaan ini, sehingga akurasi, false positive dan false negative tesis **belum dapat dihitung**.

Kasus sintetis memaksa mock AI menyebut bagian terlindungi sebagai `body`; status lokal tetap terlindungi dan formatter menolak seluruh sampel evaluasi. Ini membuktikan pemisahan izin pada skenario tes, bukan akurasi AI. Kutipan tanpa petunjuk khusus dapat disalahklasifikasi; mendeteksinya masih memerlukan pembanding manusia. Sampel belum memiliki izin otomatis untuk formatting meskipun AI menjawab `body`.

## Risiko dan langkah berikutnya

- Label sampel dan pengujian API nyata masih PENDING; lakukan uji terbatas hanya setelah memeriksa sampel, biaya dan menyetujui pengiriman dalam aplikasi. Rotasi API key yang pernah terekspos.
- Batas anggaran API bersifat estimasi, bukan jaminan batas tagihan. Konteks sampel akan dikirim ke penyedia jika disetujui.
- Validasi XML dan audit ulang bukan bukti layout visual; pemeriksaan Microsoft Word masih PENDING.
- Jangan gunakan hasil klasifikasi tunggal untuk memperluas izin formatter. Tesis asli, rules JSON, formatter dan pengamanan T14 tetap dipertahankan.

Regresi: `python -m pytest -q` — **239 passed**, termasuk Streamlit AppTest. AppTest evaluasi juga dijalankan kembali setelah penyesuaian label sebelum pemanggilan.
