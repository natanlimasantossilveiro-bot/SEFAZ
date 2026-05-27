import logging
import os

PASTA_LOGS = "logs"

os.makedirs(PASTA_LOGS, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(PASTA_LOGS, "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)


def registrar_info(mensagem):
    logging.info(mensagem)


def registrar_sucesso(mensagem):
    logging.info(f"[SUCESSO] {mensagem}")


def registrar_alerta(mensagem):
    logging.warning(mensagem)


def registrar_erro(mensagem):
    logging.error(mensagem)