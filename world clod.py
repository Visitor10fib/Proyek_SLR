import glob
import os
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import re

# --- 1. MENDAPATKAN DIREKTORI LOKAL SECARA OTOMATIS ---
BASE_DIR = (
    os.path.dirname(os.path.abspath(__file__))
    if "__file__" in locals()
    else os.getcwd()
)

# Mencari file Excel matriks SLR secara otomatis di folder proyek
excel_files = glob.glob(os.path.join(BASE_DIR, "*.xlsx"))
if not excel_files:
  print(
      "ERROR: Tidak ditemukan file Excel (.xlsx) di dalam folder Proyek_SLR!"
  )
  exit()

FILE_INPUT = excel_files[0]
for f in excel_files:
  if "AutoFit" in f or "Final" in f or "Sangat_Rapi" in f:
    FILE_INPUT = f
    break

print(f"Membaca data dari: {os.path.basename(FILE_INPUT)}")
df = pd.read_excel(FILE_INPUT)

# --- 2. MEMBANGUN GRAF JARINGAN KOLABORASI PENULIS ---
print("Memproses peta jaringan penulis gaya Research Rabbit (HD 300 DPI)...")
G = nx.Graph()

for penulis_str in df["Penulis"].dropna():
  daftar_penulis = [
      p.strip() for p in re.split(r"[,;]", str(penulis_str)) if len(p.strip()) > 2
  ]
  for i in range(len(daftar_penulis)):
    for j in range(i + 1, min(len(daftar_penulis), i + 4)):
      p1, p2 = daftar_penulis[i], daftar_penulis[j]
      if G.has_edge(p1, p2):
        G[p1][p2]["weight"] += 1
      else:
        G.add_edge(p1, p2, weight=1)

# Filter node inti untuk menjaga kerapian kluster
core_nodes = [node for node, deg in G.degree() if deg >= 2]
SubG = G.subgraph(core_nodes)
if len(SubG.nodes()) == 0:
  SubG = G

# --- 3. RENDER VISUALISASI ESTETIK (Research Rabbit Style) ---
path_net = os.path.join(BASE_DIR, "Jaringan_Penulis_ResearchRabbit.png")

# Menggunakan latar belakang gelap elegan khas Research Rabbit dengan resolusi 300 DPI
plt.figure(figsize=(16, 16), dpi=300, facecolor="#0f172a")
ax = plt.gca()
ax.set_facecolor("#0f172a")

# Tata letak pegas estetika
pos = nx.spring_layout(SubG, k=0.3, iterations=120, seed=42)
node_sizes = [SubG.degree(node) * 250 + 150 for node in SubG.nodes()]

# Menggambar garis koneksi dan node
nx.draw_networkx_edges(
    SubG, pos, alpha=0.2, edge_color="#38bdf8", width=1.0, style="solid"
)
nx.draw_networkx_nodes(
    SubG,
    pos,
    node_size=node_sizes,
    node_color="#06b6d4",
    alpha=0.9,
    edgecolors="#ffffff",
    linewidths=1.2,
)

# Label nama penulis
labels = {node: node for node in SubG.nodes()}
nx.draw_networkx_labels(
    SubG,
    pos,
    labels=labels,
    font_size=8,
    font_family="sans-serif",
    font_weight="bold",
    font_color="#f8fafc",
)

# Judul grafik yang bersih dan sesuai permintaan
plt.title(
    "Jaringan Kolaborasi Penulis dari 188 jurnal",
    fontsize=18,
    fontweight="bold",
    color="#f8fafc",
    pad=25,
)

plt.axis("off")
plt.tight_layout()
plt.savefig(
    path_net,
    dpi=300,
    bbox_inches="tight",
    facecolor=ax.get_facecolor(),
    edgecolor="none",
)
plt.close()

print(f"Peta Jaringan Penulis HD tersimpan di: {path_net}")