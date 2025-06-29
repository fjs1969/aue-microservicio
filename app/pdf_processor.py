# app/pdf_processor.py
import os
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
from app.visor_scraper import capturar_mapa

def extraer_texto_y_tablas(pdf_path):
    texto = ""
    tablas = []
    doc = fitz.open(pdf_path)
    for page in doc:
        texto += page.get_text()
    return texto, tablas

def procesar_municipio_completo(municipio, urls, output_filename):
    output_folder = os.path.join("output", municipio.replace(" ", "_"))
    os.makedirs(output_folder, exist_ok=True)

    texto_total = ""
    for nombre_doc, url in urls.items():
        file_path = os.path.join(output_folder, f"{nombre_doc.replace(' ', '_')}.pdf")
        os.system(f"wget -q \"{url}\" -O \"{file_path}\"")
        texto, _ = extraer_texto_y_tablas(file_path)
        texto_total += f"\n--- {nombre_doc} ---\n{texto}\n"

    doc = Document()
    doc.add_heading(f"Diagnóstico Agenda Urbana de {municipio}", 0)
    doc.add_paragraph(texto_total)

    # Captura de mapa y adición al documento
    try:
        mapa_path = capturar_mapa(municipio, "Tipología de vulnerabilidad", output_folder)
        doc.add_heading("Mapa de Tipología de Vulnerabilidad", level=1)
        doc.add_picture(mapa_path, width=Inches(6))
    except Exception as e:
        doc.add_paragraph(f"No se pudo capturar el mapa: {str(e)}")

    doc.save(output_filename)
    print(f"Diagnóstico guardado en: {output_filename}")
