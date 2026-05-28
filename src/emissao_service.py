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
    MSG_TITULO_RESULTADOS_FINAIS,
    MSG_TITULO_RESULTADO_EMISSAO,
)

from src.paths import ARQUIVO_PLANILHA_DOCUMENTOS

from src.resultado_factory import criar_resultado

from src.exception_service import tratar_erro_padrao

from src.terminal_service import (
    exibir_titulo,
    exibir_mensagem,
    solicitar_entrada,
)

async def emitir_com_retry(documento, total_tentativas=3):

    for tentativa in range(1, total_tentativas + 1):

        try:
            log_info(f"Tentativa {tentativa}/{total_tentativas} para o documento {documento}")

            resultado = await asyncio.wait_for(
                abrir_pagina_sefaz(documento),
                timeout=TIMEOUT_EMISSAO
            )

            if resultado["status"] == STATUS_BLOQUEIO_AUTOMACAO:
                log_alerta(MSG_BLOQUEIO_DETECTADO_RETRY)

            return resultado
        
        except Exception as erro:
            tratar_erro_padrao(
                erro,
                contexto=f"Erro na tentativa {tentativa} para o documento {documento}"
            )

            if tentativa < total_tentativas:
                tempo_espera = random.randint(TEMPO_RETRY_MINIMO, TEMPO_RETRY_MAXIMO)

                log_alerta(MSG_AGUARDANDO_RETRY.format(tempo=tempo_espera))

                await asyncio.sleep(tempo_espera)

    return criar_resultado(
        documento=documento,
        status=STATUS_ERRO_EXECUCAO,
        mensagem=f"Falha após {total_tentativas} tentativas.",
    )
        
async def emitir_por_planilha():

    documentos = ler_documentos_planilha(ARQUIVO_PLANILHA_DOCUMENTOS)

    exibir_titulo(MSG_TITULO_DOCUMENTOS_ENCONTRADOS)

    registros = []

    for item in documentos:

        exibir_mensagem(f"\nProcessando documento: {item['documento']}")

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
            
            minutos_pausa = TEMPO_PAUSA_BLOQUEIO // 60

            log_alerta(MSG_BLOQUEIO_DETECTADO_LOTE)
            log_alerta(MSG_PAUSA_BLOQUEIO.format(minutos=minutos_pausa))

            await asyncio.sleep(TEMPO_PAUSA_BLOQUEIO)

        tempo_espera = random.randint(TEMPO_ESPERA_MINIMO, TEMPO_ESPERA_MAXIMO)

        log_info(MSG_AGUARDANDO_PROXIMA_EMISSAO.format(tempo=tempo_espera))

        await asyncio.sleep(tempo_espera)

    exibir_titulo(MSG_TITULO_RESULTADOS_FINAIS)

    for registro in registros:
        exibir_mensagem(registro)

    log_info(MSG_GERANDO_RELATORIO_CONSOLIDADO)

    gerar_relatorio_emissao(registros)

    salvar_historico(registros)

async def emitir_manual():

    documento = solicitar_entrada("Informe o CPF ou CNPJ: ")

    documento = limpar_documento(documento)

    if not validar_documento(documento):
        log_alerta(MSG_DOCUMENTO_INVALIDO_NAO_INICIADO)

        resultado = criar_resultado(
            documento=documento,
            status=STATUS_DOCUMENTO_INVALIDO,
            mensagem=MSG_DOCUMENTO_INVALIDO_MANUAL,
        )

        exibir_titulo(MSG_TITULO_RESULTADO_EMISSAO)
        exibir_mensagem(resultado)

        gerar_relatorio_emissao([resultado])

        salvar_historico([resultado])

        return
    
    resultado = await emitir_com_retry(documento)

    exibir_titulo(MSG_TITULO_RESULTADO_EMISSAO)
    exibir_mensagem(resultado)

    if resultado["status"] == STATUS_BLOQUEIO_AUTOMACAO:
        log_alerta(MSG_BLOQUEIO_CONSULTAS)
        log_alerta(MSG_RECOMENDACAO_AGUARDAR)

    gerar_relatorio_emissao([resultado])

    salvar_historico([resultado])