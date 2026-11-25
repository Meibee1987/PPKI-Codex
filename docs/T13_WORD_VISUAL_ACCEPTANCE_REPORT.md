# T13 — Validasi Visual Microsoft Word

**Status: PARTIAL.** Fixture sebelum dan sesudah tersedia, tetapi perbandingan visual dan jumlah halaman belum terverifikasi. Tidak ada kesimpulan bahwa layout hasil aman secara visual.

## Dokumen dan operasi

Empat salinan sintetis tersedia di `private_tests/t13_word_validation/` (folder tidak masuk Git): `font_sebelum.docx`, `font_sesudah.docx`, `margin_sebelum.docx`, dan `margin_sesudah.docx`.

| Pasangan | Operasi formatter yang tercatat | Halaman sebelum / sesudah | Verifikasi visual |
|---|---|---|---|
| Font dan paragraf | Paragraf 3: LAY-005 Arial 11 menjadi TNR 12; LAY-017, 018 dan 019 memperbaiki spasi, indentasi dan perataan | PENDING / PENDING | PENDING MANUAL REVIEW |
| Margin | Section 1: LAY-008 kiri 2 ke 4 cm; LAY-009–011 kanan, atas dan bawah 2 ke 3 cm | PENDING / PENDING | PENDING MANUAL REVIEW |

Ini adalah laporan operasi dan pembacaan properti, **bukan bukti bahwa perubahan sudah diperiksa visual di Word**. Fixture font mempertahankan 6 paragraf, teks identik dan 1 tabel; fixture margin mempertahankan 3 paragraf, teks identik, 1 tabel dan 1 gambar inline. Seluruh komponen ZIP selain `word/document.xml` identik untuk masing-masing pasangan. Pengujian ini tidak menjamin tampilan gambar atau tabel.

## Percobaan Word

Word COM tidak dapat diinisialisasi di sesi ini: `0x80070520`, sesi logon tidak tersedia. Karenanya tidak ada pembukaan read-only melalui COM, hitungan halaman Word, atau PDF hasil ekspor. Tidak ada klaim bahwa pengaturan pencegahan macro/tautan berhasil diterapkan pada proses Word yang gagal dibuat.

Word terbuka lewat antarmuka dan memunculkan salinan Dummy Master berstatus **AutoRecovered**, bukan keempat fixture di atas. Salinan pemulihan tidak disimpan atau diubah. Fokus dialog pembukaan fixture tidak dapat diverifikasi secara andal, sehingga perbandingan tidak dilanjutkan. Tampilan AutoRecovered tersebut bukan bukti perbandingan sebelum/sesudah.

Tesis privat tidak dibuka pada sesi ini dan tidak dimodifikasi. Salinan hasil Beta tesis tidak ditemukan dalam `private_tests`; tidak ada panggilan API ulang. Margin tesis dengan gutter dan mirror tetap tidak diubah. LibreOffice tidak tersedia.

## Pemeriksaan operator yang masih diperlukan

1. Buka pasangan fixture sebagai **Open Read-Only** di Word; jangan menyimpan ulang sumber.
2. Catat jumlah halaman dan periksa apakah perubahan posisi teks dan pembungkusan sesuai operasi yang tercatat.
3. Periksa font/ukuran, heading, subheading, caption, tabel, gambar, header, footer dan nomor halaman. Fixture font tidak memiliki gambar; fixture margin memiliki gambar sintetis kecil, sehingga Dummy Master juga perlu diperiksa.
4. Periksa pemisahan halaman, teks terpotong atau bertumpuk, serta tabel/gambar yang bergeser. Dokumentasikan nomor halaman dan penyebab yang diduga jika ditemukan masalah.
5. Untuk tesis, gunakan salinan read-only dan periksa halaman bertabel/bergambar; jika hasil Beta asli tersedia, bandingkan dengannya tanpa mengulang API. Jangan memperbaiki margin ambigu sebelum interpretasi gutter/mirror disetujui.

Masalah visual: **belum dapat ditentukan**, bukan nihil. Pengujian otomatis terakhir dari v0.5.1 adalah **259 passed**; tidak ada kode atau tes diubah pada tahap ini, sehingga pytest tidak dijalankan ulang. Tidak ada API berbayar, perubahan rules, commit, atau push.
