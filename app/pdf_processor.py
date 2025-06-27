import fitz  # PyMuPDF
import requests

def extraer_texto(url):
    response = requests.get(url)
    response.raise_for_status()
    texto = ""
    with fitz.open(stream=response.content, filetype="pdf") as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def procesar_pdfs(municipio, url_ficha, url_informe):
    texto_ficha = extraer_texto(url_ficha)
    texto_informe = extraer_texto(url_informe)
    # Aquí puedes usar lógica NLP o de patrones para extraer contenido estructurado
    return f"Diagnóstico para {municipio} generado a partir de {len(texto_ficha)} caracteres de ficha y {len(texto_informe)} del informe."
