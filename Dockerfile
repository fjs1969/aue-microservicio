# Usa una imagen base de Python oficial, ligera y basada en Debian.
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para Chromium y otras herramientas
# Esto incluye herramientas básicas (wget, gnupg, unzip) y las dependencias de Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    # Dependencias necesarias para Chromium en un entorno headless
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libu2f-udev \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxshmfence6 \
    libxss1 \
    libxtst6 \
    # Instalación de Chromium y su Chromedriver (nombres de paquete ajustados)
    chromium \
    chromium-driver \
    # Limpia el cache de apt para reducir el tamaño de la imagen
    && rm -rf /var/lib/apt/lists/*

# Configura la variable de entorno para que Chromedriver esté en el PATH
# Asegúrate de que esta ruta sea la correcta para tu instalación de chromium-driver
ENV PATH="/usr/lib/chromium/:${PATH}"

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación al directorio de trabajo
COPY . .

# Comando para iniciar la aplicación Uvicorn/FastAPI
# Asegúrate de que 'main:app' apunta a tu aplicación FastAPI
# Por ejemplo, si tu archivo principal es 'main.py' y tu instancia de FastAPI se llama 'app'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]