# PRD — PPKI Academic Formatter (Personal MVP)

**Versi:** v0.1 / spesifikasi MVP  
**Pemilik produk:** penyedia jasa formatter tunggal  
**Volume:** 20–30 skripsi/tesis/disertasi per bulan  
**Platform:** aplikasi lokal yang diakses lewat browser (Streamlit)

## 1. Masalah
Memformat dokumen akademik di Microsoft Word berulang kali membutuhkan waktu, rawan ketidakkonsistenan, dan harus mengikuti aturan pedoman PPKI. Pengguna ingin mengaudit dan memperbaiki bagian format yang aman, sambil menjaga konten dokumen tidak berubah.

## 2. Tujuan
- Mempercepat audit format dasar pada DOCX.
- Menghasilkan **DOCX salinan** yang sesuai subset aturan PPKI yang benar-benar telah didukung oleh kode.
- Memberi laporan transparan: mana yang **lulus / salah / diperbaiki / perlu review / belum didukung**.
- Bisa dipakai tanpa kredit API AI, hosting, dan layanan cloud.

## 3. Pengguna dan skenario
**Satu operator**, bukan sistem multi-tenant. Operator menerima file DOCX pelanggan, membuka aplikasi di laptop, memilih jenis karya ilmiah, melakukan audit, menerapkan perubahan yang aman, meninjau hasil di Microsoft Word, lalu menyerahkan file ke pelanggan.

### Alur pengguna (happy path)
1. Buka aplikasi lokal dan pilih dokumen `.docx`.
2. Pilih jenis dokumen: **Skripsi (S1)** / **Tesis (S2)** / **Disertasi (S3)**.
3. Aplikasi memuat snapshot `rules/ppki_rules_all.json`.
4. Klik **Audit** dan lihat temuan beserta `rule_code`, nilai aktual, aturan dan tingkat keparahan.
5. Klik **Terapkan perbaikan aman** (hanya handler yang sudah diimplementasikan dan tidak ambigu).
6. Download **DOCX baru** + **report JSON/CSV**. File asli tidak diubah.
7. Operator melakukan pemeriksaan akhir visual di Microsoft Word.

## 4. Ruang lingkup MVP

### P0 — harus ada
| ID | Kemampuan | Kriteria terima singkat |
|---|---|---|
| FR-01 | Upload dan validasi `.docx` | Menolak file bukan DOCX, file rusak, dan file terlalu besar (batas awal 20 MB, dapat dikonfigurasi). |
| FR-02 | Pilih jenis dokumen | S1, S2, S3 tersedia; filter `applies_to` bersifat eksplisit. |
| FR-03 | Baca rules lokal | Memuat JSON, memeriksa kolom wajib, melaporkan duplikasi `rule_code`. |
| FR-04 | Audit format | Menampilkan temuan untuk aturan yang memiliki validator; rules yang belum didukung ditampilkan sebagai `not_supported`, tidak sebagai `pass`. |
| FR-05 | Terapkan format aman | Hanya handler yang didukung; jika tidak aman/ambigu, tidak mengubah dan mencatat alasannya. |
| FR-06 | File hasil dan laporan | Unduh DOCX dengan nama baru dan laporan per aturan; file asli tetap utuh. |
| FR-07 | Perlindungan isi | Teks, tabel, gambar, relasi referensi, dan elemen kompleks tidak dihilangkan/ditulis ulang oleh aplikasi. |

### 9 aturan kandidat pertama (subset sederhana)
> Implementasi dilakukan satu per satu; status `is_implemented` dari database **tidak otomatis** menjadikan handler siap produksi.

| `rule_code` | Target dari ekspor Supabase |
|---|---|
| PPKI-LAY-003 | Ukuran kertas A4 (21 × 29,7 cm) |
| PPKI-LAY-005 | Font teks utama Times New Roman, 12 pt |
| PPKI-LAY-008 | Margin kiri 4 cm |
| PPKI-LAY-009 | Margin kanan 3 cm |
| PPKI-LAY-010 | Margin atas 3 cm |
| PPKI-LAY-011 | Margin bawah 3 cm |
| PPKI-LAY-017 | Spasi baris isi 1,0 |
| PPKI-LAY-018 | Indentasi baris pertama 1 cm |
| PPKI-LAY-019 | Paragraf utama justified |

**Catatan penerapan:** `LAY-005`, `LAY-017`, `LAY-018`, `LAY-019` hanya boleh diterapkan pada paragraf yang dikenali dengan keyakinan tinggi sebagai **teks isi utama**. Jangan paksa pada judul, abstrak, kutipan khusus, caption, isi tabel, daftar pustaka, field, atau paragraf yang tidak jelas.

### P1 — setelah P0 stabil
- Kenali heading dan abstrak berbasis style/pola sederhana, dengan pilihan **konfirmasi** jika ambigu.
- Tambah handler dari 25 rules yang ditandai `is_implemented=true` **setelah** lolos tes.
- Tampilkan ringkasan audit per domain dan preview temuan sebelum memperbaiki.

## 5. Di luar cakupan MVP
- API AI otomatis, framework agent atau pengiriman berkas ke cloud.
- Login, akun pelanggan, pembayaran, multi-user, dashboard admin.
- Hosting/VPS, sinkronisasi real-time Supabase, migrasi database.
- Perbaikan otomatis daftar isi/field Word, halaman Romawi-Arab, daftar referensi, bibliografi, caption, tabel kompleks, gambar, persamaan.
- Deteksi plagiarisme, penulisan ulang isi, proofreading akademik.
- Format PDF atau `.doc` sebagai input/output utama.

## 6. Prinsip rule engine
- Supabase `public.rules` = sumber master, **JSON hasil ekspor** = snapshot runtime v0.1.
- Identitas stabil laporan = `rule_code`. Kunci pemetaan handler = `validation_key`.
- `expected_value_pattern` dan `official_requirement` adalah teks pedoman; **jangan disulap otomatis menjadi perintah pemformatan** tanpa mapping yang ditulis dan diuji.
- `fix_mode`:
  - `Auto`: bisa diperbaiki **jika** handler tersedia dan struktur aman.
  - `Confirm`: tunggu persetujuan eksplisit.
  - `Manual`: laporkan saja.
- Status temuan: `pass`, `fail`, `fixed`, `needs_review`, `not_supported`, `error`.
- Untuk konteks `applies_to` spesifik yang tidak dikenali, jangan klaim berlaku untuk semua.

## 7. Kriteria penerimaan keseluruhan
- [ ] Aplikasi dapat membuka DOCX sederhana dan menunjukkan audit 9 kandidat aturan.
- [ ] Semua perbaikan yang **diklaim berhasil** dibuktikan oleh audit ulang pada file output.
- [ ] Input dan output dapat dibuka di Microsoft Word.
- [ ] Berkas input tidak pernah tertimpa.
- [ ] Tidak ada perubahan pada teks ilmiah (dibandingkan sebelum/sesudah dengan tes ekstraksi teks), konten tabel, serta jumlah gambar/relasi dasar pada fixtures.
- [ ] File ambigu/kompleks tidak dipaksa berubah; alasan skip muncul di laporan.
- [ ] Pengujian otomatis minimal untuk setiap handler yang diaktifkan; uji manual pada ≥5 DOCX dengan variasi heading, tabel, gambar, section.
- [ ] Aplikasi bisa bekerja saat internet mati.

## 8. Risiko dan mitigasi
- **Gaya Word bercampur:** hanya format paragraf dengan klasifikasi pasti; selain itu laporkan.
- **Section berbeda:** audit setiap section; jangan samakan otomatis bila ada tujuan khusus yang belum dipahami.
- **Run / hyperlink / field:** jangan gunakan `paragraph.text = ...`; perlakukan sebagai elemen yang harus dipertahankan.
- **Rules pedoman ambigu:** jangan mengarang angka/format; sumber tetap ekspor Supabase.
- **Kualitas render:** output wajib ditinjau manusia di Microsoft Word sebelum dikirim.

## 9. Selesai untuk MVP berarti
Operator bisa memproses satu DOCX pada laptop dari upload sampai unduh file hasil, menangani subset rule yang jelas dengan aman, serta menerima laporan yang dapat ditelusuri ke `rule_code` PPKI.
