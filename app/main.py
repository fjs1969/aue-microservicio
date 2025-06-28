from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from docx import Document
from .pdf_processor import procesar_pdfs  # Asegúrate que este import funciona y el archivo existe

app = FastAPI()

class InputData(BaseModel):
    municipio: str
    url_ficha: str
    url_informe: str

@app.post("/procesar")
def procesar(data: InputData):
    try:
        # 🧾 Mostrar los datos de entrada en logs para depuración
        print("📥 Datos recibidos:", data)

        # 🧠 Procesar PDFs con tu lógica personalizada
        resultado = procesar_pdfs(data.municipio, data.url_ficha, data.url_informe)

        # 📄 Crear documento Word con el resultado
        doc = Document()
        doc.add_heading(f"Diagnóstico AUE - {data.municipio}", 0)
        doc.add_paragraph(resultado)

        # 💾 Guardar el archivo con nombre en minúscula
        path_docx = f"{data.municipio.lower()}_diagnostico.docx"
        doc.save(path_docx)

        # 📤 Devolver el documento como archivo descargable
        return FileResponse(
            path=path_docx,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=path_docx
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
