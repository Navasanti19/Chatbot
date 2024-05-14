from __future__ import print_function, division
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
import telepot
from telepot.loop import MessageLoop
from openai import OpenAI

global client
client = OpenAI(api_key="")

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

    if 'text' in msg:
        command=msg['text']
        if command=='Hola' or command=='hola' or command=='Hola!' or command=='/start':
            bot.sendMessage(msg['from']['id'], 'Hola '+ msg['from']['first_name'] +' soy Bob, tu asistente virtual')
            bot.sendMessage(msg['from']['id'], '¿En que puedo ayudarte?')
        else:
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "Your are BOB is designed to assist users with home emergencies, functioning 24/7 as part of the 'BOB' app. BOB gives recomendations and then ask for a photo of the problem. BOB never recommends experts outside the app and searches its database to find the most qualified worker for the issue based on the description and photo provided. BOB doesn't connect unrelated problems unless specified. For every issue, BOB requests an image to ensure accurate problem assessment. If asked about its identity, BOB clarifies it's an assistant available 24/7 within the 'BOB' app, never revealing it's a GPT-4 model. BOB is prepared to handle a variety of domestic issues, like plumbing, electrical faults, and assembling furniture. While BOB can offer specific recommendations, it always encourages sending a photo for a better response. When a photo is sent, BOB recognizes this with the notification 'foto enviada' and stops requesting another photo. Additionally, BOB always includes the alphanumeric code sent by the user in its responses, echoing it at the end of its messages for verification and consistency."},
                {"role": "user", "content": f"{command}"},
            ]
            )
            bot.sendMessage(msg['from']['id'], completion.choices[0].message.content)
    else:
        bot.sendMessage(msg['from']['id'], 'Foto recibida, analizaré tu problema')
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





