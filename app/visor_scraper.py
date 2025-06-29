# app/visor_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def capturar_mapa(nombre_municipio, capa, output_dir):
    url_base = "https://visor.gva.es/visor/"
    os.makedirs(output_dir, exist_ok=True)
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

    try:
        driver.get(url_base)
        time.sleep(6)
        buscador = driver.find_element(By.ID, "busquedaDireccion")
        buscador.send_keys(nombre_municipio)
        time.sleep(1)
        driver.find_element(By.ID, "btnBusquedaDireccion").click()
        time.sleep(6)

        driver.execute_script(f"""
            document.querySelectorAll('.tree-layer').forEach(el => {{
                if(el.textContent.includes("{capa}")) el.click();
            }});
        """)
        time.sleep(5)

        path = os.path.join(output_dir, f"{nombre_municipio}_{capa.replace(' ', '_')}.png")
        driver.save_screenshot(path)
        return path

    finally:
        driver.quit()
