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

from src.mensagens import (
    MSG_NENHUM_REGISTRO_ENCONTRADO,
    MSG_TITULO_HISTORICO,
    MSG_TITULO_RESUMO,
    MSG_FILTRO_DOCUMENTO_HISTORICO,
    MSG_TOTAL_REGISTROS,
    MSG_TOTAL_SUCESSOS,
    MSG_TOTAL_ERROS_EXECUCAO,
    MSG_TOTAL_BLOQUEIOS,
    MSG_TOTAL_DOCUMENTOS_INVALIDOS,
    MSG_TOTAL_RESULTADOS_INDEFINIDOS,
    MSG_QUANTIDADE_REGISTROS_VISUALIZAR,
    MSG_EXPORTAR_HISTORICO_CSV,
    MSG_REGISTRO_HISTORICO,
    MSG_CAMINHO_PDF_HISTORICO,
    MSG_CAMINHO_EVIDENCIA_HISTORICO,
)

from src.input_validator import (
    entrada_eh_numero,
    entrada_confirmada,
)


def exibir_registros_historico(registros):
    for registro in registros:
        exibir_mensagem(
            MSG_REGISTRO_HISTORICO.format(
                data_hora=registro["data_hora"],
                documento=registro["documento"],
                status=registro["status"],
                mensagem=registro["mensagem"],
            )
        )

        if registro.get("caminho_pdf"):
            exibir_mensagem(
                MSG_CAMINHO_PDF_HISTORICO.format(caminho_pdf=registro["caminho_pdf"])
            )

        if registro.get("caminho_evidencia"):
            exibir_mensagem(
                MSG_CAMINHO_EVIDENCIA_HISTORICO.format(
                    caminho_evidencia=registro["caminho_evidencia"]
                )
            )


def consultar_historico():

    historico = listar_historico()

    exibir_titulo(MSG_TITULO_HISTORICO)

    if not historico:
        exibir_mensagem(MSG_NENHUM_REGISTRO_ENCONTRADO)
        return
    
    filtro_documento = solicitar_entrada(
        MSG_FILTRO_DOCUMENTO_HISTORICO
    )

    if filtro_documento.strip():
        historico = filtrar_historico_por_documento(filtro_documento)

    estatisticas = gerar_estatisticas_historico(historico)

    exibir_titulo(MSG_TITULO_RESUMO)
    exibir_mensagem(MSG_TOTAL_REGISTROS.format(total=estatisticas["total"]))
    exibir_mensagem(MSG_TOTAL_SUCESSOS.format(total=estatisticas["sucesso"]))
    exibir_mensagem(MSG_TOTAL_ERROS_EXECUCAO.format(total=estatisticas["erro_execucao"]))
    exibir_mensagem(MSG_TOTAL_BLOQUEIOS.format(total=estatisticas["bloqueio_automacao"]))
    exibir_mensagem(
        MSG_TOTAL_DOCUMENTOS_INVALIDOS.format(total=estatisticas["documento_invalido"])
    )
    exibir_mensagem(
        MSG_TOTAL_RESULTADOS_INDEFINIDOS.format(total=estatisticas["resultado_indefinido"])
    )

    quantidade_texto = solicitar_entrada(
        MSG_QUANTIDADE_REGISTROS_VISUALIZAR
    )

    quantidade = 10
    
    if entrada_eh_numero(quantidade_texto):
        quantidade = int(quantidade_texto)

    exibir_registros_historico(historico[-quantidade:])

    exportar = solicitar_entrada(
        MSG_EXPORTAR_HISTORICO_CSV
    )

    if entrada_confirmada(exportar):
        exportar_historico_filtrado(historico[-quantidade:])