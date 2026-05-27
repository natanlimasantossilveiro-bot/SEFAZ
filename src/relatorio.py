import csv
import os

from src.utils import agora_para_nome_arquivo

from src.paths import PASTA_RELATORIOS

def gerar_relatorio_emissao(registros):

    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    nome_arquivo = f"relatorio_sefaz_{agora_para_nome_arquivo()}.csv"

    caminho_relatorio = os.path.join(
        PASTA_RELATORIOS,
        nome_arquivo
    )

    colunas = [
        "documento",
        "status",
        "mensagem",
        "caminho_pdf",
        "caminho_evidencia"
    ]

    with open(caminho_relatorio, "w", newline="", encoding="utf-8-sig") as arquivo_csv:

        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=colunas,
            delimiter=";"
        )

        escritor.writeheader()

        escritor.writerows(registros)

    print("Relatório gerado com sucesso!")
    print("Caminho: ", caminho_relatorio)

    return caminho_relatorio    