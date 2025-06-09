# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def buscar_estado_ot(numero_ot: str, tipo: str = "Orden de Transporte") -> list:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://sistema.tvp.cl/faces/logs_total.jsp")
        time.sleep(2)

        # Ingresar número OT
        input_ot = driver.find_element(By.NAME, "j_id_jsp_931588303_6:j_id_jsp_931588303_9")
        input_ot.send_keys(numero_ot)

        # Seleccionar tipo (Orden de Transporte o Numero de Retiro)
        select = driver.find_element(By.NAME, "j_id_jsp_931588303_6:select")
        for option in select.find_elements(By.TAG_NAME, 'option'):
            if option.text.strip() == tipo:
                option.click()
                break

        # Click en botón "Mostrar"
        boton = driver.find_element(By.NAME, "j_id_jsp_931588303_6:btnBuscar")
        boton.click()

        time.sleep(1)  # Esperar que se carguen los datos

        # Extraer la primera tabla de movimientos
        filas = driver.find_elements(By.XPATH, "//form[@id='j_id_jsp_931588303_27']//table[1]//tbody//tr")
        filas2 = driver.find_elements(By.XPATH, "//form[@id='j_id_jsp_931588303_6']//table[2]//tbody//tr")

        resultados = []

        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) >= 4:
                resultados.append({
                    "ot": columnas[0].text.strip(),
                    "estado": columnas[1].text.strip(),
                    "observacion": columnas[2].text.strip(),
                    "fecha": columnas[3].text.strip()
                })
        
    
        for fila in filas2:
            columnas = fila.find_elements(By.TAG_NAME, "td")
            if len(columnas) >= 2:
                resultados.append({
                    columnas[0].text.strip(): columnas[1].text.strip(),
                })

    
        # 2. Crear contenedor
        driver.execute_script("""
        if (!document.getElementById('vista-etiquetas')) {
            const div = document.createElement('div');
            div.id = 'vista-etiquetas';
            document.body.appendChild(div);
        }
        """)

        # 3. Sobrescribir impresión
        driver.execute_script("""
        PHE.printHtml = function(html) {
            document.getElementById('vista-etiquetas').innerHTML += html;
        };
        """)

        # 4. Ejecutar print()
        driver.execute_script("print();")

        # 5. Leer el HTML generado
        vista_html = driver.find_element("id", "vista-etiquetas").get_attribute("innerHTML")

        return vista_html

       
    finally:
        driver.quit()
