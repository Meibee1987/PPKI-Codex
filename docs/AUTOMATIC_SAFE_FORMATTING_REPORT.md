# Automatic Safe Formatting — status belum selesai

## Hasil utama

Jalur `auto_verified` dan tombol perbaikan tanpa konfirmasi per paragraf **belum
diaktifkan**. Sinyal lokal yang ada belum membuktikan identitas teks isi secara
andal, dan belum tersedia label operator yang cukup untuk mengukur false positive.
Pemeriksaan sintetis menunjukkan bahwa kutipan khusus tanpa penanda Word dapat
memakai style `Body Text` dan struktur yang sama dengan teks isi: classifier
lama mengembalikan `safe_to_apply=true`. Tes regresi memastikan pilot yang
belum dikonfirmasi tetap menolak perubahan. Menggunakan flag tersebut sebagai izin otomatis dapat
melanggar perlindungan bagian khusus.

Tidak ada API yang dipanggil atau rules JSON yang diubah. Pengecekan T14 dan
formatter yang ada tetap aktif. Tes baru tidak mengklaim bahwa classifier telah
memecahkan perbedaan semantik tersebut.

Regresi `python -m pytest -q`: **219 passed**, termasuk Streamlit AppTest.
Tes keamanan yang diperbarui juga dijalankan terpisah: **1 passed**.

## Evaluasi lokal

| Pengukuran | Hasil |
| --- | ---: |
| Kandidat teks isi tesis | 198 |
| Paragraf yang diotorisasi otomatis tanpa konfirmasi | 0 |
| Nilai kandidat terukur sesuai | 314 |
| Nilai kandidat terukur tidak sesuai | 11 |
| Nilai kandidat tidak diketahui | 467 |
| Perubahan otomatis diterapkan | 0 |
| Normalisasi otomatis dari nilai tidak diketahui | 0 |
| Keputusan per paragraf–aturan yang memerlukan review | 792 |

Angka nilai adalah pasangan kandidat–aturan dan bukan bukti bahwa kandidat
merupakan teks isi atau melanggar PPKI. Jumlah paragraf yang sesungguhnya dapat
aman diformat otomatis belum diketahui; nol adalah jumlah yang diotorisasi karena
jalurnya belum dibuat. Tidak ada file tesis yang diubah; output
pilot tanpa konfirmasi identik dengan input. Ketidakpastian identitas dan konteks
menghalangi 792 keputusan; beberapa juga memiliki nilai format tak diketahui
atau struktur yang tidak aman. Terdapat 198 kandidat yang masih membutuhkan
penilaian operator atau bantuan diagnostik; AI tidak boleh menjadi izin tunggal.

Dummy Master sebelumnya memiliki **tiga perubahan pada pilot terkonfirmasi**,
bukan perubahan pada jalur otomatis baru. Belum ada perubahan otomatis baru
pada Dummy Master maupun tesis. Salinan pilot yang telah dihasilkan sebelumnya
tetap tersedia secara lokal, tanpa menimpa sumbernya.

## Keterbatasan dan langkah lanjutan

Kasus seperti kutipan tanpa penanda, bagian khusus dengan style umum, heading
ambigu, font tema, field dan objek kompleks memerlukan bukti tambahan atau
review manusia. Perlu acuan operator pada sampel representatif beserta uji
false positive sebelum suatu pendekatan dapat dianggap aman; tidak ada dasar
untuk menjadikan hasil AI saja atau aturan panjang teks sebagai izin formatter.
Tombol otomatis dan integrasi OpenAI untuk penerapan belum layak diaktifkan.

Pemeriksaan visual Microsoft Word **PENDING**: percobaan otomasi sebelumnya
gagal dan tidak diulang tanpa batas. Sumber dan salinan dummy tersedia untuk
dibandingkan menggunakan [checklist visual](AUTOMATIC_SAFE_FORMATTING_VISUAL_CHECKLIST.md).
