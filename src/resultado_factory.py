def criar_resultado(
    documento,
    status,
    mensagem,
    caminho_pdf=None,
    caminho_evidencia=None,
):
    return {
        "documento": documento,
        "status": status,
        "mensagem": mensagem,
        "caminho_pdf": caminho_pdf,
        "caminho_evidencia": caminho_evidencia,
    }