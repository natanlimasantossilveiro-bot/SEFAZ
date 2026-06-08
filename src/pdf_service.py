import os
import shutil
import time

from src.utils import (
    agora_para_nome_arquivo,
    log_alerta,
    log_sucesso,
)

from src.paths import PASTA_CERTIDOES_EMITIDAS

from src.mensagens import (
    MSG_PDF_NAO_ENCONTRADO,
    MSG_PDF_MOVIDO_SUCESSO,
    MSG_PDF_NAO_DISPONIVEL_TENTATIVA,
    MSG_PDF_AINDA_BAIXANDO_TENTATIVA,
    MSG_PDF_EM_USO_TENTATIVA,
    MSG_DESTINO_ARQUIVO,
    MSG_PDF_COPIADO_FALLBACK_SUCESSO,
    MSG_PDF_COPIADO_SUCESSO,
    MSG_PDF_FALHA_MOVE_E_COPIA,
)

from src.config import (
    TOTAL_TENTATIVAS_PDF,
    TEMPO_ESPERA_PDF,
)

PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")


def arquivo_esta_pronto(caminho_arquivo):
    tamanho_inicial = os.path.getsize(caminho_arquivo)
    time.sleep(TEMPO_ESPERA_PDF)
    tamanho_final = os.path.getsize(caminho_arquivo)

    return tamanho_inicial == tamanho_final


def mover_pdf_mais_recente(documento):

    arquivos_pdf = [
        arquivo
        for arquivo in os.listdir(PASTA_DOWNLOADS)
        if arquivo.lower().endswith(".pdf")
    ]

    if not arquivos_pdf:
        log_alerta(MSG_PDF_NAO_ENCONTRADO)
        return None

    caminhos_completos = [
        os.path.join(PASTA_DOWNLOADS, arquivo) for arquivo in arquivos_pdf
    ]

    pdf_mais_recente = max(caminhos_completos, key=os.path.getctime)

    nome_novo = f"SEFAZ_{documento}_{agora_para_nome_arquivo()}.pdf"

    destino = os.path.join(PASTA_CERTIDOES_EMITIDAS, nome_novo)

    pdf_foi_copiado = False

    for tentativa in range(1, TOTAL_TENTATIVAS_PDF + 1):
        try:
            if not os.path.exists(pdf_mais_recente):
                log_alerta(
                    MSG_PDF_NAO_DISPONIVEL_TENTATIVA.format(
                        tentativa=tentativa, total=TOTAL_TENTATIVAS_PDF
                    )
                )
                time.sleep(TEMPO_ESPERA_PDF)
                continue

            if not arquivo_esta_pronto(pdf_mais_recente):
                log_alerta(
                    MSG_PDF_AINDA_BAIXANDO_TENTATIVA.format(
                        tentativa=tentativa, total=TOTAL_TENTATIVAS_PDF
                    )
                )
                time.sleep(TEMPO_ESPERA_PDF)
                continue

            shutil.move(pdf_mais_recente, destino)
            break

        except PermissionError:
            log_alerta(
                MSG_PDF_EM_USO_TENTATIVA.format(
                    tentativa=tentativa, total=TOTAL_TENTATIVAS_PDF
                )
            )
            time.sleep(TEMPO_ESPERA_PDF)

    else:
        try:
            shutil.copy2(pdf_mais_recente, destino)
            pdf_foi_copiado = True
            log_alerta(MSG_PDF_COPIADO_FALLBACK_SUCESSO)
        except PermissionError:
            raise PermissionError(
                MSG_PDF_FALHA_MOVE_E_COPIA.format(pdf=pdf_mais_recente)
            )

    if pdf_foi_copiado:
        log_sucesso(MSG_PDF_COPIADO_SUCESSO)
    else:
        log_sucesso(MSG_PDF_MOVIDO_SUCESSO)

    log_sucesso(MSG_DESTINO_ARQUIVO.format(destino=destino))

    return destino
