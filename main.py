import asyncio
import os

from src.menu_service import exibir_menu
from src.utils import criar_pastas_necessarias, log_sucesso, log_erro
from src.emissao_service import (
    emitir_manual,
    emitir_por_planilha,
    consultar_historico
)

async def main():

    criar_pastas_necessarias()

    while True:

        opcao = exibir_menu()

        if opcao == "1":

            await emitir_manual()

        elif opcao == "2":

            await emitir_por_planilha()

        elif opcao == "3":

            consultar_historico()

        elif opcao == "4":

            os.startfile("certidoes_emitidas")

        elif opcao == "5":

            os.startfile("relatorios")

        elif opcao == "6":

            os.startfile("evidencias")

        elif opcao == "7":

            log_sucesso("Sistema encerrado.")
            break

        else:

            log_erro("Opção inválida.")

if __name__ == "__main__":
    asyncio.run(main())
