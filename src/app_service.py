import os 

from src.emissao_service import (
    emitir_documento_manual,
    emitir_por_planilha,
)

from src.historico_view_service import consultar_historico

from src.paths import (
    PASTA_CERTIDOES_EMITIDAS,
    PASTA_RELATORIOS,
    PASTA_EVIDENCIAS,
)

from src.terminal_service import solicitar_entrada

from src.mensagens import MSG_SOLICITAR_DOCUMENTO

async def executar_emissao_manual():
    
    documento = solicitar_entrada(MSG_SOLICITAR_DOCUMENTO)

    return await emitir_documento_manual(documento)


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