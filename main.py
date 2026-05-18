from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.utils import (
    limpar_documento,
    identificar_tipo_documento,
    validar_documento,
    criar_pastas_necessarias
)

def main():

    criar_pastas_necessarias()

    documento = input("Por gentileza, informe o documento (CPF ou CNPJ): ")

    documento_limpo = limpar_documento(documento)

    tipo = identificar_tipo_documento(documento)

    valido = validar_documento(documento)

    print("\n === RESULTADO ===")
    
    print (f"Documento original: {documento}")

    print (f"Documento limpo: {documento_limpo}")

    print (f"Tipo do documento: {tipo}")

    print (f"Documento válido? {valido}")

if __name__ == "__main__":
    main()