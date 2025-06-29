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
        doc.add_paragraph(f"Contenido extraído automáticamente desde: {url}")
        # Aquí podrías integrar análisis real del PDF

    # Capturar mapas desde el visor GVA
    capas = [
        "Tipología de vulnerabilidad",
        "Densidad urbana",
        "Sistemas generales"
    ]
    for capa in capas:
        try:
            output_img = os.path.join(os.path.dirname(output_filename), f"{municipio}_{capa.replace(' ', '_')}.png")
            img_path = capturar_mapa(municipio, capa, os.path.dirname(output_filename))
            if os.path.exists(img_path):
                doc.add_heading(f"Mapa: {capa}", level=2)
                doc.add_picture(img_path, width=Inches(6))
        except Exception as e:
            doc.add_paragraph(f"No se pudo generar el mapa de {capa}: {str(e)}")

    doc.save(output_filename)
