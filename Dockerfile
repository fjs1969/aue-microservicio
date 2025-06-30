# Usa una imagen base de Python oficial, ligera, pero basada en Debian 11 (Bullseye).
FROM python:3.9-slim-bullseye

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para un navegador headless
# y las herramientas para descargar y descomprimir Chrome/Chromedriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    # Dependencias mínimas y genéricas para navegadores headless
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
    # Limpia el cache de apt
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Google Chrome y ChromeDriver de "Chrome for Testing"
# Esto es más fiable para versiones específicas y para entornos sin APT-hell
ENV CHROME_VERSION="126.0.6478.63" # Puedes actualizar esta versión si necesitas una más reciente
ENV CHROMEDRIVER_VERSION="126.0.6478.63" # Debe coincidir con la versión de Chrome

RUN wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O /tmp/chrome-linux64.zip \
    && unzip /tmp/chrome-linux64.zip -d /opt/chrome-for-testing \
    && rm /tmp/chrome-linux64.zip \
    && wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver-linux64.zip -d /opt/chrome-for-testing \
    && rm /tmp/chromedriver-linux64.zip \
    # Asegurarse de que los binarios son ejecutables
    && chmod +x /opt/chrome-for-testing/chrome-linux64/chrome \
    && chmod +x /opt/chrome-for-testing/chromedriver-linux64/chromedriver

# Configurar variables de entorno para que Chrome y Chromedriver estén en el PATH
ENV PATH="/opt/chrome-for-testing/chrome-linux64:/opt/chrome-for-testing/chromedriver-linux64:${PATH}"
ENV CHROME_PATH="/opt/chrome-for-testing/chrome-linux64/chrome" # Ruta explícita para Selenium si es necesario

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación al directorio de trabajo
COPY . .

# Comando para iniciar la aplicación Uvicorn/FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]