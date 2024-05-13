from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()
# Especifica correctamente el directorio de datos de usuario y el perfil
chrome_options.add_argument(r"user-data-dir=C:\Users\luisf\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument("profile-directory=Profile 4")

# Asegúrate de que el path al chromedriver sea el correcto
service = Service(executable_path="C:\\Users\\luisf\\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Intenta abrir la página
try:
    driver.get("https://chatgpt.com/g/g-H1igZQs86-bob")
    # Aquí puedes agregar más operaciones si lo necesitas
    # Por ejemplo, encontrar un elemento y enviar texto
    element = driver.find_element(By.CSS_SELECTOR, 'textarea[data-id="root"]')
    element.send_keys("Hola mundo!")
    element.send_keys(Keys.RETURN)  # Envía el mensaje
except Exception as e:
    print(f"Ocurrió un error: {e}")

# Mantén el script en espera para que el navegador no se cierre
input("Presiona Enter para cerrar el navegador...")

# Si quieres cerrar el navegador manualmente, puedes descomentar la siguiente línea
# driver.quit()
