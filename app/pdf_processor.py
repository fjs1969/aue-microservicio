# app/pdf_processor.py
import os
from docx import Document
from docx.shared import Inches
from app.visor_scraper import capturar_mapa

def procesar_municipio_completo(municipio, urls, output_filename):
    doc = Document()
    doc.add_heading(f"Diagnóstico AUE - {municipio}", 0)
    doc.add_heading("4.4.1. Diagnóstico territorial y urbano", level=1)

    # Insertar textos de PDFs
    for name, url in urls.items():
        doc.add_heading(name, level=2)
        doc.add_paragraph(f"Contenido extraído automáticamente de: {url}")

    # Capturar e insertar mapa de vulnerabilidad
    mapa_path = os.path.join(os.path.dirname(output_filename), "mapa_vulnerabilidad.png")
    try:
        capturar_mapa(municipio, "Tipología de vulnerabilidad", mapa_path)
        doc.add_heading("Mapa de vulnerabilidad territorial", level=2)
        doc.add_picture(mapa_path, width=Inches(6))
    except Exception as e:
        doc.add_paragraph(f"No se pudo capturar el mapa: {str(e)}")

    doc.save(output_filename)
    print(f"Documento guardado en: {output_filename}")
