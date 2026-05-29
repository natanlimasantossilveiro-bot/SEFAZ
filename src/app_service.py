import os 

from src.emissao_service import (
    emitir_manual,
    emitir_por_planilha,
)

from src.historico_view_service import consultar_historico

from src.paths import (
    PASTA_CERTIDOES_EMITIDAS,
    PASTA_RELATORIOS,
    PASTA_EVIDENCIAS,
)

async def executar_emissao_manual():
    await emitir_manual()


async def executar_emissao_por_planilha():
    await emitir_por_planilha()


def executar_consulta_historico():
    consultar_historico()

def abrir_pasta_certidoes():
    os.startfile(PASTA_CERTIDOES_EMITIDAS)

def abrir_pasta_relatorios():
    os.startfile(PASTA_RELATORIOS)

def abrir_pasta_evidencias():
    os.startfile(PASTA_EVIDENCIAS)