from src.utils import log_erro


def tratar_erro_padrao(erro, contexto="Operação"):
    mensagem = f"{contexto} falhou: {erro}"

    log_erro(mensagem)
    
    return mensagem