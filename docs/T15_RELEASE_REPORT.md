# T15 — MVP v1.0 Release Candidate

**Status: RELEASE CANDIDATE.** Pengujian teknis lulus, tetapi acceptance untuk
dokumen akademik nyata anonim dan pemeriksaan visual akhir Microsoft Word masih
**PENDING**. Status ini bukan READY atau izin menggunakan dokumen pelanggan.

## Verifikasi

| Pemeriksaan | Hasil |
| --- | --- |
| Seluruh pytest termasuk Streamlit AppTest | 132 passed, 0 failed |
| Empat fixture dan alur audit, perbaikan, audit ulang, unduh | PASS teknis dalam tes T13 |
| Dummy Master mode umum | 9 perubahan divalidasi; 118 temuan dilewati, termasuk landscape |
| Heading saja Dummy Master | 3 perubahan BAB II, audit ulang pass, section tetap utuh |
| Keamanan upload dan state T14 | Tes negatif dan AppTest lulus |
| Streamlit lokal | Server dimulai pada localhost; health endpoint menjawab `ok` |
| Dokumen nyata anonim | PENDING, ditunda oleh pengguna |
| Pemeriksaan visual akhir Microsoft Word | PENDING |

Perintah regresi: `.\.venv\Scripts\python.exe -m pytest -q`. Tes unduhan
mengonfirmasi tombol dan bytes hasil dalam AppTest, bukan unduhan manual browser.
S3 dan Master menyisakan fail untuk section landscape yang sengaja dilewati;
ini tidak berarti perubahan section lain gagal. Rincian di [T13](T13_REPORT.md).

## Kesiapan dan repository

[Kemampuan](MVP_CAPABILITIES.md) mengidentifikasi 12 validator dan 12 handler
Auto dari 317 aturan, dengan batasan konteks dan safety; 305 aturan tidak punya
validator kepatuhan aktif. [Panduan](USER_GUIDE.md) menjelaskan instalasi,
konfigurasi batas, alur dan error. [Keterbatasan](KNOWN_LIMITATIONS.md) mencatat
risiko. Environment diuji memakai Python 3.14.5; requirements memakai batas
minimum dan belum dikunci. Aturan JSON, formatter dan dependensi tidak berubah.

Pemeriksaan nama file Git tidak menemukan file rahasia atau hasil formatter yang
terlacak; ini bukan pemindaian isi atau seluruh histori Git. Fixture DOCX yang
terlacak adalah data sintetis. `.gitignore` mengabaikan environment, cache,
secrets Streamlit, `.env` dan nama hasil standar; DOCX pribadi bernama lain
tidak otomatis diabaikan, jadi jangan menaruhnya di repository. Tidak ada commit,
tag atau push yang dibuat selama T15.

## Langkah sebelum penggunaan nyata

Selesaikan acceptance pada salinan dokumen akademik anonim, dan isi
[checklist pemeriksaan Word](T13_WORD_CHECKLIST.md) untuk seluruh hasil,
termasuk review halaman 4 S2. Tinjau temuan yang dilewati dan selesaikan masalah
yang terungkap sebelum mempertimbangkan status siap digunakan.

File berubah: [README.md](../README.md), [.gitignore](../.gitignore),
[TASKS.md](TASKS.md), [MVP_CAPABILITIES.md](MVP_CAPABILITIES.md),
[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md), [USER_GUIDE.md](USER_GUIDE.md),
dan laporan ini.
