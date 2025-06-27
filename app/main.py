from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .pdf_processor import procesar_pdfs

app = FastAPI()

class InputData(BaseModel):
    municipio: str
    url_ficha: str
    url_informe: str

@app.post("/procesar")
def procesar(data: InputData):
    try:
        resultado = procesar_pdfs(data.municipio, data.url_ficha, data.url_informe)
        return {"diagnostico": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
