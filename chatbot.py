import telepot
from telepot.loop import MessageLoop


def handle(msg):
    print(msg)
    if 'text' in msg:
        command=msg['text']
        if command=='Hola':
            bot.sendMessage(msg['from']['id'], 'Hola '+ msg['from']['first_name'] +' soy Bob, tu asistente virtual')
            bot.sendMessage(msg['from']['id'], '¿En que puedo ayudarte?')
            bot.sendMessage(msg['from']['id'], 'Manda una foto de tu problema para poder ayudarte')
    else:
        bot.sendMessage(msg['from']['id'], 'Foto recibida, en unos momentos te redigiré con los especialista adecuados')
        bot.sendMessage(msg['from']['id'], 'Estoy procesando la imagen, por favor espera')
        command=msg['photo'][2]['file_id']
        bot.download_file(command, 'fotoRecibida.jpg')
        bot.sendMessage(msg['from']['id'], 'Parece que tu problema es una tubería rota, te redirigiré con los especialistas en plomería')
        

bot = telepot.Bot('6814032942:AAHAB3RGrI5T6zMfPXE9C40Ehmhh_dhj6NI') #ChatBOB
MessageLoop(bot,handle).run_forever()





