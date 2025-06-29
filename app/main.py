from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import os
from app.pdf_processor import procesar_municipio_completo

app = FastAPI()

@app.post("/procesar_municipio")
def procesar(
    municipio: str = Form(...),
    url_ficha: str = Form(...),
    url_informe: str = Form("")
):
    output_filename = f"{municipio.capitalize()}_Diagnostico_AUE.docx"
    output_path = os.path.join("/mnt/data", output_filename)
    try:
        print(f"Procesando municipio: {municipio}")
        print(f"Ficha: {url_ficha}")
        print(f"Informe: {url_informe}")
        print(f"Guardando en: {output_path}")

        procesar_municipio_completo(municipio, url_ficha, url_informe, output_path)

        if os.path.exists(output_path):
            print(f"Archivo generado: {output_path}")
            return {
                "mensaje": "Diagnóstico generado",
                "archivo": f"/download/{output_filename}"
            }
        else:
            print("❌ Archivo no encontrado tras generación.")
            return {"error": "No se generó el archivo correctamente"}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

@app.get("/download/{filename}")
def descargar_archivo(filename: str):
    ruta_archivo = os.path.join("/mnt/data", filename)
    print(f"Descargando archivo: {ruta_archivo}")
    if os.path.exists(ruta_archivo):
        return FileResponse(ruta_archivo, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=filename)
    return {"detail": "Not Found"}
