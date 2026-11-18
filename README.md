# Hubungan Kualitas Pakan (Kandungan Protein) dengan Pertambahan Bobot Badan Kambing PE

Bahan pendukung artikel **"Analisis Hubungan antara Kualitas Pakan (Kandungan Protein) dengan Pertambahan Bobot Badan Menggunakan Korelasi dan Regresi"** (Jurnal Pustaka Data).

Penulis: Moh. Azka Fariqi, Hasmi, Muhammad Ainul Yaqin, Program Studi Teknik Informatika, UIN Maulana Malik Ibrahim Malang.

## Ringkasan

Data dalam repositori ini adalah **data sintetis** hasil simulasi berbasis agen di Microsoft Excel, bukan hasil pengamatan ternak. Setiap kambing diperlakukan sebagai agen dengan atribut sendiri (umur awal, bobot awal, target konsumsi bahan kering, dan gangguan acak individu). Kandang pada setiap periode berperan sebagai lingkungan yang menyediakan ransum dan gangguan acak kandang.

- 216 kambing Peranakan Etawah (PE) jantan sintetis: 72 ekor per fase (Starter, Grower, Finisher)
- Setiap fase: 12 kandang × 2 periode × 3 kambing
- Satu kali pembangkitan penuh memanggil `RAND()` sebanyak 1.296 kali
- Dataset utama adalah satu realisasi yang dibekukan sebagai nilai tetap

## Isi repositori

| Folder / file | Isi |
|---|---|
| `data/DATASET-FINAL.xlsx` | Buku kerja pembangkitan. Lembar `Parameter`, `Ransum`, `Pemberian_Pakan`, `Individu`, dan lembar fase berisi rumus `RAND()` yang masih aktif. Lembar `Latih_Individu_*` dan `Uji_Individu_*` berisi dataset utama yang sudah dibekukan dan dipakai pada artikel (gabungan keduanya = 72 kambing per fase). |
| `hasil/Analisis_Seluruh_Kambing_-_Lima_Model.xlsx` | Hasil regresi lima model (M1–M5) pada seluruh 72 kambing per fase. |
| `kode/uji_kestabilan_50.py` | Skrip Python yang menjalankan ulang rumus pembangkitan sebanyak 50 replikasi (benih acak 2026) dan membentuk M1 serta M4 pada setiap replikasi. |
| `hasil/Uji_Kestabilan_50_Pembangkitan.xlsx` | Keluaran skrip: 50 dataset lengkap (`Rep01`–`Rep50`), ringkasan regresi per replikasi, dan statistik ringkas. Setiap lembar `Rep` memuat rumus `LINEST` Excel untuk memeriksa hasil Python. |

**Catatan:** buku kerja `DATASET-FINAL.xlsx` masih berisi rumus `RAND()` aktif. Membuka dan menghitung ulangnya (misalnya menekan F9) akan menghasilkan undian baru pada lembar berumus, tetapi **tidak** mengubah dataset utama di lembar `Latih_Individu_*` dan `Uji_Individu_*`.

## Model regresi

| Model | Variabel bebas | Variabel terikat |
|---|---|---|
| M1 | PK | ADG |
| M2 | PK, (PK − 14)² | ADG |
| M3 | PK, TDN | ADG |
| M4 | PK, TDN, DMI (regresi linear berganda) | ADG |
| M5 | Seleksi bertahap dari PK, TDN, DMI | ADG |

Keterangan: PK = protein kasar ransum (% BK), TDN = total nutrien tercerna (% BK), DMI = konsumsi bahan kering (kg BK/hari), ADG = pertambahan bobot badan harian (kg/hari), BK = bahan kering.

## Menjalankan uji kestabilan

Kebutuhan: Python 3.9+ dengan `numpy`, `pandas`, dan `scipy`.

```bash
pip install numpy pandas scipy
python kode/uji_kestabilan_50.py
```

Skrip memakai benih acak 2026, sehingga setiap kali dijalankan akan menghasilkan 50 replikasi yang sama persis. Urutan pengundian di Python berbeda dari Excel, jadi replikasi ini memakai rumus dan parameter yang sama dengan buku kerja, tetapi bukan salinan hasil perhitungan ulang di Excel.

## Lisensi

Data dan kode dapat digunakan untuk keperluan pendidikan dan penelitian dengan menyebutkan artikel di atas.
