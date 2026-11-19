# Integrasi awal AI-first — pratinjau

## Diagnosis pratinjau pertama

Pada pemeriksaan lokal ulang terhadap 30 kandidat pertama tesis privat (S2),
masing-masing 30 pemeriksaan LAY-005 dan LAY-017 berstatus `needs_review`,
dengan nilai properti belum dipastikan, identitas teks isi dan konteks BAB belum
dikonfirmasi, serta style ambigu. Tidak satu pun lolos `safe_to_apply`. Ini
menjelaskan mengapa gerbang lokal menolak usulan dalam cakupan tersebut; respons
mentah dan identitas sampel dari panggilan pertama tidak tersedia untuk memastikan
apakah ada penyebab tambahan dari AI atau bahwa sampelnya identik.

Kode sebelumnya menyatukan semua penyebab menjadi satu pesan. Pratinjau kini
menampilkan alasan spesifik per usulan dan token input/output/total jika API
melaporkannya. Error permintaan, timeout, penolakan model, batas output,
JSON tidak terbaca, dan schema lokal yang tidak cocok dibedakan. Jika respons
tidak lengkap, tidak ada rencana parsial. Hasil berupa 60 baris dari kode lama
menunjukkan respons tersebut melewati pemeriksaan status `completed`, tetapi
jumlah token panggilan pertama tidak tersimpan. Karena itu kecukupan 4096 token
untuk dokumen atau panggilan lain belum dapat disimpulkan.

Pengujian diagnosis memakai mock dan dokumen sintetis; tidak ada panggilan API
nyata atau pengiriman ulang tesis. Pengaman tidak dilonggarkan dan pratinjau
tetap tidak mengaktifkan formatter. Regresi diagnosis: 181 pytest lulus,
termasuk Streamlit AppTest; tes khusus planner: 28 lulus.

## Status dan arsitektur

Tahap ini menyediakan analisis dan pratinjau saja. Validasi input T14 berjalan
sebelum ekstraksi. `core/structure.py` memilih kandidat teks isi; paling banyak
30 kandidat dan 180 karakter per kandidat dikirim sekali melalui OpenAI Python
SDK Responses API dengan Structured Outputs. Aturan dan target berasal dari
JSON lokal; teks dokumen diperlakukan sebagai data, bukan instruksi. Tidak ada
akses ke eksekusi kode atau formatter dari respons AI.

Operator menentukan model yang tersedia pada akun, mengatur `OPENAI_API_KEY`
melalui environment, dan secara eksplisit menyetujui pengiriman. `OPENAI_MODEL`
opsional menjadi nilai awal model. Permintaan menggunakan `store=False`, tanpa
retry otomatis, dan output dibatasi 256–4096 token (awal 1024). Batas kandidat
dan panjang kutipan membatasi input, tetapi bukan jaminan batas biaya total.
Tidak ada kunci atau teks dokumen yang sengaja dicatat ke log oleh fitur ini.
Pengguna tetap harus mempertimbangkan ketentuan layanan dan privasi OpenAI.

Usulan diperiksa kembali secara lokal: ID harus ada dalam kandidat terkirim,
kode aturan berlaku untuk jenjang, operasi dan target cocok dengan aturan,
fix_mode Auto, properti terbukti gagal dan cakupan teknis lokal aman. Usulan
ambigu atau tidak valid adalah `needs_review`; ID/aturan tak dikenal tidak
ditampilkan mentah. Duplikasi, respons tidak lengkap, error dan timeout tidak
menghasilkan rencana parsial yang dapat digunakan. Hasil bukan izin menjalankan
formatter. Perubahan lokal lama tetap memerlukan persetujuan/cakupan yang sudah ada.

## Cakupan dan evaluasi

Empat aturan kandidat: PPKI-LAY-005, 017, 018 dan 019. Formatter halaman dan
heading lama tidak menjadi operasi AI tahap ini. Aturan lainnya belum otomatis
didukung; metadata JSON tidak membuktikan handler tersedia.

| Dokumen | Kandidat teks isi lokal | Kandidat maksimum dikirim dalam satu permintaan | Kandidat belum dikirim | Paragraf perubahan potensial classifier lama |
| --- | ---: | ---: | ---: | ---: |
| Dummy Master | 25 | 25 | 0 | 0 |
| Tesis privat (S2) | 198 | 30 | 168 | 0 |

Pengukuran dilakukan lokal tanpa mengirim dokumen ke API; hash file sebelum
dan sesudah sama. Angka di atas bukan jumlah hasil AI. Belum ada panggilan AI
nyata, sehingga jumlah usulan yang lolos, akurasi dan perbandingan kinerja
terhadap classifier lama masih PENDING. Hanya tes dengan respons mock yang
memastikan alur validasi dan UI bekerja. Tidak ada data atau kutipan tesis dalam
laporan ini.

## Pengujian

- Baseline: 153 passed.
- Regresi: `python -m pytest -q` — 171 passed, termasuk Streamlit AppTest dan
  tes respons valid, ambigu, tidak valid, timeout, error, serta input tanpa izin.
- SDK dan impor validasi DOCX berhasil; health endpoint Streamlit: `ok`.
- File yang berubah: `core/ai_planner.py`, `app.py`, `requirements.txt`,
  `tests/test_ai_planner.py`, README dan laporan/task terkait.

## Keterbatasan dan langkah berikut

Respons AI belum dievaluasi menggunakan akun/model nyata. Kandidat melebihi
batas satu permintaan tidak dianalisis; pemilihan berdasarkan urutan dokumen
bukan sampel representatif. AI tidak mengatasi semua konteks ambigu: persyaratan
lokal yang konservatif tetap berlaku. Font kompleks, field, tabel, gambar,
footnote dan elemen khusus tidak diberikan izin format. Tidak ada output DOCX
atau CSV dari pratinjau AI. Pemeriksaan Word dan acceptance penggunaan nyata
masih tertunda. Sebelum tahap penerapan, lakukan evaluasi respons API nyata
dengan persetujuan dan ground truth, tinjau false positive, lalu rancang tes
integritas dan persetujuan eksplisit; jangan langsung mempercayai hasil AI.
