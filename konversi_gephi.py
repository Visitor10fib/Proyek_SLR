import csv
import bibtexparser
from itertools import combinations
import os

# Menggunakan jalur mutlak langsung ke folder Proyek_SLR Anda
bibtex_file_path = r'e:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR\Tes ref.bib'

print("Membaca file BibTeX...")
with open(bibtex_file_path, 'r', encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

nodes = set()
edges = []

# Ekstrak penulis dari setiap artikel
for entry in bib_database.entries:
    author_field = entry.get('author', '')
    if author_field:
        authors = [a.strip() for a in author_field.split(' and ')]
        
        for author in authors:
            if author:
                nodes.add(author)
        
        if len(authors) > 1:
            for pair in combinations(sorted(authors), 2):
                edges.append(pair)

# Tentukan folder output secara otomatis agar file CSV tersimpan persis di folder Proyek_SLR
output_dir = r'e:\MATA KULIAH SEMESTER 1 DEPARTEMEN GEOGRAFI UNIVERSITAS INDONESIA\Metodologi Penelitian Geografi - GeoMetPen\Proyek_SLR'

# Simpan file Nodes.csv
nodes_path = os.path.join(output_dir, 'nodes.csv')
with open(nodes_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Id', 'Label'])
    for author in sorted(nodes):
        writer.writerow([author, author])

# Simpan file Edges.csv
edges_path = os.path.join(output_dir, 'edges.csv')
with open(edges_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Source', 'Target', 'Type'])
    for edge in edges:
        writer.writerow([edge[0], edge[1], 'undirected'])

print("Berhasil! File nodes.csv dan edges.csv telah dibuat di folder Proyek_SLR.")