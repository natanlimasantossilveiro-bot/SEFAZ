import os

from src.utils import agora_para_nome_arquivo

from src.paths import PASTA_EVIDENCIAS

from src.mensagens import MSG_EVIDENCIA_SALVA_SUCESSO

async def salvar_evidencia(page, documento, status):
    nome_arquivo = f"SEFAZ_{documento}_{status}_{agora_para_nome_arquivo()}.png"

    caminho = os.path.join(PASTA_EVIDENCIAS, nome_arquivo)

    await page.save_screenshot(caminho)

    print(MSG_EVIDENCIA_SALVA_SUCESSO)
    print("Caminho: ", caminho)

    return caminho