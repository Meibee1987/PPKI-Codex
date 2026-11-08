# Laporan T9A — Tabel, gambar, dan caption

## Aturan yang ditemukan

Pencarian berdasarkan domain `TBL`/`FIG` serta kata caption, ilustrasi, gambar,
dan tabel pada `element` atau `official_requirement` menemukan **76 aturan**:

| Kelompok | Rule code | Jumlah |
|---|---|---:|
| Gambar | `PPKI-FIG-001`–`PPKI-FIG-032` | 32 |
| Tabel | `PPKI-TBL-001`–`PPKI-TBL-034` | 34 |
| Abstrak | `PPKI-ABS-007`, `PPKI-ABS-017` | 2 |
| Konten | `PPKI-CNT-018`, `PPKI-CNT-019`, `PPKI-CNT-034` | 3 |
| Layout dan bilangan | `PPKI-LAY-004`, `PPKI-NUM-003` | 2 |
| Referensi | `PPKI-REF-001` | 1 |
| Struktur | `PPKI-STR-022`, `PPKI-STR-023` | 2 |

Seluruh 76 aturan berkunci `manual.not-implemented`: **0 validator kepatuhan
didukung, 76 belum didukung**. Status untuk konteks `applies_to` yang belum
dipetakan tetap perlu review, bukan dianggap berlaku untuk semua. Identitas,
persyaratan resmi, pola nilai, applicability, severity, dan fix mode tetap
bersumber dari [snapshot aturan](../rules/ppki_rules_all.json), tanpa perubahan.

## Hasil Dummy Master

| Struktur | Hasil | Status |
|---|---:|---|
| Tabel body | 3 | perlu review |
| Baris tabel pertama | 69: satu header bertanda ulang dan 68 baris lain | perlu review |
| Tabel dengan sel gabungan terdeteksi | 1 | perlu review |
| Tabel di section landscape | 1 | perlu review |
| Gambar inline | 2 | perlu review |
| Kandidat caption tabel | 3 | perlu review |
| Kandidat caption gambar | 2 | perlu review |
| Objek mengambang/kompleks yang terdeteksi di body | 0 | perlu review bila ditemukan |

Kedekatan caption dan objek hanyalah dugaan, termasuk setelah dikonfirmasi
operator; belum ada aturan yang dinyatakan lulus atau gagal. Jumlah baris
header adalah properti Word yang ditandai, bukan bukti render lintas halaman.

## Verifikasi dan batasan

`python -m pytest -q`: **106 passed**, termasuk Dummy Master, objek mengambang
sintetis, paragraf biasa, audit berulang, regresi formatter lama, dan Streamlit
AppTest. Dokumen asli tidak ditulis.

Pemeriksaan hanya mencakup blok body tingkat utama; gambar dalam sel tabel,
header/footer, bentuk floating kompleks, isi grafik, hubungan caption yang
melintasi blok kosong, dan layout hasil render tidak dapat dipastikan. Gambar
inline tidak otomatis dianggap ilustrasi ilmiah. Pemeriksaan manusia di Word
masih diperlukan, termasuk hubungan caption, kelanjutan tabel, grafik, dan
section landscape. Tidak ada formatter tabel, gambar, atau caption.

File berubah: `core/audit.py`, `app.py`, `tests/test_heading_audit.py`,
`tests/test_illustration_structure.py`, `README.md`, `docs/TASKS.md`, dan laporan ini.
