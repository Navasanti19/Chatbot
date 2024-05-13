import telepot
from telepot.loop import MessageLoop
import pyautogui
import pyperclip
import time
import keyboard
import uuid

def detener_script():
    print("Deteniendo el script...")
    exit()

keyboard.add_hotkey('esc', detener_script)

bot = telepot.Bot('6814032942:AAHAB3RGrI5T6zMfPXE9C40Ehmhh_dhj6NI')

def handle(msg):
    chat_id = msg['chat']['id']
    if 'text' in msg:
        command = msg['text']
        # Genera un marcador único para este mensaje
        unique_marker = str(uuid.uuid4())
        full_command = f"{command} {unique_marker}"
        print(f"Mensaje recibido: {full_command}")

        # Envía el mensaje al sistema externo
        pyautogui.click(x=725, y=950)  # Posición del campo de entrada en Chrome
        pyautogui.write(full_command)
        pyautogui.press('enter')
        
        # Espera para que el sistema procese el comando y genere una respuesta
        # time.sleep(20)
        
        # Intenta copiar la respuesta cada 2 segundos
        timeout = time.time() + 60  # 60 segundos de máximo
        while True:
            pyautogui.click(x=725, y=830)  # Ajusta esta posición al botón de copiar
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            respuesta = pyperclip.paste()
            if unique_marker in respuesta:
                print("Respuesta copiada: ", respuesta.replace(unique_marker, ''))
                bot.sendMessage(chat_id, respuesta.replace(unique_marker, ''))
                break
            if time.time() > timeout:
                print("Error: Tiempo de espera excedido.")
                bot.sendMessage(chat_id, "No pude copiar la respuesta a tiempo.")
                break
            time.sleep(2)  # Espera antes del próximo intento

    else:
        bot.sendMessage(chat_id, "Manejando una foto o otro tipo de mensaje")

MessageLoop(bot, handle).run_forever()
