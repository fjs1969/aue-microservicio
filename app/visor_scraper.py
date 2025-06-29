# app/visor_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os

def capturar_mapa(nombre_municipio, capa, output_path):
    url_base = "https://visor.gva.es/visor/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url_base)
        time.sleep(5)

        buscador = driver.find_element(By.ID, "busquedaDireccion")
        buscador.send_keys(nombre_municipio)
        time.sleep(1)
        buscar_btn = driver.find_element(By.ID, "btnBusquedaDireccion")
        buscar_btn.click()
        time.sleep(5)

        driver.execute_script(f"""
            let capas = Array.from(document.querySelectorAll(".tree-layer"));
            let capa = capas.find(el => el.textContent.includes("{capa}"));
            if (capa) capa.click();
        """)
        time.sleep(4)

        driver.save_screenshot(output_path)
        print(f"Mapa capturado en: {output_path}")
        return output_path

    finally:
        driver.quit()
