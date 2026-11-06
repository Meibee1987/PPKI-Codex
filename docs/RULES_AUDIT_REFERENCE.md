# Audit struktur aturan PPKI (ekspor Supabase)
- Total rules: **317** (unique codes: 317)
- Ditandai `is_implemented=true`: **25**, belum ditandai: **292**
- Catatan: flag `is_implemented` tidak membuktikan bahwa kode validator/formatter sudah ada atau lulus pengujian.

## Per domain

| Domain | Total | Flag implemented |
|---|---:|---:|
| ABS | 19 | 6 |
| CIT | 20 | 0 |
| CNT | 42 | 0 |
| CVR | 16 | 0 |
| FIG | 32 | 0 |
| HDG | 18 | 10 |
| LAN | 28 | 0 |
| LAY | 26 | 9 |
| NUM | 25 | 0 |
| REF | 32 | 0 |
| STR | 25 | 0 |
| TBL | 34 | 0 |

## Per mode perbaikan

| Mode | Total | Flag implemented |
|---|---:|---:|
| Auto | 145 | 21 |
| Confirm | 88 | 4 |
| Manual | 84 | 0 |

## Rekomendasi teknis

- Gunakan `rule_code` sebagai kode stabil dalam laporan dan `validation_key` sebagai identitas validator/transformer di kode.
- Sebagian besar `expected_value_pattern` adalah teks natural, bukan konfigurasi mesin. Jangan menerapkannya langsung dengan AI; petakan ke parameter terstruktur dan uji.
- `applies_to` memuat nilai teks bebas (misalnya `Semua`, `Skripsi`, `Tesis/Disertasi`, dan konteks khusus). Buat resolver cakupan dengan pemetaan eksplisit, jangan hanya periksa substring.
- `fix_mode=Auto` bukan bukti bahwa formatter sudah ada. Tidak semua rule yang layak diaudit aman untuk diperbaiki otomatis.
- Untuk penggunaan pribadi, mulai dari JSON lokal (snapshot) dan simpan Supabase sebagai sumber utama. Tambahkan sinkronisasi hanya jika diperlukan.
- Jangan mengubah tubuh teks ilmiah, referensi, field, tabel, gambar atau layout kompleks tanpa analisis dan konfirmasi.
- Validasi ulang hasil DOCX dan simpan original, output, serta laporan perubahan.

## Rule aktif (berdasarkan flag, belum diverifikasi secara fungsional)

- `PPKI-ABS-001` — `abstract.skripsi-language-pair` — Bahasa
- `PPKI-ABS-003` — `abstract.skripsi-narrative-paragraph-count-one` — Jumlah paragraf
- `PPKI-ABS-004` — `abstract.skripsi-word-count-max-200` — Jumlah kata
- `PPKI-ABS-011` — `abstract.skripsi-single-spacing-zero-paragraph-spacing` — Spasi dan paragraph spacing
- `PPKI-ABS-013` — `summary.thesis-dissertation-language-pair` — Bahasa
- `PPKI-ABS-019` — `abstract-summary-single-spacing-zero-paragraph-spacing` — Paragraph spacing
- `PPKI-HDG-001` — `heading.chapter-number-upper-roman-no-period` — Nomor bab
- `PPKI-HDG-002` — `heading.maximum-depth-3` — Tingkat pengebaban
- `PPKI-HDG-003` — `heading.chapter-uppercase` — Kapitalisasi judul bab
- `PPKI-HDG-004` — `heading.chapter-bold` — Tebal judul bab
- `PPKI-HDG-005` — `heading.chapter-no-period-no-underline` — Tanda akhir judul bab
- `PPKI-HDG-006` — `heading.chapter-centered` — Perataan judul bab
- `PPKI-HDG-007` — `heading.subheading-decimal-left` — Nomor subbab
- `PPKI-HDG-009` — `heading.subheading-bold-no-period-no-underline` — Tebal dan dekorasi subbab
- `PPKI-HDG-011` — `heading.subsubheading-decimal-left` — Nomor sub-subbab
- `PPKI-HDG-013` — `heading.subsubheading-regular-no-period-no-underline` — Gaya sub-subbab
- `PPKI-LAY-003` — `section.page-size-a4` — Ukuran halaman
- `PPKI-LAY-005` — `body.font-times-new-roman-12` — Fon teks utama
- `PPKI-LAY-008` — `section.margin-left-4cm` — Margin kiri
- `PPKI-LAY-009` — `section.margin-right-3cm` — Margin kanan
- `PPKI-LAY-010` — `section.margin-top-3cm` — Margin atas
- `PPKI-LAY-011` — `section.margin-bottom-3cm` — Margin bawah
- `PPKI-LAY-017` — `body.line-spacing-single` — Jarak baris utama
- `PPKI-LAY-018` — `body.first-line-indent-1cm` — Indentasi baris pertama
- `PPKI-LAY-019` — `body.justified` — Perataan paragraf
