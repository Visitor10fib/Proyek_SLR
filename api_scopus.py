import os
import re
import litstudy as ls
import pandas as pd
import openpyxl
from openpyxl.styles import Alignment

print("=== MEMBUAT MATRIKS SLR FINAL (HANYA ISI TEKS GAP) ===")

# Direktori proyek tugas GeoMetPen
folder = r"E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR"
file_bib = os.path.join(folder, "Tes ref.bib")

if os.path.exists(file_bib):
    dataset = ls.load_bibtex(file_bib)
    print(f"[SUKSES] Memuat {len(dataset)} literatur dari korpus lokal.\n")

    data_dokumen = []
    target_dataset = dataset  # Memproses seluruh 188 literatur
    
    for idx, doc in enumerate(target_dataset):  
        # Ekstraksi Metadata Jurnal & Tahun
        sumber = getattr(doc, 'journal', '') or getattr(doc, 'source', '') or getattr(doc, 'container_title', '')
        if not sumber and hasattr(doc, 'entry') and doc.entry:
            sumber = doc.entry.get('journal', '') or doc.entry.get('booktitle', '') or doc.entry.get('publisher', '')

        tahun_val = getattr(doc, 'year', '') or (doc.entry.get('year', '') if hasattr(doc, 'entry') and doc.entry else '')

        penulis_mentah = getattr(doc, 'authors', [])
        str_penulis = "; ".join([str(a).replace('<', '').replace('>', '').strip() for a in penulis_mentah])

        judul_teks = getattr(doc, 'title', '')
        teks_abstrak = getattr(doc, 'abstract', '') or (doc.entry.get('abstract', '') if hasattr(doc, 'entry') and doc.entry else '')

        # Membersihkan teks abstrak dan mendeteksi bagian Gap
        if teks_abstrak and len(teks_abstrak.strip()) > 30:
            kalimat_mentah = [k.strip() for k in re.split(r'\.(?!\d)', teks_abstrak) if len(k.strip()) > 5]
            
            kata_sampah = [
                'download', 'permission', 'copyright', 'all rights', 
                'springer', 'elsevier', 'mdpi', 'taylor & francis', 
                'union of iraqi geologists', '©', 'published by'
            ]
            
            kalimat_bersih = [
                k for k in kalimat_mentah 
                if not any(sampah in k.lower() for sampah in kata_sampah)
            ]
            
            if kalimat_bersih:
                # Ekstraksi Gap berdasarkan kata kunci akademik internasional
                keyword_gap = ['however', 'nevertheless', 'yet', 'still', 'lack', 'limited', 'gap', 'future', 'remain', 'unexplored', 'scarce', 'poorly', 'need', 'recommend']
                celah_ditemukan = None
                
                for k in kalimat_bersih:
                    if any(kw in k.lower() for kw in keyword_gap):
                        celah_ditemukan = k + "."
                        break
                
                if not celah_ditemukan and len(kalimat_bersih) > 1:
                    celah_ditemukan = kalimat_bersih[-1] + "."
                elif not celah_ditemukan:
                    celah_ditemukan = "Further spatial and temporal analysis is needed for the study area."
            else:
                celah_ditemukan = "Research gap information not available."
        else:
            celah_ditemukan = "Research gap information not available."

        # Langsung memasukkan teks celah riset tanpa awalan tulisan "Gap:" di dalam sel
        data_dokumen.append({
            'Tahun': tahun_val,
            'Penulis': str_penulis,
            'Judul Penelitian': judul_teks,
            'Jurnal / Sumber': sumber,
            'Gap Penelitian': celah_ditemukan
        })

    # Konversi ke DataFrame Pandas dan Ekspor ke Excel
    df = pd.DataFrame(data_dokumen)
    file_excel = os.path.join(folder, "Matriks_SLR_Final_Gap.xlsx")
    
    with pd.ExcelWriter(file_excel, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        
        # Pengaturan tata letak dan lebar kolom Excel agar rapi
        for col in worksheet.columns:
            max_len = 0
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            for cell in col:
                cell.alignment = Alignment(wrap_text=True, vertical='top')
                if cell.value and len(str(cell.value)) > max_len:
                    max_len = len(str(cell.value))
                        
            if col_letter == 'E':
                worksheet.column_dimensions[col_letter].width = 95  # Lebar khusus kolom Gap
            else:
                worksheet.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)

    print(f"\n-> BERHASIL: Seluruh {len(target_dataset)} literatur tersimpan sebagai 'Matriks_SLR_Final_Gap.xlsx'")
else:
    print("[GAGAL] File korpus 'Tes ref.bib' tidak ditemukan di direktori target.")