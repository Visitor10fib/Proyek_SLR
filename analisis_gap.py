import os
import pandas as pd
from collections import Counter
from docx import Document

print("=== MENYUSUN LAPORAN ANALISIS GAP OTOMATIS KE WORD ===")

# Direktori proyek tugas GeoMetPen
folder = r"E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR"
file_excel = os.path.join(folder, "Matriks_SLR_Final_Gap.xlsx")
file_word = os.path.join(folder, "Matriks_SLR_Final_Gap.docx")

if os.path.exists(file_excel):
    df = pd.read_excel(file_excel)
    total_jurnal = len(df)
    print(f"[SUKSES] Membaca {total_jurnal} data jurnal dari Excel.")

    # Analisis Kategori Fokus Gap
    kategori_fokus = {
        'Metodologis (Metode/Algoritma/Model)': ['model', 'method', 'algorithm', 'machine learning', 'svm', 'gis', 'remote sensing', 'mapping', 'analysis'],
        'Empiris (Data/Citra/Resolusi)': ['data', 'resolution', 'sentinel', 'landsat', 'image', 'spatial', 'temporal', 'dataset'],
        'Kontekstual (Wilayah/Kawasan/Studi Kasus)': ['area', 'region', 'basin', 'zone', 'local', 'case study', 'territory']
    }

    hasil_analisis = {k: 0 for k in kategori_fokus}
    semua_teks = " ".join(df['Gap Penelitian'].dropna().astype(str)).lower()

    for kat, keywords in kategori_fokus.items():
        for kw in keywords:
            hasil_analisis[kat] += semua_teks.count(kw)

    # Ekstraksi kata kunci teknis dominan
    kata_bersih = [w.strip('.,()[]{}:;') for w in semua_teks.split() if len(w) > 4]
    stop_words = {'however', 'further', 'research', 'study', 'based', 'results', 'which', 'using', 'there', 'between', 'these', 'should', 'would', 'could'}
    kata_filter = [w for w in kata_bersih if w not in stop_words]
    common_words = Counter(kata_filter).most_common(10)

    # Membuat Dokumen Word untuk Hasil Analisis
    doc = Document()
    
    # Judul Laporan
    doc.add_heading('Laporan Analisis Otomatis Celah Riset (Research Gap)', level=1)
    doc.add_paragraph('Mata Kuliah: Metodologi Penelitian Geografi (GeoMetPen) - Departemen Geografi UI\n')

    # Ringkasan Eksekutif
    doc.add_heading('1. Ringkasan Korpus Literatur', level=2)
    doc.add_paragraph(f'Total literatur yang dianalisis secara sistematis dari korpus lokal adalah sebanyak {total_jurnal} jurnal.')

    # Distribusi Fokus Celah Riset
    doc.add_heading('2. Distribusi Fokus Celah Riset', level=2)
    doc.add_paragraph('Berdasarkan pemindaian otomatis terhadap teks abstrak dan celah riset, berikut adalah distribusi kecenderungan fokus literatur:')
    for kat, count in hasil_analisis.items():
        doc.add_paragraph(f'- {kat}: terdeteksi ~{count} indikator frekuensi.', style='List Bullet')

    # Kata Kunci Teknis Dominan
    doc.add_heading('3. Kata Kunci Teknis Paling Dominan pada Gap', level=2)
    doc.add_paragraph('Istilah teknis yang paling sering muncul dalam diskusi batasan/celah penelitian meliputi:')
    for word, freq in common_words:
        doc.add_paragraph(f'• {word.capitalize()} (muncul {freq} kali)', style='List Bullet')

    # Catatan untuk Novelty
    doc.add_heading('4. Implikasi untuk Perumusan Novelty Tesis', level=2)
    doc.add_paragraph(
        'Distribusi dan frekuensi kata kunci di atas dapat digunakan sebagai dasar untuk mengidentifikasi '
        'titik kosong (blind spot) riset, yang selanjutnya diterjemahkan ke dalam rumusan masalah, tujuan, '
        'serta anatomi judul tesis berstandar spasial.'
    )

    # Simpan ke Word
    doc.save(file_word)
    print(f"\n-> BERHASIL: Laporan analisis gap tersimpan rapi sebagai 'Matriks_SLR_Final_Gap.docx'")
else:
    print(f"[GAGAL] File Excel 'Matriks_SLR_Final_Gap.xlsx' tidak ditemukan.")
    