def entrada_eh_numero(texto):
    return texto.strip().isdigit()


def entrada_confirmada(texto):
    return texto.strip().lower() == "s"


def opcao_esta_no_intervalo(opcao, opcoes_validas):
    return opcao.strip() in opcoes_validas