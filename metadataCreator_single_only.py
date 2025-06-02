
import os
import csv

# Diretório contendo os arquivos .fastq.gz
input_dir = input("Digite o caminho completo da pasta com os arquivos .fastq.gz: ").strip()

# Nome do arquivo de saída
output_file = "metadata.tsv"

# Coletando todos os arquivos .fastq.gz no diretório
fastq_files = [f for f in os.listdir(input_dir) if f.endswith(".fastq.gz")]

# Removendo possíveis duplicatas e extensões para criar sample IDs
samples = {}
for f in fastq_files:
    sample_id = os.path.splitext(os.path.splitext(f)[0])[0]
    samples[sample_id] = os.path.join(os.path.abspath(input_dir), f)

# Escrevendo o arquivo metadata.tsv no formato single
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerow(["sample-id", "absolute-filepath", "direction"])
    for sample_id, filepath in sorted(samples.items()):
        writer.writerow([sample_id, filepath, "single"])

print(f"Arquivo '{output_file}' criado com sucesso com {len(samples)} amostras.")
