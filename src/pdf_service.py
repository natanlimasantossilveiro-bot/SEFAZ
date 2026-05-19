import os
import shutil
import time

from src.utils import agora_para_nome_arquivo

PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

PASTA_CERTIDOES = "certidoes_emitidas"


def mover_pdf_mais_recente(documento):

    arquivos_pdf = [
        arquivo
        for arquivo in os.listdir(PASTA_DOWNLOADS)
        if arquivo.lower().endswith(".pdf")
    ]

    if not arquivos_pdf:
        print("Nenhum PDF encontrado na pasta Downloads.")
        return None

    caminhos_completos = [
        os.path.join(PASTA_DOWNLOADS, arquivo) for arquivo in arquivos_pdf
    ]

    pdf_mais_recente = max(caminhos_completos, key=os.path.getctime)

    nome_novo = f"SEFAZ_{documento}_{agora_para_nome_arquivo()}.pdf"

    destino = os.path.join(PASTA_CERTIDOES, nome_novo)

    for tentativa in range(1, 11):
        try:
            shutil.move(pdf_mais_recente, destino)
            break

        except PermissionError:
            print(f"PDF ainda está em uso. Tentativa {tentativa}/10...")
            time.sleep(1)

    else:
        raise PermissionError(
            f"Não foi possível mover o PDF após várias tentativas: {pdf_mais_recente}"
        )

    print("PDF movido com sucesso!")

    print("Destino: ", destino)

    return destino
