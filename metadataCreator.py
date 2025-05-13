import os
import argparse
import subprocess
import sys

try:
    import openpyxl
except ImportError:
    print("openpyxl não encontrado. Instalando...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])
    
import openpyxl

def gerar_metadata(diretorios, arquivo_saida):
    """
    Gera um arquivo XLSX com metadados dos arquivos .fastq em múltiplos diretórios.

    Args:
      diretorios: Uma lista de caminhos para os diretórios contendo os arquivos .fastq.
      arquivo_saida: O nome do arquivo XLSX de saída.
    """
    # Cria um novo arquivo XLSX
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "manifest"

    # Adiciona as colunas na primeira linha
    worksheet.append(["sample-id", "absolute-filepath", "direction"])

    # Loop pelos diretórios
    for diretorio in diretorios:
        # Loop pelos arquivos do diretório
        for filename in os.listdir(diretorio):
            if "_" in filename and filename.endswith(".fastq"):
                # Obtém o caminho absoluto do arquivo
                filepath = os.path.join(diretorio, filename)

                # Extrai o sample-id
                sample_id = filename.split("_")[0]

                # Filtra apenas os registros paired-end
                if "_" in filename:

                    # Define a direction
                    if "_1" in filename:
                        direction = "forward"
                    elif "_2" in filename:
                        direction = "reverse"
                    else:
                        direction = "unknown"  # Caso não encontre _1 ou _2

                    # Adiciona uma nova linha na planilha
                    worksheet.append([sample_id, filepath, direction])

    # Salva o arquivo XLSX no caminho expecificado
    workbook.save(arquivo_saida + ".xlsx")

if __name__ == "__main__":

    # Cria o parser de argumentos
    parser = argparse.ArgumentParser(description="Gera metadados de arquivos .fastq em um arquivo XLSX.")
    parser.add_argument("-i", "--input", required=True, nargs="+", help="Caminhos para os diretórios com os arquivos .fastq (separe múltiplos diretórios por espaço)")
    parser.add_argument("-o", "--output", required=True, help="Nome do arquivo XLSX de saída")

    # Analisa os argumentos da linha de comando
    args = parser.parse_args()

    # Chama a função para gerar o arquivo
    gerar_metadata(args.input, args.output)