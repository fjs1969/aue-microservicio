from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import os

def capturar_mapa(nombre_municipio, capa, output_dir):
    url_base = "https://visor.gva.es/visor/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # 🔧 Corrección: uso explícito del servicio de Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url_base)
        time.sleep(5)  # espera a que cargue el visor

        # 🔍 Buscar el municipio
        buscador = driver.find_element(By.ID, "busquedaDireccion")
        buscador.send_keys(nombre_municipio)
        time.sleep(1)
        buscar_btn = driver.find_element(By.ID, "btnBusquedaDireccion")
        buscar_btn.click()
        time.sleep(5)

        # 📍 Activar la capa deseada
        driver.execute_script(f"""
            let capas = Array.from(document.querySelectorAll(".tree-layer"));
            let capa = capas.find(el => el.textContent.includes("{capa}"));
            if (capa) capa.click();
        """)
        time.sleep(4)

        # 📷 Captura de pantalla
        output_path = os.path.join(output_dir, f"{nombre_municipio}_{capa.replace(' ', '_')}.png")
        driver.save_screenshot(output_path)
        print(f"✅ Mapa capturado: {output_path}")
        return output_path

    finally:
        driver.quit()
