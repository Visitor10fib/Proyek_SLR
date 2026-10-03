import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

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

# --- 2. MEMBUAT WORD CLOUD (Topik Penelitian Saja, Resolusi Tinggi) ---
print("Membuat Word Cloud (Resolusi Tinggi)...")

# Hanya menggunakan kolom Judul Penelitian (Topik), ganti '&' dengan 'dan'
judul_series = df["Judul Penelitian"].astype(str).str.replace(
    "&", " dan ", regex=False
)
teks_mentah = judul_series.str.cat(sep=" ")

stop_words = {
    "the",
    "and",
    "to",
    "of",
    "a",
    "in",
    "for",
    "is",
    "on",
    "that",
    "by",
    "this",
    "with",
    "i",
    "you",
    "it",
    "not",
    "or",
    "be",
    "are",
    "from",
    "at",
    "as",
    "your",
    "all",
    "have",
    "new",
    "more",
    "an",
    "was",
    "we",
    "will",
    "my",
    "can",
    "us",
    "about",
    "if",
    "when",
    "they",
    "yang",
    "dan",
    "di",
    "dari",
    "untuk",
    "pada",
    "dengan",
    "adalah",
    "ini",
    "oleh",
    "sebagai",
    "study",
    "using",
    "based",
    "results",
    "analysis",
    "&",
    "insar",
    "geodinamika",
}

kata_list = teks_mentah.split()
kata_bersih = [w for w in kata_list if w.lower() not in ["insar", "geodinamika"]]
teks_gabungan = " ".join(kata_bersih)

# Mengatur ukuran kanvas besar agar detail tajam
wordcloud = WordCloud(
    width=3200,
    height=1600,
    background_color="white",
    stopwords=stop_words,
    colormap="viridis",
    max_words=200,
).generate(teks_gabungan)

path_wc = os.path.join(BASE_DIR, "WordCloud_Judul_Gap.png")
plt.figure(figsize=(16, 8), dpi=300)  # Resolusi tinggi 300 DPI
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title(
    "Word Cloud Topik Penelitian dari 188 literatur",
    fontsize=18,
    fontweight="bold",
    pad=20,
)
plt.tight_layout()
plt.savefig(path_wc, dpi=300, bbox_inches="tight")
plt.close()
print(f"Word Cloud HD tersimpan di: {path_wc}")

# --- 3. MEMBUAT GRAFIK TOP 10 JURNAL (Resolusi Tinggi) ---
print("Membuat Grafik Top 10 Jurnal (Resolusi Tinggi)...")

# Membersihkan nama jurnal dan mengganti '&' dengan 'dan'
jurnal_series = df["Jurnal / Sumber"].astype(str).str.replace(
    "&", " dan ", regex=False
)
top_jurnals = jurnal_series.value_counts().head(10)


def clean_label(label):
  if len(str(label)) > 45:
    return str(label)[:42] + "..."
  return str(label)


cleaned_labels = [clean_label(j) for j in top_jurnals.index]

path_chart = os.path.join(BASE_DIR, "Top_Jurnal_Distribusi.png")
plt.figure(
    figsize=(12, 7), dpi=300
)  # Ukuran lebar & tinggi besar dengan resolusi 300 DPI
ax = sns.barplot(y=cleaned_labels, x=top_jurnals.values, palette="viridis")

plt.title(
    "Top 10 Sumber Jurnal Paling Sering Digunakan\ndari 188 literatur",
    fontsize=16,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Jumlah Artikel", fontsize=13)
plt.ylabel("Nama Jurnal", fontsize=13)

# Menambahkan angka statistik di ujung batang grafik
for p in ax.patches:
  width = p.get_width()
  ax.annotate(
      f"{int(width)}",
      (width + 0.1, p.get_y() + p.get_height() / 2.0),
      ha="left",
      va="center",
      fontsize=11,
      fontweight="bold",
      color="black",
  )

plt.xlim(0, max(top_jurnals.values) + 2)
plt.tight_layout()
plt.savefig(path_chart, dpi=300, bbox_inches="tight")
plt.close()
print(f"Grafik Top Jurnal HD tersimpan di: {path_chart}")

print(
    "\nSUKSES BESAR! Seluruh gambar resolusi tertinggi (300 DPI) berhasil"
    " dirender ulang."
)