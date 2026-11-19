# Integrasi keputusan AI dan validator lokal — dry-run

## Hambatan dan perubahan

Sebelumnya satu penanda `safe_to_apply` menggabungkan kepastian identitas teks
isi dengan pemeriksaan format. Akibatnya keputusan AI tidak dapat dipakai sebagai
bukti tambahan meskipun nilai format dan struktur paragraf dapat diperiksa.

Pratinjau sekarang memisahkan bukti identitas dari hasil pemeriksaan format per
aturan. AI harus menyatakan teks isi dan konteks isi; Python tetap mensyaratkan
BAB yang terdeteksi, style Normal, paragraf teks biasa dengan karakteristik
sederhana, struktur OOXML aman, validator yang tersedia, nilai yang diketahui,
ketidaksesuaian terbukti, target JSON yang tepat, serta `fix_mode=Auto`. Bukti
AI tidak mengubah `safe_to_apply` classifier lama dan tidak memberikan izin
formatter. Pratinjau AI hanya menerima dokumen satu section yang lolos pemeriksaan
orientasi dan kolom; dokumen multi-section tetap review. Hasilnya hanya
`kandidat_pratinjau`; bagian ambigu tetap review.

Pemeriksaan properti paragraf pratinjau juga membaca `docDefaults` yang eksplisit
ketika direct formatting dan rantai style tidak memberikan nilai. Prioritas direct
formatting dan style dipertahankan. Nilai parsial atau tidak valid tetap tidak
diketahui. Audit dan formatter lama tidak menggunakan opsi default baru. Pembacaan
font tetap konservatif: theme, simbol, teks non-ASCII, dan default font yang belum
dapat dipastikan tetap perlu review.

Antarmuka membedakan jumlah kandidat pratinjau, yang sudah sesuai, dan yang
memerlukan review; setiap penolakan tetap memiliki alasan. Aturan Confirm dan
Manual tidak diperlakukan sebagai Auto.

## Evaluasi mock dan keamanan

Pada skenario sintetis berisi lima usulan mock: satu diterima sebagai kandidat
pratinjau, satu sudah sesuai dan tidak perlu perubahan, tiga memerlukan review
(sampul, caption, dan field tidak termasuk cakupan yang dikirim). Tes tambahan
menguji properti tak diketahui, pewarisan style, default dokumen, AI ragu,
aturan non-Auto, serta BAB yang belum pasti. Tidak ada DOCX yang diformat.

Untuk evaluasi lokal tesis privat S2, 30 kandidat pertama menghasilkan 60 usulan
mock hipotetis untuk LAY-005 dan LAY-017: **0 kandidat pratinjau, 0 sudah sesuai,
60 needs_review**. Konteks BAB kandidat tersebut belum cukup pasti untuk bukti
lokal yang baru. Ini bukan hasil model dan bukan pengukuran akurasi tesis.
Hash file tidak berubah; tidak ada teks atau respons privat disimpan dalam laporan.
Tidak ada API yang dipanggil untuk evaluasi ini.

Regresi: `python -m pytest -q` — **187 passed**, termasuk Streamlit AppTest.
File yang diperbarui untuk tahap ini: `core/ai_planner.py`, `core/structure.py`,
`core/audit.py`, `app.py`, dan `tests/test_ai_planner.py`, ditambah laporan ini.

## Batas dan langkah berikut

Bukti lokal dan klasifikasi AI masih dapat salah mengidentifikasi paragraf khusus
di dalam BAB; tes sintetis bukan validasi akurasi dokumen nyata. Hasil tetap
memerlukan pemeriksaan manusia dan belum aman sebagai izin format otomatis.
Kandidat pada bagian dengan batas BAB ambigu, objek kompleks, field, tabel,
caption, daftar dan style khusus tetap dilindungi atau memerlukan review.
Sebelum mengaktifkan formatter, lakukan evaluasi terhadap acuan operator dan
pemeriksaan integritas serta visual hasil. Pengujian API nyata berikutnya dapat
diusulkan dengan persetujuan eksplisit, tetapi belum dilaksanakan pada tahap ini.
