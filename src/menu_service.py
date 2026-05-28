from src.terminal_service import (
    exibir_titulo,
    exibir_mensagem,
)

def exibir_menu():

    exibir_titulo("AUTOMAÇÃO SEFAZ")

    exibir_mensagem("1- Emitir certidão manual")
    exibir_mensagem("2- Emitir certidões por planilha")
    exibir_mensagem("3- Consultar histórico")
    exibir_mensagem("4- Abrir pasta de PDFs")
    exibir_mensagem("5- Abrir pasta de relatórios")
    exibir_mensagem("6- Abrir pasta de evidências")
    exibir_mensagem("7- Sair")

    return input("\nEscolha uma opção: ")