# Documento
MSG_DOCUMENTO_INVALIDO_NAO_INICIADO = "Documento inválido. A emissão não será iniciada."
MSG_DOCUMENTO_INVALIDO_IGNORADO = "Documento inválido. Ignorando..."
MSG_DOCUMENTO_INVALIDO_MANUAL = "CPF ou CNPJ inválido informado manualmente."
MSG_DOCUMENTO_INVALIDO_PLANILHA = "Documento inválido na planilha."

# Bloqueio
MSG_BLOQUEIO_DETECTADO_RETRY = "Bloqueio detectado pela SEFAZ. A emissão não será repetida agora."
MSG_BLOQUEIO_DETECTADO_LOTE = "Bloqueio detectado pela SEFAZ durante o lote."
MSG_BLOQUEIO_CONSULTAS = "A SEFAZ bloqueou temporariamente as consultas."
MSG_RECOMENDACAO_AGUARDAR = "Recomenda-se aguardar alguns minutos antes de tentar novamente."

# Emissão
MSG_ERRO_INESPERADO_EMISSAO = "Ocorreu um erro inesperado durante a emissão."
MSG_RESULTADO_INDEFINIDO = "Não foi possível identificar o resultado da emissão."
MSG_CERTIDAO_ENCONTRADA = "Certidão encontrada para o documento informado."
MSG_EVIDENCIA_SALVA_SUCESSO = "Evidência salva com sucesso!"
MSG_CAMINHO_EVIDENCIA = "Caminho: {caminho}"
MSG_PDF_NAO_ENCONTRADO = "Nenhum PDF encontrado na pasta Downloads."
MSG_PDF_MOVIDO_SUCESSO = "PDF movido com sucesso!"
MSG_GERANDO_RELATORIO_CONSOLIDADO = "Gerando relatório consolidado..."
MSG_TENTATIVA_EMISSAO_DOCUMENTO = "Tentativa {tentativa}/{total_tentativas} para o documento {documento}"
MSG_FALHA_APOS_TENTATIVAS = "Falha após {total_tentativas} tentativas."
MSG_ERRO_TENTATIVA_EMISSAO = "Erro na tentativa {tentativa} para o documento {documento}"
MSG_PROCESSANDO_DOCUMENTO = "\nProcessando documento: {documento}"

# Relatório
MSG_RELATORIO_GERADO_SUCESSO = "Relatório gerado com sucesso!"
MSG_CAMINHO_RELATORIO = "Caminho: {caminho}"

# Terminal
MSG_SISTEMA_ENCERRADO = "Sistema encerrado."
MSG_OPCAO_INVALIDA = "Opção inválida."
MSG_NENHUM_REGISTRO_ENCONTRADO = "Nenhum registro encontrado."
MSG_SOLICITAR_DOCUMENTO = "Informe o CPF ou CNPJ: "

# Espera / Retry
MSG_AGUARDANDO_RETRY = (
    "Aguardando {tempo} segundos antes de tentar novamente..."
)

MSG_AGUARDANDO_PROXIMA_EMISSAO = (
    "Aguardando {tempo} segundos antes da próxima emissão..."
)

MSG_PAUSA_BLOQUEIO = (
    "O sistema ficará pausado por aproximadamente {minutos} minutos."
)

# Títulos
MSG_TITULO_AUTOMACAO = "AUTOMAÇÃO SEFAZ"
MSG_TITULO_HISTORICO = "HISTÓRICO DE EMISSÕES"
MSG_TITULO_RESUMO = "Resumo"
MSG_TITULO_RESULTADO_EMISSAO = "RESULTADO DA EMISSÃO"
MSG_TITULO_RESULTADOS_FINAIS = "RESULTADOS FINAIS"
MSG_TITULO_DOCUMENTOS_ENCONTRADOS = "DOCUMENTOS ENCONTRADOS"

# Menu
MSG_MENU_EMISSAO_MANUAL = "Emitir certidão manual"
MSG_MENU_EMISSAO_PLANILHA = "Emitir certidões por planilha"
MSG_MENU_CONSULTAR_HISTORICO = "Consultar histórico"
MSG_MENU_ABRIR_PDFS = "Abrir pasta de PDFs"
MSG_MENU_ABRIR_RELATORIOS = "Abrir pasta de relatórios"
MSG_MENU_ABRIR_EVIDENCIAS = "Abrir pasta de evidências"
MSG_MENU_SAIR = "Sair"
MSG_ITEM_MENU = "{codigo}- {descricao}"
MSG_SOLICITAR_OPCAO_MENU = "\nEscolha uma opção:"

# PDF
MSG_PDF_NAO_DISPONIVEL_TENTATIVA = "PDF ainda não está disponível. Tentativa {tentativa}/{total}..."
MSG_PDF_AINDA_BAIXANDO_TENTATIVA = "PDF ainda não está baixando. Tentativa {tentativa}/{total}..."
MSG_PDF_EM_USO_TENTATIVA = "PDF ainda está em uso. Tentativa {tentativa}/{total}..."
MSG_DESTINO_ARQUIVO = "Destino: {destino}"
MSG_PDF_COPIADO_FALLBACK_SUCESSO = "PDF não pôde ser movido, mas foi copiado com sucesso."
MSG_PDF_COPIADO_SUCESSO = "PDF copiado com sucesso!"
MSG_PDF_FALHA_MOVE_E_COPIA = (
    "Não foi possível mover nem copiar o PDF após várias tentativas: {pdf}"
)

# EMISSAO_SEFAZ
MSG_COOKIES_ACEITOS = "Cookies aceitos com sucesso!"
MSG_COOKIES_NAO_ENCONTRADOS = "Banner de cookies não encontrado ou já aceito."
MSG_DOCUMENTO_PREENCHIDO_SUCESSO = "Documento preenchido com sucesso!"
MSG_BOTAO_EMITIR_CLICADO_SUCESSO = "Botão emitir clicado com sucesso!"
MSG_URL_APOS_EMITIR = "URL após emitir: {url}"
MSG_RESULTADO_EMISSAO_LOG = "Resultado da emissão: {resultado}"
MSG_PAGINA_SEFAZ_PROCESSADA = "Página da SEFAZ processada com sucesso!"
MSG_URL_ATUAL = "URL atual: {url}"
MSG_ERRO_INESPERADO_CONTEXTO_SEFAZ = "Erro inesperado durante a emissão na SEFAZ"
MSG_CPF_INVALIDO_INFORMADO = "CPF inválido informado."
MSG_CNPJ_INVALIDO_INFORMADO = "CNPJ inválido informado."
MSG_DEBUG_TEXTO_PAGINA = "DEBUG TEXTO DA PÁGINA:"
MSG_DOWNLOAD_PDF_INICIADO = "Download do PDF iniciado com sucesso!"
MSG_BOTAO_BAIXAR_PDF_NAO_ENCONTRADO = "Botão de baixar PDF não encontrado."

# Histórico
MSG_HISTORICO_ATUALIZADO_SUCESSO = "Histórico atualizado com sucesso!"
MSG_HISTORICO_NAO_ENCONTRADO = "Nenhum histórico encontrado."
MSG_HISTORICO_EXPORTADO_SUCESSO = "Histórico exportado com sucesso!"
MSG_FILTRO_DOCUMENTO_HISTORICO = "Filtrar por CPF/CNPJ (ENTER para todos): "
MSG_TOTAL_REGISTROS = "Total de registros: {total}"
MSG_TOTAL_SUCESSOS = "Sucessos: {total}"
MSG_TOTAL_ERROS_EXECUCAO = "Erros de execução: {total}"
MSG_TOTAL_BLOQUEIOS = "Bloqueios: {total}"
MSG_TOTAL_DOCUMENTOS_INVALIDOS = "Documentos inválidos: {total}"
MSG_TOTAL_RESULTADOS_INDEFINIDOS = "Resultados indefinidos: {total}"
MSG_QUANTIDADE_REGISTROS_VISUALIZAR = "\nQuantos registros deseja visualizar? (padrão 10): "
MSG_EXPORTAR_HISTORICO_CSV = "\nDeseja exportar este histórico para CSV? (s/n): "
MSG_REGISTRO_HISTORICO = "\n{data_hora} | {documento} | {status} | {mensagem}"
MSG_CAMINHO_PDF_HISTORICO = "PDF: {caminho_pdf}"
MSG_CAMINHO_EVIDENCIA_HISTORICO = "Evidência: {caminho_evidencia}"