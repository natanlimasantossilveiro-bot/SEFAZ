import csv
import os

from src.utils import (
    agora_formatado,
    limpar_documento,
    log_info,
    log_sucesso,
)

from src.paths import PASTA_HISTORICO, PASTA_RELATORIOS

from src.status import (
    STATUS_SUCESSO,
    STATUS_ERRO_EXECUCAO,
    STATUS_BLOQUEIO_AUTOMACAO,
    STATUS_DOCUMENTO_INVALIDO,
    STATUS_RESULTADO_INDEFINIDO,
)

from src.mensagens import (
    MSG_HISTORICO_ATUALIZADO_SUCESSO,
    MSG_HISTORICO_NAO_ENCONTRADO,
    MSG_HISTORICO_EXPORTADO_SUCESSO,
    MSG_CAMINHO_RELATORIO,
)

CAMINHO_HISTORICO = os.path.join(PASTA_HISTORICO, "historico_emissoes.csv")


def salvar_historico(registros):
    os.makedirs(PASTA_HISTORICO, exist_ok=True)

    colunas = [
        "data_hora",
        "documento",
        "status",
        "mensagem",
        "caminho_pdf",
        "caminho_evidencia",
    ]

    arquivo_existe = os.path.exists(CAMINHO_HISTORICO)

    with open(CAMINHO_HISTORICO, "a", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=colunas,
            delimiter=";",
        )

        if not arquivo_existe:
            escritor.writeheader()

        for registro in registros:
            linha = {
                "data_hora": agora_formatado(),
                "documento": registro.get("documento"),
                "status": registro.get("status"),
                "mensagem": registro.get("mensagem"),
                "caminho_pdf": registro.get("caminho_pdf"),
                "caminho_evidencia": registro.get("caminho_evidencia"),
            }

            escritor.writerow(linha)

    log_sucesso(MSG_HISTORICO_ATUALIZADO_SUCESSO)


def listar_historico():
    if not os.path.exists(CAMINHO_HISTORICO):
        log_info(MSG_HISTORICO_NAO_ENCONTRADO)
        return []
    
    registros = []
    
    with open(CAMINHO_HISTORICO, "r", newline="", encoding="utf-8-sig") as arquivo_csv:
        leitor = csv.DictReader(
            arquivo_csv,
            delimiter=";",
        )

        for linha in leitor:
            registros.append(linha)

    return registros


def filtrar_historico_por_documento(documento):
    documento_limpo = limpar_documento(documento)

    historico = listar_historico()

    registros_filtrados = []

    for registro in historico:
        if registro["documento"] == documento_limpo:
            registros_filtrados.append(registro)

    return registros_filtrados


def exportar_historico_filtrado(registros):
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    data_nome_arquivo = agora_formatado().replace(":", "-").replace(" ", "_")
    nome_arquivo = f"historico_filtrado_{data_nome_arquivo}.csv"

    caminho_relatorio = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    colunas = [
        "data_hora",
        "documento",
        "status",
        "mensagem",
        "caminho_pdf",
        "caminho_evidencia",
    ]

    with open(caminho_relatorio, "w", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=colunas,
            delimiter=";",
        )

        escritor.writeheader()
        escritor.writerows(registros)

    log_sucesso(MSG_HISTORICO_EXPORTADO_SUCESSO)
    log_sucesso(MSG_CAMINHO_RELATORIO.format(caminho=caminho_relatorio))

    return caminho_relatorio


def gerar_estatisticas_historico(registros):

    estatisticas = {
        "total": len(registros),
        STATUS_SUCESSO: 0,
        STATUS_ERRO_EXECUCAO: 0,
        STATUS_BLOQUEIO_AUTOMACAO: 0,
        STATUS_DOCUMENTO_INVALIDO: 0,
        STATUS_RESULTADO_INDEFINIDO: 0,
    }

    for registro in registros:

        status = registro.get("status")

        if status in estatisticas:
            estatisticas[status] += 1

    return estatisticas