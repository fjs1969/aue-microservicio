from fastapi import FastAPI, Form
from app.pdf_processor import procesar_municipio_completo
import os

app = FastAPI()

@app.post("/procesar_municipio")
def procesar(
    municipio: str = Form(...),
    output_nombre: str = Form(...),
    url_ficha: str = Form(...),
    url_informe: str = Form(...),
    url_memoria: str = Form(None),
    url_normas: str = Form(None)
):
    urls = {
        "Ficha PEGV": url_ficha,
        "Informe Urbanístico": url_informe
    }
    if url_memoria:
        urls["Memoria Urbanística"] = url_memoria
    if url_normas:
        urls["Normas Urbanísticas"] = url_normas

    output_path = os.path.join("/mnt/data", output_nombre)
    try:
        procesar_municipio_completo(municipio, urls, output_path)
        return {"mensaje": "Diagnóstico generado", "archivo": output_path}
    except Exception as e:
        return {"error": str(e)}
