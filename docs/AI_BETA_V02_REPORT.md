# AI Beta v0.2 — batching dan validasi klasifikasi

Status: **eksperimental; belum siap digunakan untuk mengubah dokumen nyata tanpa pemeriksaan operator**. Tidak ada panggilan API nyata dalam pengujian ini.

## Implementasi

Kandidat dikumpulkan untuk seluruh dokumen dan dikirim dalam batch berukuran 1–30. ID unik divalidasi sebelum dan sesudah setiap batch; konteks BAB, section, dan paragraf tetangga tetap disertakan. Status hasil adalah `body_verified`, `protected`, `uncertain`, dan `unprocessed`. Nama `body_verified` berarti AI serta pemeriksaan struktur lokal mendukung kandidat; ini bukan bukti identitas semantik atau kepatuhan PPKI. AI tidak menentukan nilai format atau menjalankan kode. Salinan diproses oleh pilot yang memeriksa aturan, section, operasi, audit ulang dan integritas DOCX.

Kutipan eksplisit dilindungi. Indentasi langsung dan kombinasi paragraf panjang dengan pola sitasi ditahan untuk review; panjang saja bukan bukti kutipan. Respons dengan ID atau schema tidak valid membatalkan hasil; timeout, rate limit, respons terpotong, atau batas anggaran menghentikan pengiriman dan meninggalkan kandidat terkait sebagai `unprocessed`. Tidak ada retry otomatis.

Anggaran berdasarkan harga input/output yang diisi operator per sejuta token. Estimasi input memakai ukuran JSON dalam byte ditambah cadangan protokol, dan output memakai batas token yang dipilih. Penggunaan aktual respons dicatat per batch bila tersedia, dan pemrosesan berhenti bila penggunaan tidak lengkap. **Ini perkiraan, bukan batas tagihan yang dijamin penyedia**: tokenisasi, metadata, respons gagal dan harga yang salah dapat menyebabkan biaya aktual berbeda. Jangan menggunakannya sebagai satu-satunya perlindungan anggaran akun.

## Hasil mock lokal

| Dokumen | Kandidat | Batch | body_verified mock | protected | uncertain | unprocessed | Perubahan | Normalisasi nilai tak diketahui |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Dummy Master | 23 | 1 | 23 | 638 | 16 | 0 | 3 | 0 |
| Tesis privat S2 | 88 | 3 | 88 | 1440 | 158 | 0 | 91 | 87 |

Kandidat tesis berkurang dari 198 karena indikasi format khusus sekarang ditahan, bukan karena 110 paragraf terbukti bukan teks isi. Mock memberi semua kandidat label `body`; angka perubahan bukan pengukuran akurasi AI dan bukan izin penggunaan pada tesis. Perubahan hanya pada salinan dalam memori; audit ulang dan validasi integritas lulus, hash file asli tetap identik. Jumlah elemen protected/uncertain juga mencakup elemen tabel. Tidak ada pemeriksaan visual Word.

Tes terpisah memproses 198 ID sintetis dalam tujuh batch tanpa pengulangan dan menjaga konteks, serta memeriksa penghentian oleh anggaran dan timeout. Evaluasi kecil berlabel memeriksa satu body, heading, caption, kutipan berindentasi dan bagian awal/akhir serta field: body contoh teridentifikasi, bagian khusus tidak menjadi body; kasus kutipan tertahan. Pada subset yang eksplisit ini: satu true positive, nol false positive, nol false negative, satu kutipan ditahan. Sampel tersebut tidak cukup untuk menggeneralisasi precision atau recall. Kutipan tanpa penanda dan tanpa bukti format masih dapat disalahklasifikasi AI.

## Keterbatasan dan langkah selanjutnya

- Pemeriksaan visual Word, ground truth tesis dan evaluasi AI nyata masih PENDING; ketepatan semantik belum dibuktikan. Satu uji API terbatas dapat dipersiapkan setelah operator menyetujui pengiriman dan memahami biaya, tetapi hasilnya tidak boleh dianggap validasi produksi.
- Penggunaan token tidak lengkap dan biaya layanan untuk request yang gagal tidak dapat dipastikan secara lokal. Anggaran adalah perkiraan konservatif, bukan jaminan pembatasan tagihan.
- Tidak semua variasi OOXML, kutipan, layout dan format khusus dapat dikenali; bagian ambigu harus ditinjau manusia.
- Tidak ada perubahan rules JSON, penyimpanan tesis ke Git, perubahan input, atau pelemahan T14. Tidak ada commit/push.

Hasil pytest akhir: `python -m pytest -q` — **236 passed**, termasuk Streamlit AppTest.
