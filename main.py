import asyncio

from src.emissao_sefaz import abrir_pagina_sefaz
from src.leitor_planilha import ler_documentos_planilha
from src.relatorio import gerar_relatorio_emissao

from src.utils import (
    criar_pastas_necessarias
)

def main():

    criar_pastas_necessarias()

    documentos = ler_documentos_planilha("planilha_documentos.xlsx")

    print("\n=== DOCUMENTOS ENCONTRADOS ===\n")

    registros = []

    for item in documentos:

        print(f"\nProcessando documento: {item['documento']}")

        if not item["valido"]:

            print("Documento inválido. Ignorando...")

            registros.append({
                "documento": item["documento"],
                "status": "documento_invalido",
                "mensagem": "Documento inválido na planilha.",
                "caminho_pdf": None
            })

            continue

        resultado = asyncio.run(
            abrir_pagina_sefaz(item["documento"])
        )

        registros.append(resultado)

    print("\n=== RESULTADOS FINAIS ===\n")

    for registro in registros:
        print(registro)

if __name__ == "__main__":
    main()