# Proyek SLR — Pemetaan Bibliometrik & Tinjauan Pustaka Sistematis Sesar Aktif

Repositori ini berisi seluruh data, skrip, dan luaran dari tugas **Systematic Literature Review (SLR)** dan **pemetaan bibliometrik** untuk mata kuliah **Metodologi Penelitian Geografi (GeoMetPen)**, Departemen Geografi, Universitas Indonesia.

- **Penulis:** Pramono Pido (NPM 2606828056)
- **Topik:** sesar aktif / sesar tektonik / *fault slip* yang dikaji dengan GIS, penginderaan jauh, dan geomorfologi
- **Korpus:** 189 dokumen terbitan tahun 2025 dari Scopus (188 dokumen dipakai di matriks *gap*)
- **Tujuan akhir:** memetakan lanskap riset, mengidentifikasi celah penelitian (*research gap*), dan menurunkan rekomendasi judul tesis

---

## Daftar Isi

1. [Ringkasan Metodologi](#1-ringkasan-metodologi)
2. [Alur Kerja (Pipeline)](#2-alur-kerja-pipeline)
3. [Struktur Repositori](#3-struktur-repositori)
4. [Dokumentasi Skrip Python](#4-dokumentasi-skrip-python)
5. [Kamus Data](#5-kamus-data)
6. [Ringkasan Hasil](#6-ringkasan-hasil)
7. [Instalasi & Cara Menjalankan](#7-instalasi--cara-menjalankan)
8. [Perangkat Eksternal yang Digunakan](#8-perangkat-eksternal-yang-digunakan)
9. [Catatan, Keterbatasan & Masalah yang Diketahui](#9-catatan-keterbatasan--masalah-yang-diketahui)
10. [Referensi](#10-referensi)

---

## 1. Ringkasan Metodologi

### 1.1 Strategi pencarian

Pencarian dilakukan di basis data **Scopus** dengan kueri:

```
TITLE-ABS-KEY ( ( "active fault" OR "tectonic fault" OR "fault slip" )
  AND ( "GIS" OR "remote sensing" OR "geomorphology" ) )
  AND ( LIMIT-TO ( PUBYEAR , "2025" ) )
```

### 1.2 Seleksi dokumen

| Tahap | Jumlah dokumen | Keterangan |
|---|---:|---|
| Hasil pencarian awal Scopus | 197 | Tersimpan di `Ris.ris` (197 entri RIS) |
| Setelah kurasi di Zotero | 189 | Deduplikasi (DOI/judul identik), penyaringan kelengkapan metadata, validasi format ekspor. Tersimpan di `Tes ref.bib` (172 `@article`, 17 `@inproceedings`) dan ekspor Zotero `.csv`/`.xlsx` |
| Dipakai di matriks gap & visualisasi Python | 188 | `Matriks_SLR_Final_Gap.xlsx`, `Matriks_SLR_AI_Campuran.xlsx`, `Daftar_Link_Verifikasi_188_Jurnal 1.xlsx` |

### 1.3 Kurasi metadata untuk Bibliometrix/Biblioshiny

Agar analisis di RStudio (paket `bibliometrix`) tidak gagal (mis. galat `missing value where TRUE/FALSE needed` atau bobot jaringan `Inf/-Inf`), metadata dikurasi sebagai berikut:

- **Standardisasi header** — nama kolom diubah ke huruf kapital (`toupper`) dan ke kode tag WoS (`PY`, `AU`, `TI`, `SO`, `DI`, `AB`, `DE`, `ID`, `CR`, `SR`, …) → `Zotero_Final_Capital.xlsx`.
- **Pembersihan tahun (`PY`)** — nilai kosong/nol/non-numerik dibuang, lalu dikunci sebagai numerik.
- **Normalisasi teks & kata kunci (`TI`, `DE`, `ID`)** — nilai `NA` dibersihkan agar algoritma klastering tidak *crash*.
- **Kelas objek** — `class(df) <- c("bibliometrixDB", "data.frame")`.
- Alternatif lain: metadata dikonversi ke format teks **Web of Science** (`Meta Data GPT/Biblioshiny_WoS_*.txt`) agar dapat diimpor langsung ke Biblioshiny.

### 1.4 Analisis

1. **Statistik deskriptif** — sumber & penulis paling relevan (Biblioshiny).
2. **Struktur konseptual & sosial** — jaringan kolaborasi, jaringan ko-okurensi kata kunci, peta tematik (Biblioshiny, Gephi, NetworkX).
3. **Pemodelan topik** — NMF 5 topik dengan `litstudy`.
4. **Ekstraksi celah riset** — berbasis aturan kata kunci (Python) lalu diperkaya LLM lokal (Ollama `llama3.1`).
5. **Sintesis & rekomendasi judul tesis**.

---

## 2. Alur Kerja (Pipeline)

```
Scopus ──(ekspor RIS)──► Ris.ris (197)
                            │  kurasi di Zotero
                            ▼
              Tes ref.bib (189)  ◄─── korpus utama
              zotero SLR.csv / Zotero_*.xlsx / Meta Data GPT/*.txt
                            │
     ┌──────────────────────┼─────────────────────────────┬──────────────────────┐
     ▼                      ▼                             ▼                      ▼
 jurnal.py            api_scopus.py                konversi_gephi.py     RStudio Biblioshiny
 (litstudy NMF)       (ekstraksi gap)              (nodes/edges CSV)     (Zotero_Final_Capital.xlsx
     │                      │                             │               / Biblioshiny_WoS_*.txt)
     ▼                      ▼                             ▼                      │
 Hasil_Analisis_     Matriks_SLR_Final_Gap.xlsx (188)  nodes.csv, edges.csv      ▼
 Litstudy_Final.docx        │                          → Gephi             Bibilo/*.png, Rplot.png
                            │
   ┌──────────────┬─────────┼───────────────┬──────────────────────┬───────────────────────┐
   ▼              ▼         ▼               ▼                      ▼                       ▼
analisis_gap.py  generate_  sintesis_untuk_ proses_ai_matriks_   visualisasi_literatur.py  visualisasi2.py
                 judul.py   judul.py        scopus.py (Ollama)                             world clod.py
   │              │         │               │                      │                       │
   ▼              ▼         ▼               ▼                      ▼                       ▼
Matriks_SLR_     Draf_Reko- Sintesis_Gap_   Matriks_SLR_AI_      WordCloud_Judul_         WordCloud_Judul_Gap.png
Final_Gap.docx   mendasi_   dan_Rekomen-    Campuran.xlsx        Literatur.png,           Top_Jurnal_Distribusi.png
                 Judul_     dasi_Judul.docx                      Peta_Jaringan_Penulis.png Jaringan_Penulis_
                 Tesis.docx                                                                ResearchRabbit.png
                            │
                            ▼
     Laporan akhir: PEMETAAN BIBLIOMETRIK DAN ANALISIS LITERATUR SISTEMATIS.docx
                    2606828056_ Pramono Pido_Tinjauan Pustaka Sistematis (...).pdf
```

**Urutan eksekusi yang disarankan:**

1. `api_scopus.py` → membuat `Matriks_SLR_Final_Gap.xlsx` (dibutuhkan hampir semua skrip lain)
2. `jurnal.py`, `konversi_gephi.py` (hanya butuh `Tes ref.bib`, bisa kapan saja)
3. `analisis_gap.py`, `sintesis_untuk_judul.py`, `generate_judul.py`
4. `proses_ai_matriks_scopus.py` (butuh server Ollama aktif)
5. `visualisasi_literatur.py`, `visualisasi2.py`, `world clod.py`

---

## 3. Struktur Repositori

### 3.1 Skrip Python

| Berkas | Fungsi singkat |
|---|---|
| `api_scopus.py` | Membaca `Tes ref.bib`, mengekstrak kalimat *gap* dari abstrak, menyimpan `Matriks_SLR_Final_Gap.xlsx` |
| `jurnal.py` | Alur kerja `litstudy`: statistik tahun + *topic modeling* NMF → `Hasil_Analisis_Litstudy_Final.docx` |
| `analisis_gap.py` | Menghitung kategori fokus gap & kata kunci dominan → `Matriks_SLR_Final_Gap.docx` |
| `sintesis_untuk_judul.py` | Sintesis gap kolektif + 5 pilihan judul tesis → `Sintesis_Gap_dan_Rekomendasi_Judul.docx` |
| `generate_judul.py` | Draf judul otomatis per artikel (maks. 35) → `Draf_Rekomendasi_Judul_Tesis.docx` |
| `proses_ai_matriks_scopus.py` | Memperkaya matriks dengan LLM lokal (Ollama) → `Matriks_SLR_AI_Campuran.xlsx` |
| `konversi_gephi.py` | Membuat daftar *node* & *edge* ko-kepenulisan untuk Gephi → `nodes.csv`, `edges.csv` |
| `visualisasi_literatur.py` | Word cloud judul + peta jaringan penulis (versi awal) |
| `visualisasi2.py` | Word cloud & grafik Top-10 jurnal resolusi tinggi (300 DPI) |
| `world clod.py` | Jaringan kolaborasi penulis bergaya ResearchRabbit (latar gelap, 300 DPI). *Catatan: meskipun namanya "world clod", skrip ini membuat peta jaringan, bukan word cloud.* |

### 3.2 Data korpus & metadata

| Berkas | Isi |
|---|---|
| `Ris.ris` | Ekspor mentah Scopus, 197 entri RIS |
| `Tes ref.bib` | Korpus utama BibTeX hasil kurasi Zotero, 189 entri (semua tahun 2025) — input semua skrip berbasis BibTeX |
| `zotero SLR.csv` | Ekspor CSV Zotero (188 baris data, kolom standar Zotero: `Key`, `Item Type`, `Publication Year`, `Author`, `Title`, …) |
| `Zotero_Final.csv.xlsx`, `Zotero_Final.csv - Gdrive.xlsx`, `Zotero_Sempurna.xlsx` | Iterasi ekspor Zotero yang header utamanya sudah dipetakan ke tag WoS (`PY`, `AU`, `TL`, `SO`, `DI`, `AB`, …); 90 kolom |
| `Zotero_Final_Capital.xlsx` | Versi akhir untuk Biblioshiny: seluruh header kapital, ditambah kolom `TC`, `DB`, `DT`, `ID`, `CR`, `SR`; 189 baris × 93 kolom |
| `Zotero_Siap_Sidang.xlsx` | Varian 93 kolom yang header aslinya tidak dikapitalkan |
| `Meta Data GPT/Biblioshiny_WoS_Lengkap.txt` | Metadata 188 dokumen dalam format teks Web of Science (tag `AU`, `TI`, `SO`, `AB`, `DE`, `ID`, `C1`, `RP`, `DB`, …) |
| `Meta Data GPT/Biblioshiny_WoS_Lengkap (1).txt` | Salinan identik dari berkas di atas |
| `Meta Data GPT/Biblioshiny_WoS_Bersih.txt` | Versi ringkas tanpa tag `C1`, `RP`, `DB` (afiliasi & alamat korespondensi) |
| `Systematic_Literature_Review_Overview.ris` | 24 referensi pendukung mengenai metodologi SLR (bukan bagian korpus) |
| `nodes.csv`, `edges.csv` | Jaringan ko-kepenulisan untuk Gephi: 893 penulis, 3.435 relasi tak berarah |

### 3.3 Matriks hasil analisis (Excel)

| Berkas | Isi |
|---|---|
| `Matriks_SLR_Final_Gap.xlsx` | Matriks SLR 188 artikel: `Tahun`, `Penulis`, `Judul Penelitian`, `Jurnal / Sumber`, `Gap Penelitian` |
| `Matriks_SLR_AI_Campuran.xlsx` | Matriks di atas + `Lokasi_Studi_AI`, `Metode_Data_AI` (bahasa Inggris), `Gap_Sintesis_AI` (bahasa Indonesia) |
| `Daftar_Link_Verifikasi_188_Jurnal 1.xlsx` | Tautan DOI resmi & rekaman Scopus untuk verifikasi tiap artikel (186 punya DOI, 2 diverifikasi lewat URL Scopus) |

### 3.4 Laporan (Word/PDF)

| Berkas | Isi |
|---|---|
| `PEMETAAN BIBLIOMETRIK DAN ANALISIS LITERATUR SISTEMATIS.docx` | Naskah laporan SLR utama |
| `2606828056_ Pramono Pido_Tinjauan Pustaka Sistematis (Systematic Literature Review).pdf` | Versi PDF final laporan (8 halaman, berisi gambar) |
| `Hasil_Analisis_Litstudy_Final.docx` | Distribusi tahun & 5 topik NMF |
| `Matriks_SLR_Final_Gap.docx` | Laporan analisis gap otomatis |
| `Sintesis_Gap_dan_Rekomendasi_Judul.docx` | Sintesis gap kolektif & 5 rekomendasi judul tesis |
| `Draf_Rekomendasi_Judul_Tesis.docx` | 35 draf judul tesis berbasis formula |

### 3.5 Visualisasi

| Berkas / folder | Isi | Sumber |
|---|---|---|
| `Bibilo/*.png` | *Most Relevant Sources*, *Most Relevant Authors*, *Collaboration Network*, *Co-occurrence Network*, *Thematic Map* (2 versi) | Biblioshiny |
| `Bibilo/iloveimg-converted/*.jpg` | Versi JPG dari gambar di atas (untuk disisipkan ke laporan) | konversi iLoveIMG |
| `Rplot.png` | Peta tematik (*thematic map*) dari R | RStudio |
| `WordCloud_Judul_Gap.png` | Word cloud judul 188 literatur (HD) | `visualisasi2.py` |
| `Top_Jurnal_Distribusi.png` | Top-10 sumber jurnal (HD) | `visualisasi2.py` |
| `Jaringan_Penulis_ResearchRabbit.png` | Jaringan kolaborasi penulis gaya ResearchRabbit | `world clod.py` |
| `Peta_Jaringan_Penulis.png` | Jaringan ko-kepenulisan (versi awal) | `visualisasi_literatur.py` |
| `New folder/` | Arsip/draf versi lama dari gambar-gambar di atas | campuran |

### 3.6 Peta pikiran (XMind)

| Berkas | Isi |
|---|---|
| `Automated SLR Pipeline Topik Jurnal.xmind` | Rancangan pipeline: sumber data & kueri, pustaka Python (`litstudy`, `pandas`, `openpyxl`, `matplotlib`, `pyvis`, `networkx`, `pybliometrics`), langkah memulai korpus baru |
| `Kerangka Laporan SLR.xmind` | Kerangka laporan SLR (latar belakang, batasan dataset 189 referensi) |
| `Tugas membuat paper berdasarkan laporan SLR yang sudah dibuat.xmind` | Rencana tugas lanjutan: menyusun *paper* dari laporan SLR |

### 3.7 `.gitignore`

Mengecualikan workspace R (`*.RData`, `.Rhistory`), arsip ZIP duplikat, dokumen yang tidak terkait, PNG kosong (0 byte) hasil ekspor Biblioshiny yang gagal, serta folder `Paper/` berisi PDF artikel penerbit (hak cipta).

---

## 4. Dokumentasi Skrip Python

> **Penting:** sebagian besar skrip memakai path absolut Windows
> `E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR`.
> Ubah variabel `folder` / `ALAMAT_FOLDER` / `bibtex_file_path` / `output_dir` ke lokasi repositori Anda sebelum menjalankan. Hanya `visualisasi2.py` dan `world clod.py` yang otomatis memakai folder skrip.

### 4.1 `api_scopus.py` — Ekstraksi matriks gap dari BibTeX

- **Input:** `Tes ref.bib`
- **Output:** `Matriks_SLR_Final_Gap.xlsx`
- **Pustaka:** `litstudy`, `pandas`, `openpyxl`
- **Cara kerja:**
  1. Memuat korpus dengan `litstudy.load_bibtex`.
  2. Untuk tiap dokumen mengambil tahun, penulis (dipisah `; `), judul, nama jurnal (`journal` → `booktitle` → `publisher`), dan abstrak.
  3. Abstrak dipecah menjadi kalimat (`re.split(r'\.(?!\d)')`), kalimat berisi teks hak cipta/penerbit (`copyright`, `©`, `elsevier`, `mdpi`, `springer`, …) dibuang.
  4. Kalimat **pertama** yang mengandung kata penanda gap (`however`, `nevertheless`, `yet`, `still`, `lack`, `limited`, `gap`, `future`, `remain`, `unexplored`, `scarce`, `poorly`, `need`, `recommend`) dijadikan *Gap Penelitian*. Jika tidak ada, dipakai kalimat terakhir abstrak; jika abstrak kosong ditulis `Research gap information not available.`
  5. Excel diformat dengan *wrap text*, kolom E (gap) selebar 95, kolom lain maks. 40.
- *Catatan:* walau bernama `api_scopus`, skrip ini **tidak** memanggil API Scopus; seluruh data diambil dari berkas BibTeX lokal.

### 4.2 `jurnal.py` — Topic modeling dengan litstudy

- **Input:** `Tes ref.bib` → **Output:** `Hasil_Analisis_Litstudy_Final.docx`
- **Pustaka:** `litstudy`, `pandas`, `python-docx`
- **Cara kerja:** menghitung distribusi publikasi per tahun, membangun korpus NLP dari judul + abstrak (`build_corpus`, `ngram_threshold=0.6`), melatih model **NMF** dengan 5 topik (`train_nmf_model`), lalu menulis tabel tahun dan token terbaik per topik ke Word.

### 4.3 `analisis_gap.py` — Laporan analisis gap

- **Input:** `Matriks_SLR_Final_Gap.xlsx` → **Output:** `Matriks_SLR_Final_Gap.docx`
- **Cara kerja:** menggabungkan seluruh teks gap, menghitung frekuensi kata kunci dalam tiga kategori:
  - *Metodologis* — `model`, `method`, `algorithm`, `machine learning`, `svm`, `gis`, `remote sensing`, `mapping`, `analysis`
  - *Empiris* — `data`, `resolution`, `sentinel`, `landsat`, `image`, `spatial`, `temporal`, `dataset`
  - *Kontekstual* — `area`, `region`, `basin`, `zone`, `local`, `case study`, `territory`

  lalu mengambil 10 kata (>4 huruf, di luar *stop words*) paling sering muncul.
- *Catatan:* penghitungan memakai `str.count`, sehingga substring ikut terhitung (mis. `data` di dalam `database`).

### 4.4 `sintesis_untuk_judul.py` — Sintesis gap & judul tesis

- **Input:** `Matriks_SLR_Final_Gap.xlsx` → **Output:** `Sintesis_Gap_dan_Rekomendasi_Judul.docx`
- **Cara kerja:** menghitung indikator `insar`+`deformation`, `dem`+`resolution`, `machine learning`+`model`+`algorithm`, `validation`+`uncertainty`+`limit` pada teks gap, lalu menulis tiga isu gap utama, premis kebaruan (*novelty*), dan **5 pilihan judul tesis** yang sudah ditetapkan di dalam skrip.

### 4.5 `generate_judul.py` — Draf judul per artikel

- **Input:** `Matriks_SLR_Final_Gap.xlsx` → **Output:** `Draf_Rekomendasi_Judul_Tesis.docx`
- **Formula:** `[Fokus Utama] Berbasis [Data] Melalui [Metode] di [Lokasi]`
- **Aturan klasifikasi** (dari judul + gap):

  | Kata kunci | Kategori | Fokus | Data |
  |---|---|---|---|
  | earthquake, fault, tectonic, seismic, deformation | Geodinamika & Kegempaan | Kajian Deformasi Koseismik Sesar Aktif | Data InSAR/SAR |
  | land use, urban, sprawl, cover, dynamics | Perencanaan & Dinamika Lahan | Pemodelan Spasial Perubahan Lahan | Citra Resolusi Tinggi |
  | hazard, risk, flood, erosion, vulnerability | Mitigasi Kebencanaan & Lingkungan | Evaluasi Tingkat Kerentanan Risiko Bencana | Data Penginderaan Jauh dan DEM |
  | lainnya | Analisis Spasial Umum | Analisis Karakteristik Keruangan Wilayah | Data Multi-Sensor Spasial |

  Metode: `insar` → DInSAR, `gis` → SIG, `machine learning`/`svm` → *Machine Learning*, selain itu "Metode Analisis Spasial Komprehensif". Lokasi dideteksi dari daftar nama wilayah (Indonesia, Jakarta, … China, Japan, Turkey, Iran), default "Studi Kasus Wilayah Indonesia". Hanya 35 artikel pertama yang dituliskan.

### 4.6 `proses_ai_matriks_scopus.py` — Pengayaan matriks dengan LLM lokal

- **Input:** `Matriks_SLR_Final_Gap.xlsx` → **Output:** `Matriks_SLR_AI_Campuran.xlsx`
- **Prasyarat:** [Ollama](https://ollama.com) berjalan di `http://localhost:11434` dengan model `llama3.1` (`ollama pull llama3.1`).
- **Cara kerja:** untuk setiap baris, judul dan teks gap (yang telah dibersihkan dari teks hak cipta) dikirim ke Ollama dengan *prompt* yang memaksa format:
  ```
  LOKASI: <lokasi studi, bahasa Inggris>
  METODE: <metode/data/alat, bahasa Inggris>
  GAP:    <1 kalimat celah riset, bahasa Indonesia>
  ```
  Respons di-*parse* dengan regex ke kolom `Lokasi_Studi_AI`, `Metode_Data_AI`, `Gap_Sintesis_AI`. Ada jeda 1 detik antar-permintaan; galat koneksi dicatat dan baris dibiarkan kosong.

### 4.7 `konversi_gephi.py` — Ekspor jaringan ke Gephi

- **Input:** `Tes ref.bib` → **Output:** `nodes.csv` (`Id`, `Label`) dan `edges.csv` (`Source`, `Target`, `Type=undirected`)
- **Pustaka:** `bibtexparser` (API v1, `bibtexparser.load`)
- **Cara kerja:** memecah field `author` dengan `" and "`, setiap penulis menjadi *node*, setiap pasangan penulis dalam satu artikel menjadi *edge*. Impor kedua CSV lewat *Data Laboratory → Import Spreadsheet* di Gephi.

### 4.8 `visualisasi_literatur.py` — Word cloud & jaringan penulis (versi awal)

- **Input:** `Matriks_SLR_Final_Gap.xlsx`
- **Output:** `WordCloud_Judul_Literatur.png`, `Peta_Jaringan_Penulis.png`
- **Cara kerja:** word cloud dari kolom `Judul Penelitian`; graf ko-kepenulisan berbobot dari kolom `Penulis`, hanya menampilkan relasi dengan bobot > 1.

### 4.9 `visualisasi2.py` — Word cloud & Top-10 jurnal (HD)

- **Input:** berkas `.xlsx` pertama di folder skrip yang namanya memuat `AutoFit`, `Final`, atau `Sangat_Rapi` (dimaksudkan: `Matriks_SLR_Final_Gap.xlsx`)
- **Output:** `WordCloud_Judul_Gap.png` (3200×1600, 300 DPI, maks. 200 kata, *stop words* Inggris + Indonesia, kata "insar"/"geodinamika" dibuang), `Top_Jurnal_Distribusi.png` (grafik batang `seaborn` dengan label jumlah artikel)

### 4.10 `world clod.py` — Jaringan penulis gaya ResearchRabbit

- **Input:** sama seperti `visualisasi2.py`
- **Output:** `Jaringan_Penulis_ResearchRabbit.png`
- **Cara kerja:** penulis dihubungkan dengan maksimal 3 penulis berikutnya dalam satu artikel, hanya *node* dengan derajat ≥ 2 yang ditampilkan, tata letak `spring_layout(seed=42)`, ukuran *node* sebanding derajat, latar `#0f172a`.

---

## 5. Kamus Data

### 5.1 `Matriks_SLR_Final_Gap.xlsx` (188 baris)

| Kolom | Deskripsi |
|---|---|
| `Tahun` | Tahun terbit (seluruhnya 2025) |
| `Penulis` | Daftar penulis, dipisah `; ` |
| `Judul Penelitian` | Judul artikel |
| `Jurnal / Sumber` | Nama jurnal / prosiding |
| `Gap Penelitian` | Kalimat celah riset hasil ekstraksi otomatis dari abstrak |

### 5.2 `Matriks_SLR_AI_Campuran.xlsx` (188 baris)

Kolom 5.1 ditambah:

| Kolom | Deskripsi |
|---|---|
| `Lokasi_Studi_AI` | Lokasi/negara/nama sesar (bahasa Inggris), mis. `Luding region, China` |
| `Metode_Data_AI` | Metode, data satelit, atau alat (bahasa Inggris), mis. `InSAR inversion method` |
| `Gap_Sintesis_AI` | Ringkasan celah riset satu kalimat (bahasa Indonesia) |

### 5.3 `Daftar_Link_Verifikasi_188_Jurnal 1.xlsx`

`No.`, `Tahun`, `Judul Artikel`, `Jurnal / Sumber`, `DOI`, `Link DOI Resmi`, `Link Rekaman Scopus`, `Status Verifikasi` (`DOI tersedia` / `Verifikasi melalui URL Scopus`).

### 5.4 Tag metadata gaya WoS (Zotero_*.xlsx, Biblioshiny_WoS_*.txt)

| Tag | Arti | Tag | Arti |
|---|---|---|---|
| `PT` | Jenis publikasi | `DE` | Kata kunci penulis |
| `AU` | Penulis | `ID` | *Keywords Plus* / kata kunci indeks |
| `TI` / `TL` | Judul | `C1` | Afiliasi |
| `SO` | Sumber (jurnal) | `RP` | Alamat korespondensi |
| `PY` | Tahun terbit | `TC` | Jumlah sitasi |
| `DI` | DOI | `DB` | Basis data asal |
| `AB` | Abstrak | `DT` | Tipe dokumen |
| `SN` | ISSN | `CR` | Referensi yang dikutip |
| `VL` / `IS` / `PG` | Volume / nomor / halaman | `SR` | *Short reference* (ID unik bibliometrix) |
| `LA` | Bahasa | `UT` | ID unik rekaman |

---

## 6. Ringkasan Hasil

### 6.1 Sumber paling relevan

| Jurnal | Dokumen |
|---|---:|
| Dizhen Dizhi | 11 |
| Geophysical Research Letters | 8 |
| Remote Sensing | 8 |
| Tectonics | 7 |
| Geophysical Journal International | 5 |
| Tectonophysics; Journal of Structural Geology; Geomorphology; Earth and Planetary Science Letters; Earth Surface Processes and Landforms; Diqiu Kexue (Earth Science – J. China Univ. of Geosciences) | 4 (masing-masing) |

### 6.2 Penulis paling relevan

LI Z (8), ZHANG X (7); LI C, LI J, LI X, LI Y (6); LI H, WANG Y, ZHANG J, ZHANG Y (5).

### 6.3 Struktur konseptual (Biblioshiny)

- **Ko-okurensi kata kunci:** klaster mayor di sekitar *fault slips*, *strike-slip faults*, *earthquakes*, dan *remote sensing*, terhubung dengan *geomorphology* dan *structural geology*.
- **Peta tematik:**
  - *Motor themes* — synthetic aperture radar, seismic hazard, earthquake event
  - *Basic themes* — fault slips, strike-slip faults, earthquakes
  - *Niche themes* — geomorphology, structural geology, miocene
  - *Emerging/declining themes* — remote sensing, active fault

### 6.4 Topik NMF (litstudy)

1. rupture, coseismic, displacement, insar, postseismic
2. gas, reservoir, lake, formation, qaidam
3. late, late_quaternary, segment, rate, quaternary
4. index, lineament, basin, factors, geomorphic
5. landslides, river, debris, sliding, concentrated

### 6.5 Analisis gap

- Indikator fokus gap: Metodologis ≈ 36, Empiris ≈ 38, **Kontekstual ≈ 93**.
- Kata dominan pada gap: *fault* (69), *seismic* (33), *faults* (31), *active* (28), *deformation* (25), *activity* (23), *tectonic* (21), *potential* (21), *earthquake* (19), *hazard* (18).
- Isu gap kolektif: (1) keterbatasan akurasi temporal & spasial data deformasi/penginderaan jauh, (2) ketidakpastian DEM & validasi lapangan, (3) kebutuhan integrasi metode pemodelan spasial modern.
- **Novelty yang diusulkan:** integrasi data multi-sensor dan penyempurnaan metode ekstraksi spasial untuk mengatasi faktor ketidakpastian (*uncertainty*).

### 6.6 Rekomendasi judul tesis

1. Analisis Deformasi Koseismik dan Estimasi Pergeseran Sesar Berbasis Integrasi Data InSAR Multi-Sensor dan Validasi Lapangan
2. Pemodelan Spasial Risiko Bencana Gempabumi Menggunakan Pendekatan Machine Learning dan Koreksi Resolusi DEM
3. Evaluasi Akurasi Pemetaan Aktivitas Sesar Aktif Melalui Analisis Runtun Waktu (Time-Series) InSAR di Wilayah Studi Kasus
4. Kajian Ketidakpastian (*Uncertainty*) Model Bahaya Geofisika Berbasis Penggabungan Data Penginderaan Jauh dan Analisis Spasial Multi-Kriteria
5. Optimasi Pemetaan Deformasi Permukaan Tanah Menggunakan Algoritma Spasial Lanjutan untuk Mitigasi Risiko Kegempaan Wilayah

---

## 7. Instalasi & Cara Menjalankan

### 7.1 Prasyarat

- Python 3.9+
- (Opsional) [Ollama](https://ollama.com) + model `llama3.1` untuk `proses_ai_matriks_scopus.py`
- (Opsional) R + RStudio dengan paket `bibliometrix` untuk Biblioshiny
- (Opsional) [Gephi](https://gephi.org) untuk `nodes.csv`/`edges.csv`

### 7.2 Instalasi pustaka Python

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install pandas openpyxl python-docx litstudy "bibtexparser<2" \
            matplotlib seaborn wordcloud networkx requests
```

### 7.3 Menjalankan

1. Sesuaikan path folder di tiap skrip (lihat [bagian 4](#4-dokumentasi-skrip-python)).
2. Jalankan sesuai urutan:

```bash
python api_scopus.py               # → Matriks_SLR_Final_Gap.xlsx
python jurnal.py                   # → Hasil_Analisis_Litstudy_Final.docx
python konversi_gephi.py           # → nodes.csv, edges.csv
python analisis_gap.py             # → Matriks_SLR_Final_Gap.docx
python sintesis_untuk_judul.py     # → Sintesis_Gap_dan_Rekomendasi_Judul.docx
python generate_judul.py           # → Draf_Rekomendasi_Judul_Tesis.docx
ollama serve & ollama pull llama3.1
python proses_ai_matriks_scopus.py # → Matriks_SLR_AI_Campuran.xlsx
python visualisasi_literatur.py
python visualisasi2.py
python "world clod.py"
```

### 7.4 Biblioshiny

```r
install.packages("bibliometrix")
library(bibliometrix)
biblioshiny()
# Impor: Zotero_Final_Capital.xlsx  ATAU  Meta Data GPT/Biblioshiny_WoS_Bersih.txt (format Web of Science)
```

### 7.5 Memakai pipeline untuk topik baru

1. Cari literatur di Scopus/WoS (atau Zotero/Mendeley) dan ekspor ke BibTeX (`.bib`).
2. Letakkan berkas di folder proyek dan ganti nama/path `Tes ref.bib` di `api_scopus.py`, `jurnal.py`, `konversi_gephi.py`.
3. Sesuaikan daftar kata kunci kategori di `analisis_gap.py`, `generate_judul.py`, `sintesis_untuk_judul.py`, serta daftar judul tetap di `sintesis_untuk_judul.py` dan judul grafik ("188 literatur") di skrip visualisasi.
4. Jalankan ulang pipeline.

---

## 8. Perangkat Eksternal yang Digunakan

| Perangkat | Peran |
|---|---|
| **Scopus** | Basis data sumber literatur |
| **Zotero** | Manajer referensi, deduplikasi & ekspor (BibTeX/CSV/RIS) |
| **RStudio + bibliometrix/Biblioshiny** | Analisis deskriptif, jaringan kolaborasi, ko-okurensi, peta tematik |
| **litstudy** | Pemrosesan BibTeX & *topic modeling* NMF |
| **Ollama (llama3.1)** | Ekstraksi lokasi, metode, dan sintesis gap berbasis LLM lokal |
| **Gephi** | Visualisasi jaringan ko-kepenulisan dari `nodes.csv`/`edges.csv` |
| **ResearchRabbit** | Inspirasi gaya visual peta jaringan penulis |
| **XMind** | Perencanaan pipeline & kerangka laporan |
| **iLoveIMG** | Konversi PNG → JPG untuk laporan |

---

## 9. Catatan, Keterbatasan & Masalah yang Diketahui

1. **Path absolut Windows.** Delapan dari sepuluh skrip memakai path `E:\...` sehingga tidak langsung berjalan di komputer lain.
2. **Pemilihan berkas Excel di `visualisasi2.py` dan `world clod.py` rapuh.** Skrip mengambil berkas `.xlsx` *pertama* yang namanya memuat `Final`. Urutan `glob` bergantung pada sistem berkas: di Windows (urut abjad) yang terpilih `Matriks_SLR_Final_Gap.xlsx`, tetapi di sistem lain bisa terpilih `Zotero_Final_Capital.xlsx` yang tidak punya kolom `Judul Penelitian`/`Penulis` sehingga skrip gagal (`KeyError`). Sebaiknya tetapkan nama berkas secara eksplisit.
3. **Selisih 189 vs 188 dokumen.** `Tes ref.bib` dan `Zotero_Final_Capital.xlsx` berisi 189 entri, sedangkan matriks gap, daftar verifikasi, dan berkas WoS berisi 188. Laporan menyebut 189 dokumen; skrip visualisasi menyebut 188.
4. **Ekstraksi gap berbasis aturan.** Kalimat gap diambil dari abstrak dengan pencocokan kata kunci, sehingga kata umum seperti `yet`, `still`, atau `need` dapat memilih kalimat yang bukan celah riset. Hasil perlu diverifikasi manual; kolom `Gap_Sintesis_AI` juga merupakan keluaran LLM yang bisa keliru.
5. **Penghitungan frekuensi berbasis substring** (`str.count`) di `analisis_gap.py` dan `sintesis_untuk_judul.py` ikut menghitung kata yang mengandung kata kunci (mis. `dem` di dalam `demonstrate`).
6. **Draf judul di `generate_judul.py`** sangat template; hampir seluruh artikel masuk kategori "Geodinamika & Kegempaan" dan lokasi default "Studi Kasus Wilayah Indonesia".
7. **Distribusi tahun tidak informatif** karena kueri dibatasi `PUBYEAR = 2025`.
8. **Berkas duplikat.** `Meta Data GPT/Biblioshiny_WoS_Lengkap (1).txt` identik dengan `Biblioshiny_WoS_Lengkap.txt`; folder `New folder/` dan beberapa varian `Zotero_*.xlsx` adalah iterasi lama.
9. **Kunci API Scopus tersimpan di `Automated SLR Pipeline Topik Jurnal.xmind`.** Karena berkas ini ikut di-*commit*, kunci tersebut sebaiknya dicabut/dibuat ulang di [Elsevier Developer Portal](https://dev.elsevier.com) dan dihapus dari berkas XMind. Untuk ke depannya simpan kunci di variabel lingkungan atau berkas yang di-*ignore*.
10. **Hak cipta.** PDF artikel penerbit sengaja tidak diunggah (`Paper/` di-*ignore*). Abstrak di berkas metadata tetap milik penerbit masing-masing.

---

## 10. Referensi

- Dewi, Y. R., Parahiyanti, C. R., & Nyoko, A. E. L. (2024). Systematic Literature Review: The Methodology Applied for Social Media Marketing Research. *KnE Social Sciences*. https://doi.org/10.18502/kss.v9i4.15076
- Marzi, G., Balzano, M., Caputo, A., & Pellegrini, M. M. (2025). Guidelines for Bibliometric-Systematic Literature Reviews: 10 steps to combine analysis, synthesis and theory development. *International Journal of Management Reviews, 27*(1), 81–103. https://doi.org/10.1111/ijmr.12381
- Referensi metodologi SLR tambahan: `Systematic_Literature_Review_Overview.ris` (24 entri).
- Daftar lengkap 188/189 artikel korpus: `Tes ref.bib` dan `Daftar_Link_Verifikasi_188_Jurnal 1.xlsx`.
