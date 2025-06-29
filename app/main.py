from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
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
        return {"mensaje": "Diagnóstico generado correctamente", "archivo": f"/download/{output_nombre}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join("/mnt/data", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    return {"error": f"No se encuentra el archivo {filename}"}
