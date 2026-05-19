import os

from src.utils import agora_para_nome_arquivo


PASTA_EVIDENCIAS = "evidencias"


async def salvar_evidencia(page, documento, status):
    nome_arquivo = f"SEFAZ_{documento}_{status}_{agora_para_nome_arquivo()}.png"

    caminho = os.path.join(PASTA_EVIDENCIAS, nome_arquivo)

    await page.save_screenshot(caminho)

    print("Evidência salva com sucesse!")
    print("Caminho: ", caminho)

    return caminho