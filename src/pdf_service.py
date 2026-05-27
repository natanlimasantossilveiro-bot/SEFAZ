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
)

PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

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

    for tentativa in range(1, 11):
        try:
            shutil.move(pdf_mais_recente, destino)
            break

        except PermissionError:
            log_alerta(f"PDF ainda está em uso. Tentativa {tentativa}/10...")
            time.sleep(1)

    else:
        raise PermissionError(
            f"Não foi possível mover o PDF após várias tentativas: {pdf_mais_recente}"
        )

    log_sucesso(MSG_PDF_MOVIDO_SUCESSO)

    log_sucesso(f"Destino: {destino}")

    return destino
