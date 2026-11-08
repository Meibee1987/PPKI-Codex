# v1.2A.1 — Perbaikan evaluasi cakupan

## Penyebab v1.2A menghasilkan auto_safe = 0

Analisis dilakukan sebelum perubahan, pada Dummy Master (S1) dan tesis lokal
(S2). Angka hambatan kandidat isi berikut saling tumpang tindih:

| Hambatan lama | Master: 26 kandidat isi | Tesis: 198 kandidat isi |
| --- | ---: | ---: |
| Konteks BAB tidak dianggap kuat | 26 | 198 |
| Style bukan BodyText | 0 | 198 |
| XML bukan pPr/r dan rPr/t saja | 22 | 187 |
| Teks non-ASCII | 6 | 3 |
| Lebih pendek dari 80 karakter | 5 | 2 |

Semua BAB pada kedua dokumen berstatus needs_review; kondisi lama menuntut
detected dan judul sederhana. Konteks juga hilang setelah caption, daftar dan
paragraf khusus lain tanpa membedakan apakah bagian BAB benar-benar berakhir.
Seluruh kandidat isi tesis menggunakan Normal sehingga audit yang hanya
memeriksa BodyText tidak pernah memeriksanya. Pemeriksaan XML mencampur
proofErr (15.496 penanda pada kandidat isi tesis) dan bookmark dengan objek
berisiko. Itu menyebabkan pemeriksaan berlebih, bukan bukti seluruh paragraf
protected keliru. Tabel, bagian khusus, field dan footnote memang perlu
perlindungan.

## Perubahan

Keputusan per paragraf dan aturan kini memuat:

- `eligible`: kandidat struktur dapat diperiksa dan mapping aturan berlaku.
- `needs_change`: True bila fail, False bila pass, None jika belum diketahui.
- `technical_safe`: properti dapat diperiksa dan struktur cocok untuk analisis
  teknis, tanpa menyatakan identitas semantiknya telah dikonfirmasi.
- `safe_to_apply`: kandidat memenuhi pemeriksaan teknis, fix_mode Auto dan
  bukti identitas isi yang lebih kuat. **Tetap eksperimental, bukan izin
  menjalankan formatter.** Kondisi sudah sesuai tidak membuatnya tidak aman.

Normal dalam konteks BAB boleh diperiksa, tetapi tetap membutuhkan konfirmasi
identitas. Nilai font yang ambigu tidak menghalangi pemeriksaan indent atau
alignment. Batas 80 karakter dan ASCII tidak lagi menolak seluruh properti;
validator font tetap memakai batasannya sendiri. Penanda proofErr/bookmark
dihilangkan hanya dari deepcopy paragraf untuk memanggil validator yang ada;
original tidak disentuh atau disimpan. Caption/daftar tidak menghapus konteks
BAB, tetapi selalu dilindungi sendiri. Bagian awal/akhir, section, tabel,
field/objek, revisi, daftar dan format paragraf khusus tetap dilindungi;
struktur XML lain yang belum dikenali memerlukan review. Teks mirip heading
tidak otomatis diproses sebagai isi.

Validator dan formatter lama, aturan JSON serta mekanisme konfirmasi tidak
diubah. Kemampuan teknis pada salinan analisis tidak berarti formatter lama
sudah menerima paragraf dengan marker; aktivasi memerlukan regresi penerapan
dan integritas tersendiri.

## Sebelum dan sesudah

| Dokumen | Versi | auto_safe | needs_review | protected | eligible | needs_change | technical_safe | safe_to_apply |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Master | v1.2A | 0 | 16 | 661 | Belum dipisah | Belum dipisah | Belum dipisah | Belum dipisah |
| Master | v1.2A.1 | 0 | 42 | 635 | 24 | 2 | 24 | 0 |
| Tesis | v1.2A | 0 | 42 | 1644 | Belum dipisah | Belum dipisah | Belum dipisah | Belum dipisah |
| Tesis | v1.2A.1 | 0 | 247 | 1439 | 198 | 11 | 162 | 0 |

Kolom keputusan adalah jumlah paragraf. Kolom eligible dan berikutnya menghitung
paragraf dengan setidaknya satu aturan yang memenuhi keputusan tersebut.
Tidak ada usulan yang diotorisasi sebagai safe_to_apply pada dokumen ini;
ketidaksesuaian eligible kini terlihat meskipun identitas masih perlu review.

### Rekap alasan utama setelah perubahan

| Alasan utama paragraf | Master | Tesis |
| --- | ---: | ---: |
| Sel tabel | 565 | 790 |
| Kosong | 11 | 246 |
| Bagian khusus | 56 | 397 |
| Field/objek/revisi | 3 | 6 |
| Struktur bukan kandidat isi | 17 | 48 |
| XML lain belum dikenali | 0 | 1 |
| Teks menyerupai heading | 1 | 0 |
| Periksa keputusan aturan / identitas isi | 24 | 198 |

Untuk seluruh kandidat eligible, bukti identitas BAB masih memerlukan review;
pada tesis, Normal menambah ambiguitas style. Aturan tidak berlaku atau handler
tidak tersedia kini dilaporkan secara terpisah; tidak ada kejadian tersebut
pada empat aturan Auto yang dievaluasi dalam dua dokumen ini. Sudah sesuai
adalah hasil pemeriksaan, bukan alasan perlindungan. Nilai tidak diketahui
tetap None, bukan dianggap sesuai atau tidak perlu diubah.

### Cakupan tesis per aturan

| Aturan | Eligible | Sudah sesuai | Perlu perubahan | Belum diketahui | technical_safe | safe_to_apply |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PPKI-LAY-005 | 198 | 1 | 0 | 197 | 1 | 0 |
| PPKI-LAY-017 | 198 | 0 | 0 | 198 | 0 | 0 |
| PPKI-LAY-018 | 198 | 151 | 11 | 36 | 162 | 0 |
| PPKI-LAY-019 | 198 | 162 | 0 | 36 | 162 | 0 |

Nol perubahan font/spasi bukan bukti semuanya sesuai; kebanyakan nilai belum
dapat dipastikan oleh validator lama. Master: masing-masing 24 kandidat layak
untuk empat aturan; font menghasilkan 2 fail/15 pass/7 unknown, sedangkan tiga
properti paragraf masing-masing 1 fail/23 pass. Seluruhnya masih perlu konfirmasi
identitas. Angka merupakan diagnosis format, bukan ukuran akurasi classifier.

## Sampling dan acuan

Disiapkan CSV privat **40 sampel tanpa teks**: empat kandidat isi per BAB I–V,
lima BAB acuan, lima entri daftar isi BAB, dan sepuluh contoh bagian/objek
khusus. Metadata hash sumber dicatat hanya di folder privat. Kolom operator_role,
operator_safe_rules dan operator_notes belum diisi; suggested_type adalah hasil
mesin, bukan label operator. Sampel menghasilkan 20 eligible, 2 needs_change,
19 technical_safe, 0 safe_to_apply; 21 needs_review dan 19 protected.

Lima BAB dan entri daftar isi yang sudah dicocokkan pada v1.1A tidak menjadi
isi yang dapat diubah. Salah penolakan yang terbukti pada tahap ini adalah
penanda non-konten dianggap sebagai struktur berisiko untuk pemeriksaan;
diperbaiki lewat salinan analisis dan fixture sintetis. Tidak ada false positive
safe_to_apply yang teramati pada sampel, karena tidak ada kandidat dengan izin
tersebut. **FP/FN keselamatan dan precision/recall belum dapat diukur** sebelum
operator memberi label acuan per aturan. Jangan menyamakan 40 baris template
dengan 40 sampel yang sudah diverifikasi manusia.

## Tes dan keputusan v1.2B

Baseline **141 passed**. Regresi: `.\.venv\Scripts\python.exe -m pytest -q`
— **147 passed**, termasuk Streamlit AppTest. Tes mencakup marker non-konten,
Normal dalam BAB ambigu, properti sudah sesuai, Unicode per properti, caption
yang tidak menghapus konteks, serta XML asing/field tetap ditolak. Hash sumber
sebelum/sesudah sama; tidak ada API, dependency baru, commit atau push.

**Belum siap diaktifkan untuk formatter otomatis v1.2B.** Perbaikan memperluas
pemeriksaan tanpa mengarang izin penerapan. Lengkapi label operator pada sampel
privat, verifikasi tiap perubahan terhadap keselamatan XML dan render Word,
lalu uji pada beberapa dokumen anonim sebelum aktivasi. Konfirmasi lama dan
validasi T14 tetap berlaku.

File berubah: [structure.py](../core/structure.py), [app.py](../app.py),
[test_safe_scope.py](../tests/test_safe_scope.py), [README.md](../README.md),
[TASKS.md](TASKS.md), dan laporan ini. CSV serta hasil pengukuran lokal tetap
di private_tests yang diabaikan Git.
