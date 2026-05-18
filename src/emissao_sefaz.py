import asyncio
import nodriver as uc

from src.pdf_service import mover_pdf_mais_recente
from src.relatorio import gerar_relatorio_emissao

URL_SEFAZ = "https://cdwfazenda.paas.pr.gov.br/cdwportal/certidao/automatica"


async def aceitar_cookies(page):

    try:
        botao_cookies = await page.find("Aceitar tudo", best_match=True)

        await botao_cookies.click()

        await page.sleep(2)

        print("Cookies aceitos com sucesso!")

    except Exception:
        print("Banner de cookies não encontrado ou já aceito.")


async def preencher_documento(page, documento):

    campo_documento = await page.select(
        'input[aria-label="CPF ou CNPJ do requerente"]'
    )

    await campo_documento.send_keys(documento)

    await page.sleep(1)

    print("Documento preenchido com sucesso!")


async def clicar_botao_emitir(page):

    botao_emitir = await page.select(
        'button[type="submit"]'
    )

    await botao_emitir.click()

    await page.sleep(5)

    print("Botão emitir clicado com sucesso!")


async def abrir_pagina_sefaz():

    browser = await uc.start()

    page = await browser.get(URL_SEFAZ)

    await page.sleep(5)

    documento = "13316414000176"

    await aceitar_cookies(page)

    await preencher_documento(page, documento)

    await clicar_botao_emitir(page)

    print("URL após emitir: ", page.url)

    resultado = await verificar_resultado_emissao(page)

    print("Resultado da emissão: ")
    print(resultado)

    caminho_pdf = None

    if resultado["status"] == "sucesso":
        
        await baixar_pdf(page)

        caminho_pdf = mover_pdf_mais_recente(documento)

    registro = {
        "documento": documento,
        "status": resultado["status"],
        "mensagem": resultado["mensagem"],
        "caminho_pdf": caminho_pdf
    }

    gerar_relatorio_emissao([registro])

    print("Página da SEFAZ aberta com sucesso!")

    print ("URL atual: ", page.url)

    browser.stop()

async def verificar_resultado_emissao(page):

    conteudo_pagina = await page.evaluate(
        "document.body.innerText"
    )

    print("DEBUG TEXTO DA PÁGINA:")
    print(conteudo_pagina)
    
    if "CPF inválido" in conteudo_pagina:
        return {
            "status": "documento_invalido",
            "mensagem": "CPF inválido informado."
        }
    
    if "CNPJ inválido" in conteudo_pagina:
        return {
            "status": "documento_invalido",
            "mensagem": "CNPJ inválido informado."
        }
    
    if "Certidões recentes emitidas para o requerente" in conteudo_pagina:
        return {
            "status": "sucesso",
            "mensagem": "Certidão encontrada para o documento informado."
        }
    
    return {
        "status": "resultado_indefinido",
        "mensagem": "Não foi possível identificar o resultado da emissão."
    }

async def baixar_pdf(page):

    await page.sleep(3)

    botoes = await page.select_all("button")

    for botao in botoes:
        texto = botao.text

        if texto and "file_save" in texto:
            await botao.click()

            await page.sleep(5)

            print("Download do PDF iniciado com sucesso!")

            return

    print("Botão de baixar PDF não encontrado.")

if __name__ == "__main__":
    asyncio.run(abrir_pagina_sefaz())
