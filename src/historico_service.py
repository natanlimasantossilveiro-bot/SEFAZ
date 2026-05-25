import csv
import os

from src.utils import agora_formatado, limpar_documento

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

def filtrar_historico_por_documento(documento):
    documento_limpo = limpar_documento(documento)

    historico = listar_historico()

    registros_filtrados = []

    for registro in historico:
        if registro["documento"] == documento_limpo:
            registros_filtrados.append(registro)

    return registros_filtrados

def exportar_historico_filtrado(registros):
    os.makedirs("relatorios", exist_ok=True)

    nome_arquivo = f"historico_filtrado_{agora_formatado().replace(':', '_').replace(' ', '_')}.csv"

    caminho_relatorio = os.path.join("relatorios", nome_arquivo)

    colunas = [
        "data_hora",
        "documento",
        "status",
        "mensagem",
        "caminho_pdf",
        "caminho_evidencia",
    ]

    with open(caminho_relatorio, "w", newline="", encoding="utf-8-sig") as arquivo_csv:
        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=colunas,
            delimiter=";"
        )

        escritor.writeheader()
        escritor.writerows(registros)

    print("Histórico filtrado exportado com sucesso!")
    print("Caminho: ", caminho_relatorio)

    return caminho_relatorio

def gerar_estatisticas_historico(registros):

    estatisticas = {
        "total": len(registros),
        "sucesso": 0,
        "erro_execucao": 0,
        "bloqueio_automacao": 0,
        "documento_invalido": 0,
        "resultado_indefinido": 0,
    }

    for registro in registros:

        status = registro.get("status")

        if status in estatisticas:
            estatisticas[status] += 1

    return estatisticas