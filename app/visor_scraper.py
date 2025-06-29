# app/visor_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import time
import os

def capturar_mapa(nombre_municipio, capa, output_dir):
    url_base = "https://visor.gva.es/visor/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

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

        screenshot_path = os.path.join(output_dir, f"{nombre_municipio}_{capa.replace(' ', '_')}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Mapa capturado: {screenshot_path}")
        return screenshot_path

    finally:
        driver.quit()
