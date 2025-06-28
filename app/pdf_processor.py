import requests
import fitz  # PyMuPDF
from docx import Document
import tempfile
import os

def procesar_pdfs(municipio: str, url_ficha: str, url_informe: str) -> str:
    try:
        # 1. Descargar PDFs a archivos temporales
        ficha_path = descargar_pdf(url_ficha, f"ficha_{municipio}.pdf")
        informe_path = descargar_pdf(url_informe, f"informe_{municipio}.pdf")

        # 2. Extraer texto de ambos PDFs
        texto_ficha = extraer_texto_pdf(ficha_path)
        texto_informe = extraer_texto_pdf(informe_path)

        # 3. Generar diagnóstico
        diagnostico = generar_diagnostico(municipio, texto_ficha, texto_informe)

        # 4. Crear documento Word
        crear_docx(municipio, diagnostico)

        return diagnostico

    except Exception as e:
        raise RuntimeError(f"❌ Error procesando los PDFs: {str(e)}")


def descargar_pdf(url: str, nombre_archivo: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"No se pudo descargar el PDF desde: {url}")
    tmp_path = os.path.join(tempfile.gettempdir(), nombre_archivo)
    with open(tmp_path, "wb") as f:
        f.write(response.content)
    return tmp_path


def extraer_texto_pdf(pdf_path: str) -> str:
    texto = ""
    with fitz.open(pdf_path) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto


def generar_diagnostico(municipio: str, texto_ficha: str, texto_informe: str) -> str:
    return (
        f"Diagnóstico para {municipio} generado a partir de "
        f"{len(texto_ficha)} caracteres de ficha y {len(texto_informe)} del informe."
    )


def crear_docx(municipio: str, contenido: str):
    doc = Document()
    doc.add_heading(f"Diagnóstico AUE - {municipio}", level=1)
    doc.add_paragraph(contenido)
    output_path = f"{municipio.lower().replace(' ', '_')}_diagnostico.docx"
    doc.save(output_path)
