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
    log_info,
    log_erro,
    log_alerta,
)

async def emitir_com_retry(documento, total_tentativas=3):

    for tentativa in range(1, total_tentativas + 1):

        try:
            log_info(f"Tentativa {tentativa}/{total_tentativas} para o documento {documento}")

            resultado = await asyncio.wait_for(
                abrir_pagina_sefaz(documento),
                timeout=TIMEOUT_EMISSAO
            )

            if resultado["status"] == "bloqueio_automacao":
                log_alerta("Bloqueio detectado pela SEFAZ. A emissão não será repetida agora.")

            return resultado
        
        except Exception as erro:
            log_erro(f"Erro na tentativa {tentativa} para o documento {documento}: {erro}")

            if tentativa < total_tentativas:
                tempo_espera = random.randint(TEMPO_RETRY_MINIMO, TEMPO_RETRY_MAXIMO)

                log_alerta(f"Aguardando {tempo_espera} segundos antes de tentar novamente...")

                await asyncio.sleep(tempo_espera)

    return {
        "documento": documento,
        "status": "erro_execucao",
        "mensagem": f"Falha após {total_tentativas} tentativas.",
        "caminho_pdf": None,
        "caminho_evidencia": None,
    }
        
async def emitir_por_planilha():

    documentos = ler_documentos_planilha("planilha_documentos.xlsx")

    print("\n=== DOCUMENTOS ENCONTRADOS ===\n")

    registros = []

    for item in documentos:

        print(f"\nProcessando documento: {item['documento']}")

        if not item["valido"]:

            log_alerta("Documento inválido. Ignorando...")

            registros.append(
                {
                    "documento": item["documento"],
                    "status": "documento_invalido",
                    "mensagem": "Documento inválido na planilha.",
                    "caminho_pdf": None,
                    "caminho_evidencia": None,
                }
            )

            continue
        
        resultado = await emitir_com_retry(item["documento"])

        registros.append(resultado)

        if resultado["status"] == "bloqueio_automacao":
            
            minutos_pausa = TEMPO_PAUSA_BLOQUEIO // 60

            log_alerta("Bloqueio detectado pela SEFAZ durante o lote.")
            log_alerta(
                f"O sistema ficará pausado por aproximadamente {minutos_pausa} minutos."
            )

            await asyncio.sleep(TEMPO_PAUSA_BLOQUEIO)

        tempo_espera = random.randint(TEMPO_ESPERA_MINIMO, TEMPO_ESPERA_MAXIMO)

        log_info(f"Aguardando {tempo_espera} segundos antes da próxima emissão...")

        await asyncio.sleep(tempo_espera)

    print("\n=== RESULTADOS FINAIS ===\n")

    for registro in registros:
        print(registro)

    log_info("Gerando relatório consolidado...")

    gerar_relatorio_emissao(registros)

    salvar_historico(registros)

async def emitir_manual():

    documento = input("Informe o CPF ou CNPJ: ")

    resultado = await emitir_com_retry(documento)

    print("\n=== RESULTADO DA EMISSÃO ===\n")
    print(resultado)

    if resultado["status"] == "bloqueio_automacao":
        log_alerta("A SEFAZ bloqueou temporariamente as consultas.")
        log_alerta("Recomenda-se aguardar alguns minutos antes de tentar novamente.")

    gerar_relatorio_emissao([resultado])

    salvar_historico([resultado])