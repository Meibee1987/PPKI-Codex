# Keterbatasan MVP v1.0 Release Candidate

- Acceptance dokumen nyata anonim dan pemeriksaan visual akhir Microsoft Word
  masih **PENDING**; jangan gunakan untuk pekerjaan pelanggan sebelum selesai.
- Validator hanya mencakup 12 aturan pada [daftar kemampuan](MVP_CAPABILITIES.md).
  Hasil diagnostik dan aturan tanpa handler memerlukan pemeriksaan manual.
- Pemilihan style tidak membuktikan semua paragraf adalah isi; operator wajib
  memeriksa cakupan. Font tema, simbol dan run kompleks, default Word yang tak
  diketahui, field, hyperlink dan numbering otomatis dapat memerlukan review.
- Formatter halaman melewati section landscape, berkolom atau ambigu. Heading
  BAB hanya kandidat Heading 1 yang dikonfirmasi dengan struktur aman; subbab,
  penomoran dan titik tidak diperbaiki. Perubahan huruf besar pada judul BAB
  yang disetujui perlu diperiksa secara visual.
- Keamanan ZIP memiliki batas 20 MiB input secara default, 2.000 entri,
  200 MiB dekompresi dan rasio 1.000 per entri; batas input memakai variabel
  `PPKI_MAX_UPLOAD_MB`. Bytes sudah diterima Streamlit sebelum validasi aplikasi.
  Pemeriksaan bukan antivirus atau sandbox dan tidak menjamin keamanan Word.
- Integritas otomatis memeriksa konstruksi yang diuji; tata letak, pagination,
  semua objek tertanam dan relasi Word kompleks belum dapat dijamin. Tinjau
  secara manual menggunakan [checklist Word](T13_WORD_CHECKLIST.md).
- Requirement paket menyatakan batas minimum, bukan versi terkunci; instalasi
  baru dapat menghasilkan versi berbeda dari environment yang diuji.
- Input `.doc`, PDF, OCR, nomor halaman otomatis, daftar isi otomatis,
  cloud, AI API dan database berada di luar cakupan ini.
