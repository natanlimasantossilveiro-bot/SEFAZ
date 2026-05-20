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
    print("5- Abrir pasta de relatórios")
    print("6- Abrir pasta de evidências")
    print("7- Sair")

    return input("\nEscolha uma opção:")

async def emitir_com_retry(documento, total_tentativas=3):

    for tentativa in range(1, total_tentativas + 1):

        try:
            print(f"Tentativa {tentativa}/{total_tentativas} para o documento {documento}")

            resultado = await asyncio.wait_for(
                abrir_pagina_sefaz(documento),
                timeout=60
            )

            return resultado
        
        except Exception as erro:
            print(f"Erro na tentativa {tentativa} para o documento {documento}: {erro}")

            if tentativa < total_tentativas:
                tempo_espera = random.randint(10, 20)

                print(f"Aguardando {tempo_espera} segundos antes de tentar novamente...")

                await asyncio.sleep(tempo_espera)

    return {
        "documento": documento,
        "status": "erro_execucao",
        "mensagem": f"Falha após {total_tentativas} tentativas.",
        "caminho_pdf": None,
        "caminho_evidencia": None,
    }

async def main():

    criar_pastas_necessarias()

    while True:

        opcao = exibir_menu()

        if opcao == "1":

            documento = input("Informe o CPF ou CNPJ: ")

            resultado = await emitir_com_retry(documento)

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

                resultado = await emitir_com_retry(item["documento"])

                registros.append(resultado)

                tempo_espera = random.randint(8, 15)

                print(f"Aguardando {tempo_espera} segundos antes da próxima emissão...")

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

            os.startfile("relatorios")

        elif opcao == "6":

            os.startfile("evidencias")

        elif opcao == "7":

            print("Sistema encerrado.")
            break

        else:

            print("Opção inválida.")

if __name__ == "__main__":
    asyncio.run(main())
