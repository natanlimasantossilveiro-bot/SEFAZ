import asyncio
import os

from src.menu_service import exibir_menu
from src.utils import criar_pastas_necessarias, log_sucesso, log_erro
from src.emissao_service import (
    emitir_manual,
    emitir_por_planilha,
)

from src.historico_view_service import consultar_historico

from src.paths import (
    PASTA_CERTIDOES_EMITIDAS,
    PASTA_RELATORIOS,
    PASTA_EVIDENCIAS,
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

            os.startfile(PASTA_CERTIDOES_EMITIDAS)

        elif opcao == "5":

            os.startfile(PASTA_RELATORIOS)

        elif opcao == "6":

            os.startfile(PASTA_EVIDENCIAS)

        elif opcao == "7":

            log_sucesso("Sistema encerrado.")
            break

        else:

            log_erro("Opção inválida.")

if __name__ == "__main__":
    asyncio.run(main())
