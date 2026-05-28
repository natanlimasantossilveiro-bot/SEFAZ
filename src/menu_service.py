from src.terminal_service import (
    exibir_titulo,
    exibir_mensagem,
    solicitar_entrada,
)

from src.mensagens import MSG_TITULO_AUTOMACAO

from src.menu_options import OPCOES_MENU
def exibir_menu():

    exibir_titulo(MSG_TITULO_AUTOMACAO)

    for codigo, descricao in OPCOES_MENU:
        exibir_mensagem(f"{codigo}- {descricao}")

    return solicitar_entrada("\nEscolha uma opção: ")