import asyncio
import nodriver as uc

from src.pdf_service import mover_pdf_mais_recente
from src.evidencia_service import salvar_evidencia
from src.utils import log_info, log_sucesso, log_alerta, log_erro

URL_SEFAZ = "https://cdwfazenda.paas.pr.gov.br/cdwportal/certidao/automatica"


async def aceitar_cookies(page):

    try:
        botao_cookies = await page.find("Aceitar tudo", best_match=True)

        await botao_cookies.click()

        await page.sleep(2)

        log_sucesso("Cookies aceitos com sucesso!")

    except Exception:
        log_alerta("Banner de cookies não encontrado ou já aceito.")


async def preencher_documento(page, documento):

    campo_documento = await page.select('input[aria-label="CPF ou CNPJ do requerente"]')

    await campo_documento.send_keys(documento)

    await page.sleep(1)

    log_sucesso("Documento preenchido com sucesso!")


async def clicar_botao_emitir(page):

    botao_emitir = await page.select('button[type="submit"]')

    await botao_emitir.click()

    await page.sleep(5)

    log_sucesso("Botão emitir clicado com sucesso!")


async def abrir_pagina_sefaz(documento):

    browser = await uc.start()

    page = await browser.get(URL_SEFAZ)

    await page.sleep(5)

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

    if resultado["status"] == "sucesso":

        await baixar_pdf(page)

        try:

            browser.stop()

        except Exception:
            pass

        await asyncio.sleep(3)

        caminho_pdf = mover_pdf_mais_recente(documento)

        browser = None

    registro = {
        "documento": documento,
        "status": resultado["status"],
        "mensagem": resultado["mensagem"],
        "caminho_pdf": caminho_pdf,
        "caminho_evidencia": caminho_evidencia,
    }

    log_sucesso("Página da SEFAZ aberta com sucesso!")

    log_info(f"URL atual: {page.url}")

    if browser:

        try:

            browser.stop()

        except Exception:

            pass

    return registro


async def verificar_resultado_emissao(page):

    conteudo_pagina = await page.evaluate("document.body.innerText")

    print("DEBUG TEXTO DA PÁGINA:")
    print(conteudo_pagina)

    if "CPF inválido" in conteudo_pagina:
        return {"status": "documento_invalido", "mensagem": "CPF inválido informado."}

    if "CNPJ inválido" in conteudo_pagina:
        return {"status": "documento_invalido", "mensagem": "CNPJ inválido informado."}

    if "Certidões recentes emitidas para o requerente" in conteudo_pagina:
        return {
            "status": "sucesso",
            "mensagem": "Certidão encontrada para o documento informado.",
        }
    
    if "seu computador ou rede pode estar enviando consultas automatizadas" in conteudo_pagina.lower():
        return {
            "status": "bloqueio_automacao",
            "mensagem": "A SEFAZ identificou possível automação ou excesso de consultas."
        }

    return {
        "status": "resultado_indefinido",
        "mensagem": "Não foi possível identificar o resultado da emissão.",
    }


async def baixar_pdf(page):

    await page.sleep(3)

    botoes = await page.select_all("button")

    for botao in botoes:
        texto = botao.text

        if texto and "file_save" in texto:
            await botao.click()

            log_sucesso("Download do PDF iniciado com sucesso!")

            await page.sleep(15)

            return

    log_alerta("Botão de baixar PDF não encontrado.")


if __name__ == "__main__":
    documento = input("Informe o CPF ou CNPJ: ")
    asyncio.run(abrir_pagina_sefaz(documento))
