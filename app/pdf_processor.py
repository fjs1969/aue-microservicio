import fitz  # PyMuPDF
import requests
from docx import Document
from docx.shared import Inches
import os
from app.visor_scraper import capturar_mapa

def descargar_pdf_y_extraer_texto(url, output_path):
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    doc = fitz.open(output_path)
    texto = ""
    for page in doc:
        texto += page.get_text()
    return texto

def procesar_municipio_completo(municipio, urls, output_filename):
    output_folder = os.path.dirname(output_filename)
    os.makedirs(output_folder, exist_ok=True)

    doc = Document()
    doc.add_heading(f'Diagnóstico del municipio de {municipio}', 0)

    # Extraer y añadir textos de PDFs
    for nombre, url in urls.items():
        if url:
            doc.add_heading(nombre, level=1)
            pdf_path = os.path.join(output_folder, f"{nombre.replace(' ', '_')}.pdf")
            try:
                texto = descargar_pdf_y_extraer_texto(url, pdf_path)
                doc.add_paragraph(texto[:1000] + "..." if len(texto) > 1000 else texto)
            except Exception as e:
                doc.add_paragraph(f"Error al procesar {nombre}: {str(e)}")

    # Capturar mapas desde el visor GVA
    capas = [
        "Tipología de vulnerabilidad",
        "Planeamiento General",
        "Clasificación del suelo",
        "Protección Territorial"
    ]
    doc.add_heading("Mapas extraídos del visor GVA", level=1)
    for capa in capas:
        try:
            mapa_path = capturar_mapa(municipio, capa, output_folder)
            doc.add_paragraph(capa)
            doc.add_picture(mapa_path, width=Inches(6))
        except Exception as e:
            doc.add_paragraph(f"No se pudo capturar la capa '{capa}': {str(e)}")

    doc.save(output_filename)
    print(f"📄 Diagnóstico generado en: {output_filename}")
