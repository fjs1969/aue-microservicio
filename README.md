# AUE Microservicio

Microservicio FastAPI para generar diagnósticos de Agendas Urbanas descargando y procesando PDFs automáticamente.

## Cómo desplegar (Railway)

1. Crear un nuevo proyecto en Railway.
2. Conectar este repositorio.
3. Railway detectará el Dockerfile y desplegará automáticamente.
4. Usa el endpoint `/procesar` con un JSON así:

```json
{
  "municipio": "Tuéjar",
  "url_ficha": "https://pegv.gva.es/auto/scpd/web/FM/CAS/ES_FM_46247.pdf",
  "url_informe": "https://mediambient.gva.es/documents/213952844/179408661/46247-1000+2021-0017+01.+Informe+Sostenibilidad+Ambiental.pdf"
}
```