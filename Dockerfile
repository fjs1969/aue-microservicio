# Usa una imagen base de Python oficial, ligera, pero basada en Debian 11 (Bullseye).
# Bullseye tiene paquetes más actualizados y puede resolver el problema de libxshmfence6.
FROM python:3.9-slim-bullseye

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias de sistema y Google Chrome Stable
# Esta es una versión mejorada para la instalación de Chrome/Chromedriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Herramientas básicas
    wget \
    gnupg \
    unzip \
    # Dependencias de Chrome/Navegador Headless (se mantienen ya que son genéricas para X server libs)
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
    # Ahora, añadir Google Chrome Stable y su repositorio
    # Descargar la clave GPG de Google de forma segura y añadirla al sistema de claves
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    # Añadir el repositorio oficial de Google Chrome para la versión estable
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    \
    # Actualizar listas de paquetes para incluir el nuevo repositorio de Google Chrome
    && apt-get update \
    # Instalar Google Chrome Stable
    && apt-get install -y google-chrome-stable \
    # Limpia el cache de apt para reducir el tamaño de la imagen
    && rm -rf /var/lib/apt/lists/*

# Configura la variable de entorno PATH para incluir los binarios de Chrome y Chromedriver.
# Google Chrome Stable instala el binario de Chrome en /usr/bin/google-chrome.
# ChromeDriver a menudo se instala en /usr/bin/chromedriver o se enlaza allí.
ENV PATH="/usr/bin:/usr/local/bin:${PATH}"

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación al directorio de trabajo
COPY . .

# Comando para iniciar la aplicación Uvicorn/FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]