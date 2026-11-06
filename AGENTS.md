# Instruksi untuk Codex — PPKI Academic Formatter

## Tujuan

Bangun MVP lokal yang **andal, sederhana, aman untuk isi DOCX**, dan bisa saya pakai sendiri untuk jasa format 20–30 dokumen per bulan. Baca `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/ERD.md`, dan `docs/TASKS.md` sebelum mengubah kode.

## Aturan wajib

1. **Kerjakan hanya task yang diminta**, bukan seluruh roadmap sekaligus. Jangan melakukan refactor besar tanpa kebutuhan nyata.
2. Stack: **Python 3.12+, Streamlit, python-docx**; gunakan `lxml` hanya bila fitur OOXML perlu dan ada tesnya. Pakai library standar untuk JSON, logging, hash, zip, dan path.
3. **Dilarang menambah** microservices, FastAPI, Next.js, Docker, Supabase client, SQLite, Redis, Celery, LangChain/CrewAI, autentikasi, atau pembayaran untuk MVP ini.
4. `rules/ppki_rules_all.json` adalah **sumber data aturan**. Jangan mengubah `rule_code`, `official_requirement`, `expected_value_pattern`, `validation_key`, atau memalsukan asal pedoman.
5. `is_implemented` dari Supabase **bukan bukti** bahwa handler kode sudah bekerja. Keberadaan fungsi dan tes passing yang menentukan kemampuan aplikasi.
6. `validation_key = manual.not-implemented` harus dilaporkan sebagai **belum didukung**. Jangan mengeksekusi atau diam-diam mengklaim lulus.
7. **Default audit/dry-run**; perubahan hanya dilakukan setelah pengguna memilih tindakan. `fix_mode=Auto` adalah aturan yang _boleh diotomasi jika handler aman_, `Confirm` butuh persetujuan eksplisit, `Manual` tidak diubah otomatis.
8. **Jangan mengubah teks penelitian**, sitasi, persamaan, isi tabel, gambar atau footnote. Jangan set `paragraph.text` untuk memformat. Jangan mengganti keseluruhan dokumen menjadi dokumen baru berbasis teks.
9. Selalu simpan hasil ke file baru; **jangan timpa input**. Jika struktur kompleks/ambigu, **skip + laporkan** daripada menebak.
10. **Tidak boleh mengunggah** dokumen pengguna ke AI/cloud tanpa opt-in eksplisit. Untuk MVP, tidak ada network call.
11. Kode sederhana, fungsi kecil, type hints seperlunya, exception yang dapat ditindaklanjuti, tes `pytest` untuk setiap handler baru. Tidak perlu abstraksi generik besar.
12. Aturan yang tampil di UI harus berasal dari JSON PPKI, **bukan dari contoh umum**. Contoh: margin atas **3 cm**, spasi isi **1,0**, bukan nilai skripsi generik.

## Batasan yang harus dijaga

- Mendukung `.docx` dulu. `.doc`, PDF, OCR, dan konversi format masuk backlog.
- Tidak perlu memproses 317 aturan sekaligus. Mulai dari subset **9 aturan LAY** di `docs/TASKS.md`.
- Untuk `applies_to` yang belum terpetakan tegas, jangan terapkan otomatis; tandai butuh review.
- Error harus menghasilkan pesan jelas, bukan dokumen yang diam-diam rusak.

## Pola jawaban setelah menyelesaikan task

- **Dikerjakan:** ringkasan singkat.
- **File berubah:** path file.
- **Tes:** perintah dan hasil nyata; jika tidak dapat dijalankan, jelaskan penyebab.
- **Risiko/keterbatasan:** spesifik, tidak ditutup-tutupi.
- **Langkah berikutnya:** satu task berikut di `docs/TASKS.md`, bukan pekerjaan tambahan yang tidak diminta.

## AI Model Usage Policy

Default Model: GPT-6.1 Terra
Reasoning: Medium

Gunakan model default untuk seluruh pekerjaan PPKI Academic Formatter.

### Aturan Pergantian Model

1. Gunakan GPT-6.1 Terra (Medium) untuk:
   - Membuat fitur aplikasi
   - Mengembangkan Python Formatter
   - Mengintegrasikan Supabase Rules
   - Membuat UI Streamlit
   - Debugging sederhana
   - Unit testing

2. Rekomendasikan GPT-6.1 Sol (High) jika:
   - Bug sulit diselesaikan setelah 2 percobaan
   - Perubahan melibatkan banyak modul
   - Manipulasi DOCX sangat kompleks
   - Terjadi masalah arsitektur yang signifikan

3. Rekomendasikan GPT-6 Astra hanya jika:
   - Sol belum berhasil menyelesaikan masalah
   - Dibutuhkan analisis arsitektur mendalam

### Instruksi Wajib

Jika suatu tugas membutuhkan model lebih kuat:

- JANGAN langsung melanjutkan dengan pendekatan rumit.
- Berhenti dan beri rekomendasi pergantian model.
- Jelaskan alasan pergantian.
- Sebutkan model dan reasoning yang disarankan.
- Berikan prompt untuk melanjutkan pekerjaan.
- Tunggu keputusan pengguna.

Jangan melakukan overengineering.

Setelah tugas kompleks selesai, sarankan kembali
ke GPT-6.1 Terra (Medium).

Pergantian model dilakukan manual oleh pengguna.
