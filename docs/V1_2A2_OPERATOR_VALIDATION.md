# v1.2A.2 — Review operator privat

## Status

Antarmuka dan evaluasi tersedia sebagai **dry-run lokal**. Pada saat laporan
dibuat, 40 sampel belum memiliki label jenis operator dan semua 160 penilaian
aturan masih PENDING. Tidak ada akurasi, false positive atau false negative
empiris yang dapat dilaporkan sebelum label diberikan. Tidak ada classifier
yang diubah berdasarkan sampel dan formatter otomatis baru tidak diaktifkan.

## Cara menjalankan panel

Di PowerShell dari direktori proyek, gunakan flag opt-in dan ikat server ke
localhost. Panel tidak ditampilkan bila flag tidak ada dan ditolak bila alamat
server bukan `localhost`, `127.0.0.1` atau `::1`.

```powershell
$env:PPKI_LOCAL_REVIEW = "1"
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address localhost --browser.gatherUsageStats false
```

Buka aplikasi lokal lalu bagian **Review privat sampel operator** dan centang
**Buka 40 sampel privat**. Pilih lokasi. Teks paragraf dan konteks tetangganya
ditampilkan di layar untuk penilaian lokal; tabel menampilkan prediksi dan
alasan serta keempat aturan PPKI. Pilih jenis dan, untuk masing-masing aturan,
aman, tidak aman, belum yakin, atau biarkan PENDING. Klik **Simpan label lokal**.
Tidak ada pilihan yang otomatis mengambil prediksi sebagai label. Tidak perlu
mengunggah dokumen ke form audit untuk memakai panel ini.

Panel membaca `private_tests/tesis_uji.docx`, daftar sampel dan metadata hash
yang sudah disiapkan. Label disimpan terpisah pada
`private_tests/scope_operator_labels.csv`, dengan hash dan lokasi; teks dan
catatan bebas tidak disimpan. File sampel dan DOCX asli tidak ditulis. Folder
privat diabaikan Git; `.gitignore` tidak menghapus file yang telanjur terlacak.
Jika dokumen atau daftar lokasi berubah, atau file label berisi hash lain,
duplikat atau nilai tidak dikenal, proses ditolak. Untuk berhenti gunakan
Ctrl+C; hapus flag pada sesi PowerShell dengan
`Remove-Item Env:PPKI_LOCAL_REVIEW` bila tidak diperlukan lagi.

## Interpretasi evaluasi

Hanya label eksplisit untuk enam jenis yang dapat dibandingkan. Label kosong,
`lainnya` dan `belum_yakin` dihitung PENDING/ambigu, bukan negatif. Tabel
klasifikasi menyajikan TP, FP, FN; prediksi classifier yang tidak pasti dihitung
di FN dan juga ditampilkan tersendiri. Precision/recall hanya dihitung bila
ada minimal lima label positif dan lima label kategori lain. Ambang ini sekadar
syarat minimum tampilan, bukan bukti sampel memadai secara statistik; hasil
hanya berlaku untuk bagian sampel yang dilabeli.

Tabel keamanan per aturan membandingkan jawaban tegas operator dengan
`safe_to_apply` kandidat. `protected` dihitung sebagai dilindungi, sedangkan
`needs_review` adalah abstain, bukan otomatis prediksi tidak aman. Jawaban
kosong atau belum yakin tidak menghasilkan izin atau perbandingan aman/tidak
aman. Label sampel tidak diteruskan ke formatter atau digeneralisasi ke dokumen
lain. Pemeriksaan Word dan dokumen nyata untuk hasil formatting tetap PENDING.

## Pengujian dan file

Regresi `.\.venv\Scripts\python.exe -m pytest -q`: **153 passed**, termasuk
Streamlit AppTest untuk opt-in, pembatasan localhost, menyimpan label sintetis,
dan pengujian file berubah, label asing, sampel berubah, label kosong/belum
yakin, serta integritas DOCX. Pengujian sintetis tidak menulis label pada tesis
pribadi; status 40/160 PENDING diperiksa sebelum laporan dibuat.
AppTest terpisah membuka panel dengan tesis lokal dan menemukan 40 lokasi;
hash DOCX dan keberadaan file label tidak berubah selama pemeriksaan tersebut.

File berubah: [operator_review.py](../core/operator_review.py), [app.py](../app.py),
[test_operator_review.py](../tests/test_operator_review.py), [README.md](../README.md),
[TASKS.md](TASKS.md), dan laporan ini. File privat tetap diabaikan Git.

## Kesiapan selanjutnya

Pelabelan operator dan perbandingan hasil masih harus dilakukan. Bahkan setelah
40 sampel berlabel, keselamatan tidak bisa digeneralisasi ke seluruh dokumen;
uji integritas dan render Word serta evaluasi dokumen anonim tambahan diperlukan
sebelum mempertimbangkan formatter otomatis v1.2B.
