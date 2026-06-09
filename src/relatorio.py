import csv
import os

from src.utils import (
    agora_para_nome_arquivo,
    log_sucesso,
)

from src.paths import PASTA_RELATORIOS

from src.mensagens import (
    MSG_RELATORIO_GERADO_SUCESSO,
    MSG_CAMINHO_RELATORIO,
    )

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

    log_sucesso(MSG_RELATORIO_GERADO_SUCESSO)
    log_sucesso(MSG_CAMINHO_RELATORIO.format(caminho=caminho_relatorio))

    return caminho_relatorio