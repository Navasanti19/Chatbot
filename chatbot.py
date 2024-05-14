from __future__ import print_function, division
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import cv2
import time
import keyboard
from math import pi 
import matplotlib.pyplot as plt
import numpy as np
import glob
import telepot
from telepot.loop import MessageLoop

global device
device="cuda"

global model
model=torch.load('bobred.pth')
model.to(device)
model.eval()

global loader
loader = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

def image_loader(image_name):
    global device
    image = Image.fromarray(image_name)
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)  
    return image.to(device)

global classes
classes= ('FAUCET', 'OUTLET', 'WALL')



def handle(msg):
    global model
    global loader
    global classes

    #print(msg['text'])
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
        bot.download_file(command, 'fotoRecibida.png')
        
        img=cv2.imread('fotoRecibida.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image=image_loader(img)
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)
      
        print(classes[predicted[0]])

        if classes[predicted[0]] == 'FAUCET':
            bot.sendMessage(msg['from']['id'], 'Parece que tu problema es una llave rota, te redirigiré con los especialistas en plomería') 
        elif classes[predicted[0]] == 'OUTLET':
            bot.sendMessage(msg['from']['id'], 'Parece que tu problema es un contacto eléctrico roto, te redirigiré con los especialistas en electricidad')
        elif classes[predicted[0]] == 'WALL':
            bot.sendMessage(msg['from']['id'], 'Parece que tu problema es de una pared dañada, te redirigiré con los especialistas en paredes')

        

bot = telepot.Bot('6814032942:AAHAB3RGrI5T6zMfPXE9C40Ehmhh_dhj6NI') #ChatBOB
MessageLoop(bot,handle).run_forever()





