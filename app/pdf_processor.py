# app/pdf_processor.py
import os
from docx import Document
from docx.shared import Inches
from app.visor_scraper import capturar_mapa

def procesar_municipio_completo(municipio, urls, output_filename):
    doc = Document()
    doc.add_heading(f"Diagnóstico AUE - {municipio}", level=1)
    doc.add_heading("4.4.1. Diagnóstico territorial y urbano", level=2)

    # Insertar textos de PDFs (simulado aquí)
    for name, url in urls.items():
        doc.add_heading(name, level=2)
        doc.add_paragraph(f"Contenido extraído automáticamente de {url}")

    # Captura de mapas
    output_folder = os.path.dirname(output_filename)
    capa_vulnerabilidad = "Tipología de vulnerabilidad"
    mapa_vulnerabilidad_path = capturar_mapa(municipio, capa_vulnerabilidad, output_folder)

    if mapa_vulnerabilidad_path and os.path.exists(mapa_vulnerabilidad_path):
        doc.add_heading("Mapa de vulnerabilidad territorial", level=2)
        doc.add_picture(mapa_vulnerabilidad_path, width=Inches(6))
        doc.add_paragraph("Fuente: visor.gva.es")

    # Guardar el documento
    doc.save(output_filename)
    print(f"Documento guardado en: {output_filename}")
