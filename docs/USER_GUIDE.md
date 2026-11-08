# Panduan pengguna MVP v1.0 Release Candidate

Gunakan dokumen sintetis untuk uji coba sampai acceptance selesai. Pada Windows
PowerShell, dari direktori proyek dengan Python 3.12 atau lebih baru:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Buka URL lokal yang ditampilkan; hentikan aplikasi dengan Ctrl+C. Instalasi
memerlukan sumber paket; aplikasi tidak mengirim dokumen ke layanan AI/database.
Opsional, sebelum menjalankan, atur `$env:PPKI_MAX_UPLOAD_MB = "20"` untuk
menetapkan batas upload dalam MiB; nilai bawaan adalah 20.

1. Unggah DOCX dan pilih S1/S2/S3. Untuk audit teks isi, pilih style yang
   ditemukan, periksa semua paragraf kandidat dan konfirmasi cakupannya. Pilihan
   itu tidak diperlukan untuk audit halaman atau diagnostik read-only.
2. Untuk audit BAB, konfirmasi setiap kandidat Heading 1 yang benar-benar BAB.
   Pilih mode Heading saja jika hanya ingin merencanakan perbaikan BAB.
3. Klik **Audit**, baca ringkasan dan detail. `fail` adalah ketidaksesuaian yang
   terdeteksi; `needs_review` perlu pemeriksaan operator; `not_supported` berarti
   validator tidak tersedia. Diagnostik kandidat bukan bukti kepatuhan PPKI.
4. Periksa rencana Auto dan alasan dilewati. Bila sesuai, pilih **Terapkan
   Perbaikan Otomatis**. Ini hanya mengerjakan rencana yang ditampilkan.
5. Setelah validasi berhasil, unduh DOCX salinan dan laporan CSV. Input tidak
   ditimpa. Periksa dokumen hasil secara visual di Word menggunakan
   [checklist](T13_WORD_CHECKLIST.md).

Jika file ditolak, periksa pesan dan gunakan DOCX valid yang tidak terenkripsi
atau berisi VBA/ActiveX. Jika perbaikan gagal validasi, hasil tidak disediakan;
periksa dokumen dan log lokal. Detail diagnostik dapat dilihat kembali dengan
menjalankan audit lagi. Lihat [keterbatasan](KNOWN_LIMITATIONS.md).
