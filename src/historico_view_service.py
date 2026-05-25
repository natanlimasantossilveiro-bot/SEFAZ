from src.historico_service import (
    listar_historico,
    filtrar_historico_por_documento,
    exportar_historico_filtrado,
    gerar_estatisticas_historico,
)

def exibir_registros_historico(registros):
    for registro in registros:
        print(
            f"\n{registro['data_hora']} | "
            f"{registro['documento']} | "
            f"{registro['status']} | "
            f"{registro['mensagem']}"
        )

        if registro.get("caminho_pdf"):
            print(f"PDF: {registro['caminho_pdf']}")

        if registro.get("caminho_evidencia"):
            print(f"Evidência: {registro['caminho_evidencia']}")

def consultar_historico():

    historico = listar_historico()

    print("\n=== HISTÓRICO DE EMISSÕES ===\n")

    if not historico:
        print("Nenhum registro encontrado.")
        return
    
    filtro_documento = input(
        "Filtrar por CPF/CNPJ (ENTER para todos): "
    )

    if filtro_documento.strip():
        historico = filtrar_historico_por_documento(filtro_documento)

    estatisticas = gerar_estatisticas_historico(historico)

    print("\n=== Resumo ===")
    print(f"Total de registros: {estatisticas['total']}")
    print(f"Sucessos: {estatisticas['sucesso']}")
    print(f"Erros de execução: {estatisticas['erro_execucao']}")
    print(f"Bloqueios: {estatisticas['bloqueio_automacao']}")
    print(f"Documentos inválidos: {estatisticas['documento_invalido']}")
    print(f"Resultados indefinidos: {estatisticas['resultado_indefinido']}")

    quantidade_texto = input(
        "\nQuantos registros deseja visualizar? (padrão 10): "
    )

    quantidade = 10
    
    if quantidade_texto.strip().isdigit():
        quantidade = int(quantidade_texto)

    exibir_registros_historico(historico[-quantidade:])

    exportar = input(
        "\nDeseja exportar este histórico para CSV? (s/n): "
    )

    if exportar.strip().lower() == "s":
        exportar_historico_filtrado(historico[-quantidade:])