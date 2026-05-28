import asyncio
import nodriver as uc
import random

from src.pdf_service import mover_pdf_mais_recente
from src.evidencia_service import salvar_evidencia
from src.utils import log_info, log_sucesso, log_alerta, log_debug

from src.config import (
    URL_SEFAZ,
    TEMPO_CARREGAMENTO_PAGINA,
    TEMPO_APOS_COOKIES,
    TEMPO_APOS_PREENCHER_DOCUMENTO,
    TEMPO_APOS_CLICAR_EMITIR,
    TEMPO_ANTES_BAIXAR_PDF,
    TEMPO_AGUARDAR_DOWNLOAD_PDF,
    TEMPO_APOS_FECHAR_BROWSER,
    TEMPO_ANTES_DIGITAR_MINIMO,
    TEMPO_ANTES_DIGITAR_MAXIMO,
    TEMPO_ENTRE_TECLAS_MINIMO,
    TEMPO_ENTRE_TECLAS_MAXIMO,
)

from src.status import (
    STATUS_SUCESSO,
    STATUS_DOCUMENTO_INVALIDO,
    STATUS_BLOQUEIO_AUTOMACAO,
    STATUS_RESULTADO_INDEFINIDO,
    STATUS_ERRO_INESPERADO,
)

from src.mensagens import (
    MSG_ERRO_INESPERADO_EMISSAO,
    MSG_RESULTADO_INDEFINIDO,
    MSG_CERTIDAO_ENCONTRADA,
    MSG_BLOQUEIO_CONSULTAS,
)

from src.resultado_factory import criar_resultado

from src.exception_service import tratar_erro_padrao


async def aceitar_cookies(page):

    try:
        botao_cookies = await page.find("Aceitar tudo", best_match=True)

        await botao_cookies.click()

        await page.sleep(TEMPO_APOS_COOKIES)

        log_sucesso("Cookies aceitos com sucesso!")

    except Exception:
        log_alerta("Banner de cookies não encontrado ou já aceito.")


async def preencher_documento(page, documento):

    campo_documento = await page.select('input[aria-label="CPF ou CNPJ do requerente"]')

    await page.sleep(
        random.uniform(TEMPO_ANTES_DIGITAR_MINIMO, TEMPO_ANTES_DIGITAR_MAXIMO)
    )

    for caractere in documento:
        await campo_documento.send_keys(caractere)
        await page.sleep(
            random.uniform(TEMPO_ENTRE_TECLAS_MINIMO, TEMPO_ENTRE_TECLAS_MAXIMO)
        )

    await page.sleep(TEMPO_APOS_PREENCHER_DOCUMENTO)

    log_sucesso("Documento preenchido com sucesso!")


async def clicar_botao_emitir(page):

    botao_emitir = await page.select('button[type="submit"]')

    await botao_emitir.click()

    await page.sleep(TEMPO_APOS_CLICAR_EMITIR)

    log_sucesso("Botão emitir clicado com sucesso!")


async def abrir_pagina_sefaz(documento):

    browser = None
    page = None
    
    try:
        browser = await uc.start()

        page = await browser.get(URL_SEFAZ)

        await page.sleep(TEMPO_CARREGAMENTO_PAGINA)

        await aceitar_cookies(page)

        await preencher_documento(page, documento)

        await clicar_botao_emitir(page)

        log_info(f"URL após emitir: {page.url}")

        resultado = await verificar_resultado_emissao(page)

        caminho_evidencia = await salvar_evidencia(
            page,
            documento,
            resultado["status"]
        )

        log_info(f"Resultado da emissão: {resultado}")

        caminho_pdf = None
        
        if resultado["status"] == STATUS_SUCESSO:

            await baixar_pdf(page)

            fechar_browser(browser)

            await asyncio.sleep(TEMPO_APOS_FECHAR_BROWSER)

            caminho_pdf = mover_pdf_mais_recente(documento)

            browser = None

        registro = criar_resultado(
            documento=documento,
            status=resultado["status"],
            mensagem=resultado["mensagem"],
            caminho_pdf=caminho_pdf,
            caminho_evidencia=caminho_evidencia,
        )

        log_sucesso("Página da SEFAZ processada com sucesso!")

        if page:
            log_info(f"URL atual: {page.url}")

        return registro
    
    except Exception as erro:
        
        tratar_erro_padrao(
            erro,
            contexto="Erro inesperado durante a emissão na SEFAZ"
        )

        return criar_resultado(
            documento=documento,
            status=STATUS_ERRO_INESPERADO,
            mensagem=MSG_ERRO_INESPERADO_EMISSAO,
        )
    
    finally:
        if browser:
            fechar_browser(browser)


def fechar_browser(browser):

    try:
        browser.stop()

    except Exception:
        pass


async def verificar_resultado_emissao(page):

    conteudo_pagina = await page.evaluate("document.body.innerText")

    log_debug("DEBUG TEXTO DA PÁGINA:")
    log_debug(conteudo_pagina)

    if "CPF inválido" in conteudo_pagina:
        return {"status": STATUS_DOCUMENTO_INVALIDO, "mensagem": "CPF inválido informado."}

    if "CNPJ inválido" in conteudo_pagina:
        return {"status": STATUS_DOCUMENTO_INVALIDO, "mensagem": "CNPJ inválido informado."}

    if "Certidões recentes emitidas para o requerente" in conteudo_pagina:
        return {
            "status": STATUS_SUCESSO,
            "mensagem": MSG_CERTIDAO_ENCONTRADA,
        }
    
    if (
        "consultas automatizadas" in conteudo_pagina.lower()
        or "não podemos processar sua solicitação" in conteudo_pagina.lower()
    ):
        
        return {
            "status": STATUS_BLOQUEIO_AUTOMACAO,
            "mensagem": MSG_BLOQUEIO_CONSULTAS
        }

    return {
        "status": STATUS_RESULTADO_INDEFINIDO,
        "mensagem": MSG_RESULTADO_INDEFINIDO,
    }


async def baixar_pdf(page):

    await page.sleep(TEMPO_ANTES_BAIXAR_PDF)

    botoes = await page.select_all("button")

    for botao in botoes:
        texto = botao.text

        if texto and "file_save" in texto:
            await botao.click()

            log_sucesso("Download do PDF iniciado com sucesso!")

            await page.sleep(TEMPO_AGUARDAR_DOWNLOAD_PDF)

            return

    log_alerta("Botão de baixar PDF não encontrado.")


if __name__ == "__main__":
    documento = input("Informe o CPF ou CNPJ: ")
    asyncio.run(abrir_pagina_sefaz(documento))
