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
        
        
        time.sleep(2)
        
        timeout = time.time() + 60
        while True:
            pyautogui.click(x=725, y=825)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            respuesta = pyperclip.paste()
            if unique_marker in respuesta:
                resp = respuesta.replace(("Código: " + unique_marker), '')
                print("Respuesta copiada: ", resp)
                bot.sendMessage(chat_id, resp)
                break
            if time.time() > timeout:
                print("Error: Tiempo de espera excedido.")
                bot.sendMessage(chat_id, "No pude procesar tu solicitud a tiempo. Vuelve a intentarlo.")
                break
            time.sleep(2)  # Espera antes del próximo intento

    else:
        bot.sendMessage(chat_id, "Manejando una foto o otro tipo de mensaje")

MessageLoop(bot, handle).run_forever()
