import asyncio


from src.app_service import (
    executar_emissao_manual,
    executar_emissao_por_planilha,
    executar_consulta_historico,
    abrir_pasta_certidoes,
    abrir_pasta_relatorios,
    abrir_pasta_evidencias,
    abrir_pasta_logs,
)

from src.menu_service import exibir_menu

from src.utils import criar_pastas_necessarias, log_sucesso, log_erro

from src.mensagens import (
    MSG_SISTEMA_ENCERRADO,
    MSG_OPCAO_INVALIDA,
)

from src.input_validator import opcao_esta_no_intervalo

from src.menu_options import OPCOES_VALIDAS_MENU

async def main():

    criar_pastas_necessarias()

    while True:

        opcao = exibir_menu()

        if not opcao_esta_no_intervalo(opcao, OPCOES_VALIDAS_MENU):
            log_erro(MSG_OPCAO_INVALIDA)
            continue

        if opcao == "1":

            await executar_emissao_manual()

        elif opcao == "2":

            await executar_emissao_por_planilha()

        elif opcao == "3":

            executar_consulta_historico()

        elif opcao == "4":

            abrir_pasta_certidoes()

        elif opcao == "5":

            abrir_pasta_relatorios()

        elif opcao == "6":

            abrir_pasta_evidencias()

        elif opcao == "7":

            abrir_pasta_logs()

        elif opcao == "8":

            log_sucesso(MSG_SISTEMA_ENCERRADO)
            break

if __name__ == "__main__":
    asyncio.run(main())
