# Imagen base
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY app/ ./app/
COPY app/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


