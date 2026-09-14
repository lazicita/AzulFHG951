# Nombre: Azul Hernandez Garcia
# Grupo: 951
# Fecha de realización: 5 de septiembre de 2026
# Descripción del problema: Implementar un proceso de web scraping
# utilizando la librería Selenium de Python, aplicado sobre la página
# de compras MercadoLibre México.


import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navegar(producto, paginas):
    url = "https://www.mercadolibre.com.mx/"
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument('--window-size=1020x800')
    navegador = webdriver.Chrome(service=s, options=opc)

    wait = WebDriverWait(navegador, 10)

    navegador.get(url)
    time.sleep(2)

    txtuser = wait.until(
        EC.presence_of_element_located((By.ID, "cb1-edit"))
    )

    txtuser.send_keys(producto)
    time.sleep(2)
    txtuser.send_keys(Keys.ENTER)
    time.sleep(2)
    time.sleep(2)

    data = []

    for pagina in range(1, paginas + 1):
        if pagina > 1:
            buttonext = navegador.find_element(By.CLASS_NAME, "andes-pagination__button--next")
            linknext = buttonext.find_element(By.TAG_NAME, "a")
            navegador.execute_script("arguments[0].click();", linknext)
            time.sleep(2)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-search-layout"))
        )
        items = navegador.find_elements(By.CLASS_NAME, "poly-card")

        for item in items:
            try:
                nombre = item.find_element(By.CLASS_NAME, "poly-component__title").text
            except:
                nombre = "No mencionado"
            try:
                precio = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text

            except:
                precio = "No mencionado"
            try:
                fecha_entrega = item.find_element(By.CLASS_NAME, "polylabel-pill").text
            except:
                fecha_entrega = "No mencionado"

            if not fecha_entrega.startswith("Llega"):
                fecha_entrega = "No mencionado"

            info_producto = {"Nombre": nombre, "Precio ($)": precio, "Fecha_Entrega": fecha_entrega}
            data.append(info_producto)
    navegador.close()

    df = pd.DataFrame(data)
    df.to_csv("informacion_productos.csv", index=False)
    return df


if __name__ == "__main__":
    navegar("Sanrio", 3)