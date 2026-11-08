# Kemampuan MVP v1.0 Release Candidate

Snapshot memuat 317 aturan. Berdasarkan mapping yang ada di kode dan snapshot
saat ini, **12 aturan memiliki validator aktif**, semuanya `fix_mode=Auto` dan
`applies_to=Semua`. Sebanyak **305 aturan lainnya belum memiliki validator
kepatuhan aktif**. Pada audit, aturan yang konteks penerapannya belum dipetakan
dapat tampil `needs_review`; metadata `is_implemented` tidak menunjukkan
bahwa validator tersedia.

| Rule | Pemeriksaan dan perbaikan yang tersedia |
| --- | --- |
| PPKI-LAY-003 | A4 per section aman |
| PPKI-LAY-008, 009, 010, 011 | Margin kiri, kanan, atas dan bawah per section aman |
| PPKI-LAY-005 | Nama dan ukuran font pada teks isi yang aman dan dikonfirmasi |
| PPKI-LAY-017, 018, 019 | Spasi baris, indentasi baris pertama dan alignment teks isi yang aman dan dikonfirmasi |
| PPKI-HDG-003, 004, 006 | Kapitalisasi judul BAB, bold dan alignment kandidat BAB yang dikonfirmasi dan aman |

Kedua belas aturan tersebut memiliki handler perbaikan Auto, tetapi perubahan
hanya direncanakan untuk temuan `fail` yang aman dan berlaku. Operator harus
memilih tindakan sebelum perubahan, mengonfirmasi cakupan style teks isi dan
setiap kandidat BAB yang hendak diperiksa. Kapitalisasi BAB memang mengubah
huruf judul yang ditargetkan; teks penelitian lainnya tidak dimaksudkan berubah.
Section landscape, berkolom atau ambigu dilewati. Aturan `Confirm` dan `Manual`
tidak memiliki perbaikan otomatis dalam cakupan ini; konfirmasi cakupan bukan
implementasi fix_mode Confirm.

Diagnostik read-only tersedia untuk struktur nomor halaman dan field PAGE,
tabel/gambar/caption, kandidat sitasi/referensi, serta kandidat bagian dokumen.
Diagnostik tersebut bukan validator kepatuhan aturan terkait dan dapat
membutuhkan review. Tidak ada formatter nomor halaman, tabel, gambar, caption,
sitasi, daftar pustaka, struktur dokumen, atau heading subbab.
