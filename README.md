# PPKI Academic Formatter — Codex Starter Pack

## Menjalankan aplikasi T0

Gunakan Python 3.12 atau lebih baru. Di PowerShell, dari folder proyek:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Buka alamat lokal yang ditampilkan Streamlit. Untuk berhenti, tekan Ctrl+C di terminal.
Instalasi dependensi membutuhkan akses ke sumber paket; aplikasi sendiri tidak memakai API atau database.

Pada T0, unggah DOCX dan pilihan S1/S2/S3 tersedia, tetapi Audit belum diimplementasikan.
Aplikasi tidak membaca isi atau menyimpan berkas unggahan sebagai hasil, dan tidak mengubah dokumen asli.
Aturan yang tersedia di `rules/ppki_rules_all.json` belum dimuat; pemuat aturan termasuk T1.

Dokumentasi siap pakai untuk membangun **MVP lokal** pemformat skripsi (S1), tesis (S2), dan disertasi (S3). Digunakan sendiri oleh penyedia jasa, sekitar **20–30 dokumen/bulan**.

## Mulai dari sini

1. Buka folder ini sebagai **workspace/repository** di Codex (bukan menyalin prompt panjang saja).
2. Minta Codex membaca `AGENTS.md` dan `docs/PRD.md`, `docs/ERD.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`.
3. Mulai dari **T0** di `docs/TASKS.md`. Kerjakan **satu task per giliran**; review hasil dan tesnya sebelum melanjutkan.
4. Gunakan `rules/ppki_rules_all.json` sebagai snapshot resmi dataset; `rules/ppki_rules_mvp25.json` untuk daftar kandidat aturan yang pernah ditandai implemented.
5. Ketika aplikasi sudah jadi, jalankan di laptop lewat Streamlit. Gunakan **DOCX contoh tanpa data pribadi** untuk pengujian.

## Prompt pertama untuk Codex

```text
Baca AGENTS.md dan semua file dalam docs/ terlebih dahulu.
Kita membangun PPKI Academic Formatter untuk penggunaan pribadi 20–30 DOCX per bulan.
Gunakan rules/*.json yang tersedia; jangan membuat ulang rules PPKI.
Kerjakan HANYA Task T0 dari docs/TASKS.md.
Jangan menambah database baru, hosting, Docker, framework agent, atau OpenAI API pada tahap ini.
Setelah selesai, jalankan pengujian yang relevan dan laporkan: file yang diubah, hasil tes,
serta batasan yang masih ada. Jangan lanjut ke task lain tanpa instruksi.
```

## Urutan baca

- `docs/PRD.md`: **apa** yang perlu jadi dan apa yang tidak.
- `docs/ERD.md`: **data** apa yang sudah ada (bukan desain database baru).
- `docs/ARCHITECTURE.md`: **cara** membangunnya secara sederhana.
- `docs/TASKS.md`: **urutan langkah**, tiap langkah punya kriteria selesai.
- `AGENTS.md`: **aturan kerja Codex** di repository.

## Keputusan yang sengaja sederhana

- Satu aplikasi **Python + Streamlit + python-docx**.
- **Tanpa login**, tanpa frontend/backend terpisah, tanpa server online.
- **Tanpa database lokal**: cukup JSON rules dan file laporan per pekerjaan.
- **Tanpa API AI pada MVP pertama**; AI kelak hanya membantu mengenali struktur yang ambigu.
- **Tanpa sinkronisasi Supabase langsung** pada MVP. Update rules dilakukan dengan ekspor ulang JSON secara sengaja.
- Berkas DOCX asli tidak diubah. Semua pemformatan menghasilkan salinan baru.

> Penting: dataset rules yang dilampirkan adalah hasil ekspor, bukan bukti bahwa semua rules bisa dieksekusi. `is_implemented=true` hanyalah metadata. Validator dan formatter harus benar-benar memiliki implementasi serta tes.
