def entrada_eh_numero(texto):
    return texto.strip().isdigit()


def entrada_confirmada(texto):
    return texto.strip().lower() == "s"