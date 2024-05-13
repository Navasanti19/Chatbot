import pyautogui
import time

print("Mueve el cursor a la esquina superior izquierda de la región y espera 5 segundos...")
time.sleep(5)
top_left = pyautogui.position()

print("Mueve el cursor a la esquina inferior derecha de la región y espera 5 segundos...")
time.sleep(5)
bottom_right = pyautogui.position()

print("Coordenadas de la región seleccionada:")
print(f"Top-left: {top_left}")
print(f"Bottom-right: {bottom_right}")
width = bottom_right.x - top_left.x
height = bottom_right.y - top_left.y
print(f"Ancho: {width}, Alto: {height}")
