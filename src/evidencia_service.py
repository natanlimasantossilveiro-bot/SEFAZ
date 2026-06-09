import os

from src.utils import (
    agora_para_nome_arquivo,
    log_sucesso,
)

from src.paths import PASTA_EVIDENCIAS

from src.mensagens import (
    MSG_EVIDENCIA_SALVA_SUCESSO,
    MSG_CAMINHO_EVIDENCIA,
)

async def salvar_evidencia(page, documento, status):
    nome_arquivo = f"SEFAZ_{documento}_{status}_{agora_para_nome_arquivo()}.png"

    caminho = os.path.join(PASTA_EVIDENCIAS, nome_arquivo)

    await page.save_screenshot(caminho)

    log_sucesso(MSG_EVIDENCIA_SALVA_SUCESSO)
    log_sucesso(
        MSG_CAMINHO_EVIDENCIA.format(caminho=caminho)
    )

    return caminho