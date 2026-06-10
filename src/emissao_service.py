import asyncio
import random

from src.emissao_sefaz import abrir_pagina_sefaz
from src.leitor_planilha import ler_documentos_planilha
from src.relatorio import gerar_relatorio_emissao
from src.historico_service import salvar_historico

from src.config import (
    TIMEOUT_EMISSAO,
    TEMPO_ESPERA_MINIMO,
    TEMPO_ESPERA_MAXIMO,
    TEMPO_RETRY_MINIMO,
    TEMPO_RETRY_MAXIMO,
    TEMPO_PAUSA_BLOQUEIO,
    TOTAL_TENTATIVAS_EMISSAO,
)

from src.utils import (
    limpar_documento,
    validar_documento,
    log_info,
    log_alerta,
)

from src.status import (
    STATUS_BLOQUEIO_AUTOMACAO,
    STATUS_DOCUMENTO_INVALIDO,
    STATUS_ERRO_EXECUCAO,
)

from src.mensagens import (
    MSG_DOCUMENTO_INVALIDO_NAO_INICIADO,
    MSG_DOCUMENTO_INVALIDO_IGNORADO,
    MSG_BLOQUEIO_DETECTADO_RETRY,
    MSG_BLOQUEIO_DETECTADO_LOTE,
    MSG_BLOQUEIO_CONSULTAS,
    MSG_RECOMENDACAO_AGUARDAR,
    MSG_DOCUMENTO_INVALIDO_MANUAL,
    MSG_DOCUMENTO_INVALIDO_PLANILHA,
    MSG_AGUARDANDO_RETRY,
    MSG_AGUARDANDO_PROXIMA_EMISSAO,
    MSG_PAUSA_BLOQUEIO,
    MSG_GERANDO_RELATORIO_CONSOLIDADO,
    MSG_TITULO_DOCUMENTOS_ENCONTRADOS,
    MSG_TENTATIVA_EMISSAO_DOCUMENTO,
    MSG_FALHA_APOS_TENTATIVAS,
    MSG_ERRO_TENTATIVA_EMISSAO,
    MSG_PROCESSANDO_DOCUMENTO,
)

from src.paths import ARQUIVO_PLANILHA_DOCUMENTOS

from src.resultado_factory import criar_resultado

from src.exception_service import tratar_erro_padrao

from src.terminal_service import (
    exibir_titulo,
    exibir_mensagem,
)


async def emitir_com_retry(
    documento,
    total_tentativas=TOTAL_TENTATIVAS_EMISSAO,
):

    for tentativa in range(1, total_tentativas + 1):

        try:
            log_info(
                MSG_TENTATIVA_EMISSAO_DOCUMENTO.format(
                    tentativa=tentativa,
                    total_tentativas=total_tentativas,
                    documento=documento,
                )
            )

            resultado = await asyncio.wait_for(
                abrir_pagina_sefaz(documento),
                timeout=TIMEOUT_EMISSAO,
            )

            if resultado["status"] == STATUS_BLOQUEIO_AUTOMACAO:
                log_alerta(MSG_BLOQUEIO_DETECTADO_RETRY)

            return resultado

        except Exception as erro:
            tratar_erro_padrao(
                erro,
                contexto=MSG_ERRO_TENTATIVA_EMISSAO.format(
                    tentativa=tentativa,
                    documento=documento,
                ),
            )

            if tentativa < total_tentativas:
                tempo_espera = random.randint(TEMPO_RETRY_MINIMO, TEMPO_RETRY_MAXIMO)

                log_alerta(MSG_AGUARDANDO_RETRY.format(tempo=tempo_espera))

                await asyncio.sleep(tempo_espera)

    return criar_resultado(
        documento=documento,
        status=STATUS_ERRO_EXECUCAO,
        mensagem=MSG_FALHA_APOS_TENTATIVAS.format(
            total_tentativas=total_tentativas,
        ),
    )


async def emitir_por_planilha():

    documentos = ler_documentos_planilha(ARQUIVO_PLANILHA_DOCUMENTOS)

    exibir_titulo(MSG_TITULO_DOCUMENTOS_ENCONTRADOS)

    registros = []

    for item in documentos:

        exibir_mensagem(MSG_PROCESSANDO_DOCUMENTO.format(documento=item["documento"]))

        if not item["valido"]:

            log_alerta(MSG_DOCUMENTO_INVALIDO_IGNORADO)

            registros.append(
                criar_resultado(
                    documento=item["documento"],
                    status=STATUS_DOCUMENTO_INVALIDO,
                    mensagem=MSG_DOCUMENTO_INVALIDO_PLANILHA,
                )
            )

            continue

        resultado = await emitir_com_retry(item["documento"])

        registros.append(resultado)

        if resultado["status"] == STATUS_BLOQUEIO_AUTOMACAO:

            log_alerta(MSG_BLOQUEIO_DETECTADO_LOTE)
            log_alerta(MSG_RECOMENDACAO_AGUARDAR)

            break

        tempo_espera = random.randint(TEMPO_ESPERA_MINIMO, TEMPO_ESPERA_MAXIMO)

        log_info(MSG_AGUARDANDO_PROXIMA_EMISSAO.format(tempo=tempo_espera))

        await asyncio.sleep(tempo_espera)

    log_info(MSG_GERANDO_RELATORIO_CONSOLIDADO)

    gerar_relatorio_emissao(registros)

    salvar_historico(registros)

    return registros


async def emitir_documento_manual(documento):

    documento = limpar_documento(documento)

    if not validar_documento(documento):
        log_alerta(MSG_DOCUMENTO_INVALIDO_NAO_INICIADO)

        resultado = criar_resultado(
            documento=documento,
            status=STATUS_DOCUMENTO_INVALIDO,
            mensagem=MSG_DOCUMENTO_INVALIDO_MANUAL,
        )

        gerar_relatorio_emissao([resultado])

        salvar_historico([resultado])

        return resultado

    resultado = await emitir_com_retry(documento)

    if resultado["status"] == STATUS_BLOQUEIO_AUTOMACAO:
        log_alerta(MSG_BLOQUEIO_DETECTADO_RETRY)
        return resultado
    
    return resultado

    gerar_relatorio_emissao([resultado])

    salvar_historico([resultado])

    return resultado
