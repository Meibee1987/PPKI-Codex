# Evaluasi 20 sampel pembanding

Dua berkas yang diberikan operator ditemukan di folder Downloads dan dibaca langsung secara lokal. Keduanya tidak disalin ke repository. Dua puluh ID, BAB, dan kelompok pada CSV cocok dengan sampel tesis yang dipersiapkan. CSV tidak memuat hash dokumen, sehingga kecocokan metadata tidak membuktikan asal label; operator tetap perlu memeriksa sumber.

Prediksi yang tercatat dalam CSV dibandingkan dengan label operator, bukan hasil API baru. Prediksi mentah: **7 TP, 8 TN, 2 FP dan 3 FN** (15 dari 20 cocok). Kedua FP berkaitan dengan proposisi dan lanjutan daftar; ketiga FN merupakan sitasi dalam teks yang diprediksi sebagai kutipan langsung.

Pada pembandingan ulang dengan bukti lokal dan prediksi yang sama: **5 TP, 10 TN, 0 FP, 0 FN dan 5 tidak pasti**. Dua bagian khusus yang sebelumnya salah diterima sekarang dikenali sebagai proposisi atau lanjutan daftar; tiga sitasi yang sebelumnya disebut kutipan menjadi tidak pasti, bukan otomatis teks isi. Dua paragraf berindentasi yang sebelumnya benar diprediksi body juga tetap tidak pasti. Jadi angka kesalahan yang turun disertai lima abstensi; ini **bukan bukti peningkatan akurasi AI** atau estimasi kualitas pada seluruh tesis.

Pengenalan membedakan sitasi yang mengandung tahun dari bukti kutipan langsung, serta mendeteksi proposisi P1/P2 dan lanjutan daftar berindentasi yang memiliki bukti lokal. Indentasi teks isi yang tidak mempunyai bukti daftar tidak disamakan dengan kutipan, tetapi tetap membutuhkan review sebelum formatting. Tidak semua daftar atau kutipan Word dapat dikenali dengan heuristik sederhana.

CSV label dapat diimpor ke panel evaluasi. ID, BAB, dan kelompok wajib cocok tepat; duplikasi, label tidak valid, dan sampel berbeda ditolak. Kolom prediksi CSV ditampilkan sebagai prediksi yang belum diverifikasi. Label tersimpan dalam sesi lokal dan tidak memberi izin formatter. Tidak ada panggilan API baru, perubahan tesis asli, perubahan rules, atau perubahan pengamanan formatter.

Regresi akhir: `.\.venv\Scripts\python.exe -m pytest -q` — **244 passed**. Dua tes terfokus impor Streamlit dan perlindungan proposisi/daftar dijalankan kembali setelah penyesuaian terakhir — **2 passed**.
