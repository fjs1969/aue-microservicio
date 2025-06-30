FROM python:3.9-slim-bullseye

WORKDIR /app

# Instalar utilidades mínimas necesarias para Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl gnupg2 \
    libnss3 libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgbm1 libgtk-3-0 \
    ca-certificates fonts-liberation libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_VERSION="126.0.6478.63"
ENV CHROMEDRIVER_VERSION="126.0.6478.63"

RUN wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chrome-linux64.zip" -O /tmp/chrome.zip && \
    unzip /tmp/chrome.zip -d /opt/chrome && rm /tmp/chrome.zip && \
    wget "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /opt/chrome && rm /tmp/chromedriver.zip && \
    chmod +x /opt/chrome/chrome-linux64/chrome /opt/chrome/chromedriver-linux64/chromedriver

ENV PATH="/opt/chrome/chrome-linux64:/opt/chrome/chromedriver-linux64:$PATH"
ENV CHROME_PATH="/opt/chrome/chrome-linux64/chrome"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
