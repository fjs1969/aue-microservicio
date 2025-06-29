import os
import fitz  # PyMuPDF
import requests
from docx import Document
from docx.shared import Inches

def descargar_pdf(url, destino):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destino, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"No se pudo descargar el archivo: {url}")

def extraer_texto_pdf(ruta_pdf):
    texto_total = ""
    with fitz.open(ruta_pdf) as doc:
        for pagina in doc:
            texto_total += pagina.get_text()
    return texto_total

def crear_documento(texto_extraido, municipio, output_path):
    doc = Document()
    doc.add_heading(f"Diagnóstico de {municipio}", level=1)
    doc.add_paragraph(texto_extraido)
    doc.save(output_path)

def procesar_municipio_completo(municipio, urls: dict, output_path: str):
    carpeta_temp = "temp_pdfs"
    os.makedirs(carpeta_temp, exist_ok=True)

    texto_total = ""
    for nombre_doc, url in urls.items():
        nombre_archivo = f"{municipio}_{nombre_doc.replace(' ', '_')}.pdf"
        ruta_archivo = os.path.join(carpeta_temp, nombre_archivo)
        descargar_pdf(url, ruta_archivo)
        texto = extraer_texto_pdf(ruta_archivo)
        texto_total += f"\n\n===== {nombre_doc} =====\n\n"
        texto_total += texto

    crear_documento(texto_total, municipio, output_path)
