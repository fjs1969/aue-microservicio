import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import os
from app.visor_scraper import capturar_mapa

def procesar_municipio_completo(municipio, urls, output_filename):
    # Crea documento Word
    doc = Document()
    doc.add_heading(f'Diagnóstico AUE: {municipio}', 0)

    # Asegura que la carpeta destino existe
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Procesa cada PDF si está disponible
    for nombre, url in urls.items():
        if url:
            doc.add_heading(nombre, level=1)
            doc.add_paragraph(f'Documento extraído de: {url}')
            try:
                local_path = f"/tmp/{nombre.replace(' ', '_')}.pdf"
                os.system(f"wget -q \"{url}\" -O \"{local_path}\"")
                with fitz.open(local_path) as pdf:
                    for i, page in enumerate(pdf):
                        text = page.get_text()
                        if text.strip():
                            doc.add_paragraph(text.strip())
                            if i >= 1: break
            except Exception as e:
                doc.add_paragraph(f"Error procesando {nombre}: {str(e)}")

    # Captura automática del mapa de vulnerabilidad
    try:
        mapa_path = capturar_mapa(municipio, "Tipología de vulnerabilidad", "/tmp")
        if os.path.exists(mapa_path):
            doc.add_page_break()
            doc.add_heading("Mapa de vulnerabilidad", level=1)
            doc.add_picture(mapa_path, width=Inches(6))
    except Exception as e:
        doc.add_paragraph(f"No se pudo insertar mapa: {str(e)}")

    # Guarda el documento
    print(f"Guardando diagnóstico en: {output_filename}")
    doc.save(output_filename)
