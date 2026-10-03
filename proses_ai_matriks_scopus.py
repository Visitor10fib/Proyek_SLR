import pandas as pd
import requests
import time
import os
import re

# --- KONFIGURASI ---
NAMA_MODEL = "llama3.1"
URL_OLLAMA = "http://localhost:11434/api/generate"

ALAMAT_FOLDER = r"E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR"
FILE_INPUT = os.path.join(ALAMAT_FOLDER, "Matriks_SLR_Final_Gap.xlsx")
FILE_OUTPUT = os.path.join(ALAMAT_FOLDER, "Matriks_SLR_AI_Campuran.xlsx") # Nama file baru

print(f"Membaca data dari:\n{FILE_INPUT}\n")
try:
    df = pd.read_excel(FILE_INPUT)
except FileNotFoundError:
    print(f"ERROR: File tidak ditemukan.")
    exit()

df['Lokasi_Studi_AI'] = ""
df['Metode_Data_AI'] = ""
df['Gap_Sintesis_AI'] = ""

total_baris = len(df)
print(f"Total data ditemukan: {total_baris} baris.")
print(f"Memulai proses AI ({NAMA_MODEL}) ke SELURUH baris...\n")

for index, row in df.iterrows():
    judul = str(row.get('Judul Penelitian', 'No Title'))
    gap_asli = str(row.get('Gap Penelitian', 'No Description'))
    
    # Membersihkan teks dari hak cipta
    gap_asli_bersih = re.sub(r'(?i)(©|copyright|The Author\(s\).*?|All rights reserved.*?|Published by.*?)', '', gap_asli)
    
    # Prompt dengan instruksi bahasa campuran yang ketat
    prompt = f"""
    You are an expert Geography research assistant. Analyze the text below and extract 3 specific pieces of information.
    
    CRITICAL INSTRUCTIONS:
    1. For LOKASI and METODE, use ENGLISH. If missing, write "Not specified".
    2. For GAP, you MUST translate and summarize it into INDONESIAN (Bahasa Indonesia). If missing, write "Tidak disebutkan".
    3. DO NOT use introductory phrases (e.g., "Here is...", "The gap is...").
    4. You MUST format your answer EXACTLY like this template:
    
    LOKASI: [Extract study location, country, or fault name in English]
    METODE: [Extract method, satellite data, or tools used in English]
    GAP: [Tuliskan 1 kalimat inti celah penelitian atau temuan utama dalam BAHASA INDONESIA]
    
    Title: {judul}
    Original Text: {gap_asli_bersih}
    """
    
    payload = {
        "model": NAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        print(f"Memproses baris {index+1}/{total_baris}: {judul[:40]}...")
        
        response = requests.post(URL_OLLAMA, json=payload)
        response.raise_for_status()
        
        hasil_ai = response.json().get('response', '').strip()
        
        lokasi_match = re.search(r'LOKASI:\s*(.*?)(?=METODE:|GAP:|$)', hasil_ai, re.IGNORECASE | re.DOTALL)
        metode_match = re.search(r'METODE:\s*(.*?)(?=GAP:|$)', hasil_ai, re.IGNORECASE | re.DOTALL)
        gap_match = re.search(r'GAP:\s*(.*)', hasil_ai, re.IGNORECASE | re.DOTALL)
        
        df.at[index, 'Lokasi_Studi_AI'] = lokasi_match.group(1).strip() if lokasi_match else "Extraction failed"
        df.at[index, 'Metode_Data_AI'] = metode_match.group(1).strip() if metode_match else "Extraction failed"
        df.at[index, 'Gap_Sintesis_AI'] = gap_match.group(1).strip() if gap_match else hasil_ai 
        
    except requests.exceptions.ConnectionError:
        print(f"Baris {index+1}: ERROR - Tidak terhubung ke Ollama.")
    except Exception as e:
        print(f"Baris {index+1}: ERROR - {e}")
        
    time.sleep(1)

# --- SIMPAN HASIL ---
print(f"\nMenyimpan hasil ke:\n{FILE_OUTPUT}\n")
try:
    df.to_excel(FILE_OUTPUT, index=False)
    print(f"Selesai! Silakan buka file Matriks_SLR_AI_Campuran.xlsx")
except Exception as e:
    print(f"Gagal menyimpan file Excel: {e}")