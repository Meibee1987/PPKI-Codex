# Progres Automatic Safe Formatting

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
