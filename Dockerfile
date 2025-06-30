# Imagen base ligera con Python 3.9 sobre Debian Bullseye
FROM python:3.9-slim-bullseye

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalación de dependencias del sistema necesarias para ejecutar Chrome Headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg2 \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 \
    libgbm1 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 \
    libpango-1.0-0 libpangocairo-1.0-0 libu2f-udev libvulkan1 libxcomposite1 \
    libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 libxshmfence6 \
    libxss1 libxtst6 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Versiones específicas de Chrome y Chromedriver
ENV CHROME_VERSION="126.0.6478.63"
ENV CHROMEDRIVER_VERSION="126.0.6478.63"

# Descarga de Chrome y Chromedriver
RUN wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O /tmp/chrome.zip && \
    unzip /tmp/chrome.zip -d /opt/chrome && rm /tmp/chrome.zip && \
    wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /opt/chrome && rm /tmp/chromedriver.zip && \
    chmod +x /opt/chrome/chrome-linux64/chrome /opt/chrome/chromedriver-linux64/chromedriver

# Añadir Chrome y Chromedriver al PATH
ENV PATH="/opt/chrome/chrome-linux64:/opt/chrome/chromedriver-linux64:$PATH"
ENV CHROME_PATH="/opt/chrome/chrome-linux64/chrome"

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . .

# Exponer el puerto que usará Uvicorn
EXPOSE 8000

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
