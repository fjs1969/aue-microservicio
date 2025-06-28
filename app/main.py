from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .pdf_processor import procesar_pdfs  # Asegúrate de que este import funciona

app = FastAPI()

class InputData(BaseModel):
    municipio: str
    url_ficha: str
    url_informe: str

@app.post("/procesar")
def procesar(data: InputData):
    try:
        # 📋 Depuración: mostrar datos recibidos en logs
        print("🧾 Datos recibidos:", data)

        # 🧠 Procesar PDFs con tu lógica
        resultado = procesar_pdfs(data.municipio, data.url_ficha, data.url_informe)

        # 📤 Devolver el resultado como respuesta JSON
        return {"diagnostico": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))