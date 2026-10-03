import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx

# --- KONFIGURASI DIREKTORI ---
ALAMAT_FOLDER = r"E:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR"
FILE_INPUT = os.path.join(ALAMAT_FOLDER, "Matriks_SLR_Final_Gap.xlsx")

print(f"Membaca data dari:\n{FILE_INPUT}\n")
try:
    df = pd.read_excel(FILE_INPUT)
except FileNotFoundError:
    print(f"ERROR: File Excel input tidak ditemukan.")
    exit()

# ==========================================
# 1. MEMBUAT WORD CLOUD DARI JUDUL PENELITIAN
# ==========================================
print("Sedang menghasilkan Word Cloud...")
teks_judul = " ".join(str(judul) for judul in df['Judul Penelitian'].dropna())

wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(teks_judul)

file_wc = os.path.join(ALAMAT_FOLDER, "WordCloud_Judul_Literatur.png")
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud Topik Literatur Sesar & InSAR", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(file_wc, dpi=300)
plt.close()
print(f"Word Cloud berhasil disimpan ke: {file_wc}")


# ==========================================
# 2. MEMBUAT PETA JARINGAN PENULIS (NETWORK MAP)
# ==========================================
print("Sedang membangun Peta Jaringan Penulis...")
G = nx.Graph()

# Mengambil kolom Penulis (pastikan nama kolom di Excel Anda sesuai, misal 'Penulis')
for penulis_str in df['Penulis'].dropna():
    # Memisahkan penulis jika dalam satu baris terdapat banyak penulis (dipisah koma atau titik koma)
    daftar_penulis = [p.strip() for p in str(penulis_str).replace(';', ',').split(',') if len(p.strip()) > 2]
    
    # Menghubungkan antar penulis dalam satu artikel yang sama
    for i in range(len(daftar_penulis)):
        for j in range(i + 1, len(daftar_penulis)):
            p1, p2 = daftar_penulis[i], daftar_penulis[j]
            if G.has_edge(p1, p2):
                G[p1][p2]['weight'] += 1
            else:
                G.add_edge(p1, p2, weight=1)

# Menyaring jaringan agar hanya menampilkan penulis yang memiliki koneksi/kolaborasi lebih dari 1
edges_to_keep = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > 1]
sub_G = G.edge_subgraph(edges_to_keep).copy() if edges_to_keep else G

file_net = os.path.join(ALAMAT_FOLDER, "Peta_Jaringan_Penulis.png")
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(sub_G, k=0.15, iterations=50)
nx.draw_networkx_nodes(sub_G, pos, node_size=50, node_color='skyblue')
nx.draw_networkx_edges(sub_G, pos, alpha=0.3, edge_color='gray')
nx.draw_networkx_labels(sub_G, pos, font_size=8, font_family='sans-serif')

plt.title("Peta Jaringan Kolaborasi Penulis (Co-authorship)", fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig(file_net, dpi=300)
plt.close()
print(f"Peta Jaringan Penulis berhasil disimpan ke: {file_net}")

print("\nSemua visualisasi berhasil digenerate dan disimpan di folder Proyek_SLR!")