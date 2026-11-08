# T10A — Diagnostik sitasi dan daftar pustaka

## Inventaris aturan

Pencarian pada domain CIT/REF dan kata sitasi, kutipan, daftar pustaka,
perujukan, pengutipan, mengutip, rujukan dan referensi pada element atau
official_requirement menemukan 65 aturan: CIT 20, REF 32, CNT 4, FIG 3,
ABS 2, LAN 1, LAY 1, STR 1 dan TBL 1. Selain CIT dan REF, kode terkait adalah
ABS-007, ABS-017, CNT-001, CNT-003, CNT-018, CNT-032, FIG-028, FIG-029,
FIG-032, LAN-004, LAY-022, STR-005 dan TBL-029 (semuanya berawalan `PPKI-`).
Semua memakai `manual.not-implemented`: **0 validator kepatuhan didukung**.
Metadata fix_mode terdiri atas 33 Auto, 23 Confirm dan 9 Manual; metadata ini
tidak membuat validator atau formatter tersedia. Severity: 35 Error, 24 Warning,
6 Info. Sebanyak 41 berlaku untuk Semua; label konteks lainnya bervariasi dan
sebagian belum terpetakan. Ketentuan, nilai target dan metadata lengkap tetap
berasal dari JSON sumber dan dapat dilihat dalam audit aturan aplikasi.
Audit umum dapat menampilkan `needs_review` ketika konteks penerapan belum
dipetakan; itu tidak berarti validator aturan tersebut tersedia.

## Hasil Dummy Master

| Pemeriksaan diagnostik | Hasil |
| --- | --- |
| Kandidat sitasi | 5 |
| Kandidat referensi | 4 |
| Kandidat sitasi mungkin cocok | 4: Rahman 2021 dan Putri/Sari 2022, masing-masing dua kemunculan |
| Kandidat sitasi tanpa kandidat referensi yang dapat dipastikan | 0 |
| Kandidat referensi tanpa kandidat sitasi | 2: Halim 2020 dan Wulandari 2019 |
| Perlu review | 1: Nugraha 2023 pada paragraf 102 berada di rentang daftar pustaka |

Kecocokan hanya membandingkan nama dan tahun yang dapat diekstraksi dengan pola
sederhana. Tidak ditemukan pasangan bukan bukti tidak ada sitasi atau referensi;
Nugraha tidak dinyatakan pasti hilang karena konteks paragrafnya ambigu.

## Pengujian dan perubahan

`.\.venv\Scripts\python.exe -m pytest -q`: **110 passed**,
termasuk Streamlit AppTest dan regresi fitur terdahulu. Fixture sintetis dalam
memori menguji sitasi naratif, dalam kurung, dua penulis, beberapa sitasi,
pasangan tidak ditemukan, tanggal/tahun biasa dan entri lanjutan ambigu.
Dummy Master diuji berulang dan byte sumber tetap identik.

File berubah: [audit.py](../core/audit.py), [app.py](../app.py),
[test_citation_diagnostics.py](../tests/test_citation_diagnostics.py),
[README.md](../README.md), [TASKS.md](TASKS.md), dan laporan ini.

## Keterbatasan

Hanya heading dengan teks DAFTAR PUSTAKA dan style Heading yang dikenali;
heading lain atau lebih dari satu heading memerlukan review. Ekstraksi terbatas
pada nama Latin sederhana, satu atau dua penulis dan pola entri penulis-inisial
diikuti tahun. Penulis lebih banyak, nama kompleks, entri multiline, field dan
hyperlink tidak dapat ditafsirkan secara menyeluruh. Tabel, catatan kaki,
header/footer dan text box tidak termasuk cakupan diagnostik. Struktur kompleks
atau teks di dalam bagian daftar pustaka yang bukan entri tetap perlu review.
Hasil tidak memverifikasi format sitasi, kelengkapan sumber, substansi akademik,
ataupun tata letak. Pemeriksaan visual Microsoft Word T5 tetap PENDING.
