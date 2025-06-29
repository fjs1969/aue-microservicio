from fastapi import FastAPI, Form
from pdf_processor import procesar_municipio_completo
import os

app = FastAPI()

# Asociación provincia -> código URL
PROVINCIAS = {
    "Castellón": "3%20CASTELL%d3N",
    "Valencia": "4%20VALENCIA",
    "Alicante": "2%20ALICANTE"
}

@app.post("/procesar_municipio_general")
def procesar_general(
    municipio: str = Form(...),
    codigo_ine: str = Form(...),
    provincia: str = Form(...),
    output_nombre: str = Form(...)
):
    try:
        base_url = f"https://mediambient.gva.es/auto/urbanismo/reg-planeamiento/{PROVINCIAS[provincia]}/{codigo_ine}%20{municipio.upper()}/1%20P.%20GENERAL/{codigo_ine}-1000%201990-0087%20%20NNSS%20{municipio.upper()}/"

        urls = {
            "Ficha PEGV": f"https://dogv.gva.es/datos/2021/07/22/pdf/2021_7683.pdf",  # Sustituir si hay otra específica
            "Memoria Urbanística": base_url + "3%20PLANOS/" + f"{codigo_ine}-1000%201990-0087%20%20NNSS%20{municipio.upper()}%20MEMORIA.pdf",
            "Normas Urbanísticas": base_url + "4%20NORMAS/" + f"{codigo_ine}-1000%201990-0087%20%20NNSS%20{municipio.upper()}%20NORMAS%20URBANISTICAS.pdf"
        }

        output_path = os.path.join("/mnt/data", output_nombre)
        procesar_municipio_completo(municipio, urls, output_path)
        return {"mensaje": "Diagnóstico generado", "archivo": output_path}
    except Exception as e:
        return {"error": str(e)}