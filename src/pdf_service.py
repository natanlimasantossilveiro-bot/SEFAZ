import os
import shutil
from src.utils import agora_para_nome_arquivo

PASTA_DOWNLOADS = os.path.join(
    os.path.expanduser("~"),
    "Downloads"
)

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
        os.path.join(PASTA_DOWNLOADS, arquivo)
        for arquivo in arquivos_pdf
    ]

    pdf_mais_recente = max(
        caminhos_completos,
        key=os.path.getctime
    )

    nome_novo = f"SEFAZ_{documento}_{agora_para_nome_arquivo()}.pdf"

    destino = os.path.join(
        PASTA_CERTIDOES,
        nome_novo
    )

    shutil.move(pdf_mais_recente, destino)

    print("PDF movido com sucesso!")

    print("Destino: ", destino)

    return destino