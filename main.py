import asyncio
import random
import os

from src.emissao_sefaz import abrir_pagina_sefaz
from src.leitor_planilha import ler_documentos_planilha
from src.relatorio import gerar_relatorio_emissao
from src.historico_service import salvar_historico, listar_historico

from src.utils import criar_pastas_necessarias

def exibir_menu():

    print("\n=== AUTOMAÇÃO SEFAZ ===")
    print("1- Emitir certidão manual")
    print("2- Emitir certidões por planilha")
    print("3- Consultar histórico")
    print("4- Abrir pasta de PDFs")
    print("5- Sair")

    return input("\nEscolha uma opção:")

async def main():

    criar_pastas_necessarias()

    while True:

        opcao = exibir_menu()

        if opcao == "1":

            documento = input("Informe o CPF ou CNPJ: ")

            resultado = await abrir_pagina_sefaz(documento)

            print("\n=== RESULTADO DA EMISSÃO ===\n")
            print(resultado)

            gerar_relatorio_emissao([resultado])

            salvar_historico([resultado])

        elif opcao == "2":

            documentos = ler_documentos_planilha("planilha_documentos.xlsx")

            print("\n=== DOCUMENTOS ENCONTRADOS ===\n")

            registros = []

            for item in documentos:

                print(f"\nProcessando documento: {item['documento']}")

                if not item["valido"]:

                    print("Documento inválido. Ignorando...")

                    registros.append(
                        {
                            "documento": item["documento"],
                            "status": "documento_invalido",
                            "mensagem": "Documento inválido na planilha.",
                            "caminho_pdf": None,
                            "caminho_evidencia": None,
                        }
                    )

                    continue

                resultado = await abrir_pagina_sefaz(item["documento"])

                registros.append(resultado)

                tempo_espera = random.randint(8, 15)

                print(
                    f"Aguardando {tempo_espera} segundos antes da próxima emissão..."
                )

                await asyncio.sleep(tempo_espera)

            print("\n=== RESULTADOS FINAIS ===\n")

            for registro in registros:
                print(registro)

            print("\nGerando relatório consolidado...")

            gerar_relatorio_emissao(registros)

            salvar_historico(registros)

        elif opcao == "3":
            
            historico = listar_historico()

            print("\n=== HISTÓRICO DE EMISSÕES ===\n")

            if not historico:
                print("Nenhum registro encontrado.")

            else:
                for registro in historico[-10:]:
                    print(
                        f"{registro['data_hora']} | "
                        f"{registro['documento']} | "
                        f"{registro['status']} | "
                        f"{registro['mensagem']}"
                    )

        elif opcao == "4":

            os.startfile("certidoes_emitidas")

        elif opcao == "5":

            print("Sistema encerrado.")
            break

        else:

            print("Opção inválida.")


if __name__ == "__main__":
    asyncio.run(main())
