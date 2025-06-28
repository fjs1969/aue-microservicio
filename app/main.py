from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .pdf_processor import procesar_pdfs
from docx import Document
import os

app = FastAPI()

class InputData(BaseModel):
    municipio: str
    url_ficha: str
    url_informe: str

@app.post("/procesar")
def procesar(data: InputData):
    try:
        # 🧾 Verifica datos de entrada
        print(f"📥 Recibido: {data}")

        # 🧠 Procesamiento principal
        resultado = procesar_pdfs(data.municipio, data.url_ficha, data.url_informe)

        # 📄 Generar documento Word
        doc = Document()
        doc.add_heading(f"Diagnóstico AUE - {data.municipio}", 0)
        doc.add_paragraph(resultado)

        filename = f"{data.municipio.lower()}_diagnostico.docx"
        filepath = os.path.join("/tmp", filename)  # ubicación temporal segura
        doc.save(filepath)

        # 📤 Devolver archivo Word
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"❌ Error al procesar: {e}")
        raise HTTPException(status_code=500, detail=str(e))
