import os
import pandas as pd
from docx import Document

print("=== MEMPERBAHARUI SKRIP: MENGHILANGKAN PEMBOROSAN KATA 'DAN' ===")

folder = r"E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR"
file_excel = os.path.join(folder, "Matriks_SLR_Final_Gap.xlsx")
file_output_word = os.path.join(folder, "Draf_Rekomendasi_Judul_Tesis.docx")

if os.path.exists(file_excel):
    df = pd.read_excel(file_excel)
    print(f"[SUKSES] Membaca {len(df)} data dari file Excel.")

    doc = Document()
    doc.add_heading('Rekomendasi Draf Judul Tesis Spasial (Gaya Akademik Ringkas)', level=1)
    doc.add_paragraph('Berdasarkan Ekstraksi Topikal Korpus Literatur Geografi (GeoMetPen UI)\n')

    doc.add_heading('Draf Kombinasi Judul:', level=2)
    doc.add_paragraph('Formula: [Fokus Utama] Berbasis [Data] Menggunakan [Metode] di [Lokasi]\n')

    count = 0
    for idx, row in df.iterrows():
        judul_asli = str(row['Judul Penelitian'])
        gap_teks = str(row['Gap Penelitian'])
        teks_gabung = (judul_asli + " " + gap_teks).lower()
        
        # Fokus Utama yang lebih ringkas (menghindari tumpukan kata 'dan')
        if any(k in teks_gabung for k in ['earthquake', 'fault', 'tectonic', 'seismic', 'deformation']):
            kategori = "Geodinamika & Kegempaan"
            fokus_str = "Kajian Deformasi Koseismik Sesar Aktif"
            data_default = "Data InSAR/SAR"
        elif any(k in teks_gabung for k in ['land use', 'urban', 'sprawl', 'cover', 'dynamics']):
            kategori = "Perencanaan & Dinamika Lahan"
            fokus_str = "Pemodelan Spasial Perubahan Lahan"
            data_default = "Citra Resolusi Tinggi"
        elif any(k in teks_gabung for k in ['hazard', 'risk', 'flood', 'erosion', 'vulnerability']):
            kategori = "Mitigasi Kebencanaan & Lingkungan"
            fokus_str = "Evaluasi Tingkat Kerentanan Risiko Bencana"
            data_default = "Data Penginderaan Jauh dan DEM"
        else:
            kategori = "Analisis Spasial Umum"
            fokus_str = "Analisis Karakteristik Keruangan Wilayah"
            data_default = "Data Multi-Sensor Spasial"

        # Deteksi Lokasi
        loc_candidates = ['indonesia', 'jakarta', 'bandung', 'citarum', 'jawa', 'sumatra', 'kalimantan', 'sulawesi', 'china', 'japan', 'turkey', 'iran']
        found_loc = [loc.capitalize() for loc in loc_candidates if loc in teks_gabung]
        lokasi_str = found_loc[0] if found_loc else "Studi Kasus Wilayah Indonesia"

        # Ekstraksi Metode (Ringkas)
        if 'insar' in teks_gabung:
            metode_str = "Teknik Differential InSAR (DInSAR)"
        elif 'gis' in teks_gabung:
            metode_str = "Pendekatan Sistem Informasi Geografis"
        elif 'machine learning' in teks_gabung or 'svm' in teks_gabung:
            metode_str = "Algoritma Machine Learning"
        else:
            metode_str = "Metode Analisis Spasial Komprehensif"

        count += 1
        if count <= 35:
            # Menggunakan struktur sambung yang mengalir dan meminimalisir kata "dan"
            draf_judul = f"{fokus_str} Berbasis {data_default} Melalui {metode_str} di {lokasi_str}"
            
            p = doc.add_paragraph()
            p.add_run(f"{count}. [{kategori}]\n").bold = True
            p.add_run(f"   - Draf Judul: ").bold = True
            p.add_run(f"{draf_judul}\n")
            p.add_run(f"   - Referensi Asli: {judul_asli[:85]}...\n")

    doc.save(file_output_word)
    print(f"\n-> BERHASIL: {count} draf judul tanpa penumpukan kata 'dan' tersimpan di Word.")
else:
    print(f"[GAGAL] File Excel tidak ditemukan.")