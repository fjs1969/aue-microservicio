# app/pdf_processor.py
import os
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
from app.visor_scraper import capturar_mapa

def procesar_municipio_completo(municipio, urls, output_path):
    doc = Document()
    doc.add_heading(f"Diagnóstico AUE de {municipio}", 0)

    for nombre_doc, url in urls.items():
        doc.add_heading(nombre_doc, level=1)
        doc.add_paragraph(f"URL del documento: {url}")

        if url.endswith(".pdf"):
            try:
                with fitz.open(stream=os.popen(f"curl -s {url}").read().encode(), filetype="pdf") as pdf:
                    texto = ""
                    for page in pdf:
                        texto += page.get_text()
                    doc.add_paragraph(texto[:1000] + "..." if len(texto) > 1000 else texto)
            except Exception as e:
                doc.add_paragraph(f"No se pudo leer el PDF: {e}")
        else:
            doc.add_paragraph("Formato no soportado o URL inválida.")

    # Captura automática del mapa de vulnerabilidad
    mapa_vulnerabilidad = capturar_mapa(municipio, "Tipología de vulnerabilidad", os.path.dirname(output_path))
    if mapa_vulnerabilidad and os.path.exists(mapa_vulnerabilidad):
        doc.add_picture(mapa_vulnerabilidad, width=Inches(6))
        doc.add_paragraph("Mapa de vulnerabilidad añadido automáticamente.")

    doc.save(output_path)
    print(f"Documento guardado en: {output_path}")
