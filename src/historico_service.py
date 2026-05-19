import csv
import os

from src.utils import agora_formatado

CAMINHO_HISTORICO = os.path.join("historico", "historico_emissoes.csv")

def salvar_historico(registros):
    os.makedirs("historico", exist_ok=True)

    colunas = [
        "data_hora",
        "documento",
        "status",
        "mensagem",
        "caminho_pdf",
        "caminho_evidencia",
    ]

    arquivo_existe = os.path.exists(CAMINHO_HISTORICO)

    with open(CAMINHO_HISTORICO, "a", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=colunas,
            delimiter=";"
        )

        if not arquivo_existe:
            escritor.writeheader()

        for registro in registros:
            linha = {
                "data_hora": agora_formatado(),
                "documento": registro.get("documento"),
                "status": registro.get("status"),
                "mensagem": registro.get("mensagem"),
                "caminho_pdf": registro.get("caminho_pdf"),
                "caminho_evidencia": registro.get("caminho_evidencia"),
            }

            escritor.writerow(linha)

    print("Histórico atualizado com sucesso!")

def listar_historico():
    if not os.path.exists(CAMINHO_HISTORICO):
        print("Nenhum histórico encontrado.")
        return []
    
    registros = []
    
    with open(CAMINHO_HISTORICO, "r", newline="", encoding="utf-8-sig") as arquivo_csv:
        leitor = csv.DictReader(
            arquivo_csv,
            delimiter=";"
        )

        for linha in leitor:
            registros.append(linha)

    return registros