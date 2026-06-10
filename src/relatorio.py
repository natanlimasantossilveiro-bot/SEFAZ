import csv
import os

from openpyxl import Workbook
from openpyxl.styles import Font

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
        nome_arquivo,
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
            delimiter=";",
        )

        escritor.writeheader()

        escritor.writerows(registros)

    workbook = Workbook()

    planilha = workbook.active
    planilha.title = "Emissão SEFAZ"

    planilha.append(colunas)

    for celula in planilha[1]:
        celula.font = Font(bold=True)

    planilha.freeze_panes = "A2"

    for registro in registros:
        planilha.append([
            registro.get("documento"),
            registro.get("status"),
            registro.get("mensagem"),
            registro.get("caminho_pdf"),
            registro.get("caminho_evidencia"),
        ])

    planilha.auto_filter.ref = planilha.dimensions
    
    for coluna in planilha.columns:
        maior_tamanho = 0
        letra_coluna = coluna[0].column_letter
        
        for celula in coluna:
            if celula.value:
                maior_tamanho = max(maior_tamanho, len(str(celula.value)))

        planilha.column_dimensions[letra_coluna].width = maior_tamanho + 2

    caminho_excel = caminho_relatorio.replace(".csv", ".xlsx")

    workbook.save(caminho_excel)

    log_sucesso(MSG_RELATORIO_GERADO_SUCESSO)
    log_sucesso(
        MSG_CAMINHO_RELATORIO.format(
            caminho=caminho_relatorio
        )
    )

    log_sucesso(
        MSG_CAMINHO_RELATORIO.format(
            caminho=caminho_excel
        )
    )

    return caminho_relatorio