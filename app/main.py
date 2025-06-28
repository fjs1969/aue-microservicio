from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .pdf_processor import procesar_pdfs
import os
import tempfile

app = FastAPI()

class InputData(BaseModel):
    municipio: str
    url_ficha: str
    url_informe: str

@app.post("/procesar")
def procesar(data: InputData):
    try:
        print("📥 Recibido:", data)

        # Crear una ruta temporal para el .docx
        filename = f"{data.municipio.lower().replace(' ', '_')}_diagnostico.docx"
        tmp_dir = tempfile.gettempdir()
        output_path = os.path.join(tmp_dir, filename)

        # Llamada a la función con cuatro argumentos
        resultado = procesar_pdfs(
            data.municipio,
            data.url_ficha,
            data.url_informe,
            output_path
        )

        # Verificar que el documento se generó
        if not os.path.exists(output_path):
            raise FileNotFoundError("❌ No se ha generado el archivo .docx")

        # Devolver el archivo descargable
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
