import os
import re

from datetime import datetime
from src.config import DEBUG

from src.paths import (
    PASTA_DOWNLOADS,
    PASTA_CERTIDOES_EMITIDAS,
    PASTA_EVIDENCIAS,
    PASTA_HISTORICO,
    PASTA_RELATORIOS,
    PASTA_UPLOADS,
)

from src.logger_service import (
    registrar_info,
    registrar_sucesso,
    registrar_alerta,
    registrar_erro,
)

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


def validar_cpf(cpf):
    cpf = limpar_documento(cpf)

    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10) % 11
    primeiro_digito = 0 if primeiro_digito == 10 else primeiro_digito

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10) % 11
    segundo_digito = 0 if segundo_digito == 10 else segundo_digito

    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


def validar_cnpj(cnpj):
    cnpj = limpar_documento(cnpj)

    if len(cnpj) != 14:
        return False
    
    if cnpj == cnpj[0] * 14:
        return False
    
    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_segundo = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = sum(int(cnpj[i]) * pesos_primeiro[i] for i in range(12))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto

    soma = sum(int(cnpj[i]) * pesos_segundo[i] for i in range(13))
    resto = soma % 11
    segundo_digito = 0 if resto < 2 else 11 - resto

    return cnpj[-2:] == f"{primeiro_digito}{segundo_digito}"


def validar_documento(documento):
    tipo = identificar_tipo_documento(documento)

    if tipo == "CPF":
        return validar_cpf(documento)
    
    if tipo == "CNPJ":
        return validar_cnpj(documento)
    
    return False


def criar_pastas_necessarias():
    pastas = [
        PASTA_DOWNLOADS,
        PASTA_CERTIDOES_EMITIDAS,
        PASTA_EVIDENCIAS,
        PASTA_HISTORICO,
        PASTA_RELATORIOS,
        PASTA_UPLOADS,
    ]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)


def log_info(mensagem):
    print(f"[INFO] {mensagem}")
    registrar_info(mensagem)


def log_sucesso(mensagem):
    print(f"[SUCESSO] {mensagem}")
    registrar_sucesso(mensagem)


def log_erro(mensagem):
    print(f"[ERRO] {mensagem}")
    registrar_erro(mensagem)


def log_alerta(mensagem):
    print(f"[ALERTA] {mensagem}")
    registrar_alerta(mensagem)


def log_debug(mensagem):
    if DEBUG:
        print(f"[DEBUG] {mensagem}")