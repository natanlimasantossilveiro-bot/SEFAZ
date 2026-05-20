import os
import re

from datetime import datetime

DEBUG = True

def agora_formatado():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def agora_para_nome_arquivo():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def limpar_documento(documento):
    return re.sub(r"\D", "", str(documento))


def identificar_tipo_documento(documento):
    documento_limpo = limpar_documento(documento)

    if len(documento_limpo) == 11:
        return "CPF"

    if len(documento_limpo) == 14:
        return "CNPJ"

    return "INVÁLIDO"


def validar_documento(documento):
    tipo = identificar_tipo_documento(documento)

    if tipo == "CPF":
        return True

    if tipo == "CNPJ":
        return True

    return False


def criar_pastas_necessarias():
    pastas = [
        "downloads",
        "certidoes_emitidas",
        "evidencias",
        "historico",
        "relatorios",
        "uploads"
    ]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)


def log_info(mensagem):
    print(f"[INFO] {mensagem}")


def log_sucesso(mensagem):
    print(f"[SUCESSO] {mensagem}")


def log_erro(mensagem):
    print(f"[ERRO] {mensagem}")


def log_alerta(mensagem):
    print(f"[ALERTA] {mensagem}")


def log_debug(mensagem):
    if DEBUG:
        print(f"[DEBUG] {mensagem}")