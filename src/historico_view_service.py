from src.historico_service import (
    listar_historico,
    filtrar_historico_por_documento,
    exportar_historico_filtrado,
    gerar_estatisticas_historico,
)

from src.terminal_service import (
    exibir_titulo,
    exibir_mensagem,
    solicitar_entrada,
)

from src.mensagens import MSG_NENHUM_REGISTRO_ENCONTRADO

from src.input_validator import (
    entrada_eh_numero,
    entrada_confirmada,
)

def exibir_registros_historico(registros):
    for registro in registros:
        exibir_mensagem(
            f"\n{registro['data_hora']} | "
            f"{registro['documento']} | "
            f"{registro['status']} | "
            f"{registro['mensagem']}"
        )

        if registro.get("caminho_pdf"):
            exibir_mensagem(f"PDF: {registro['caminho_pdf']}")

        if registro.get("caminho_evidencia"):
            exibir_mensagem(f"Evidência: {registro['caminho_evidencia']}")

def consultar_historico():

    historico = listar_historico()

    exibir_titulo("HISTÓRICO DE EMISSÕES")

    if not historico:
        exibir_mensagem(MSG_NENHUM_REGISTRO_ENCONTRADO)
        return
    
    filtro_documento = solicitar_entrada(
        "Filtrar por CPF/CNPJ (ENTER para todos): "
    )

    if filtro_documento.strip():
        historico = filtrar_historico_por_documento(filtro_documento)

    estatisticas = gerar_estatisticas_historico(historico)

    exibir_titulo("Resumo")
    exibir_mensagem(f"Total de registros: {estatisticas['total']}")
    exibir_mensagem(f"Sucessos: {estatisticas['sucesso']}")
    exibir_mensagem(f"Erros de execução: {estatisticas['erro_execucao']}")
    exibir_mensagem(f"Bloqueios: {estatisticas['bloqueio_automacao']}")
    exibir_mensagem(f"Documentos inválidos: {estatisticas['documento_invalido']}")
    exibir_mensagem(f"Resultados indefinidos: {estatisticas['resultado_indefinido']}")

    quantidade_texto = solicitar_entrada(
        "\nQuantos registros deseja visualizar? (padrão 10): "
    )

    quantidade = 10
    
    if entrada_eh_numero(quantidade_texto):
        quantidade = int(quantidade_texto)

    exibir_registros_historico(historico[-quantidade:])

    exportar = solicitar_entrada(
        "\nDeseja exportar este histórico para CSV? (s/n): "
    )

    if entrada_confirmada(exportar):
        exportar_historico_filtrado(historico[-quantidade:])