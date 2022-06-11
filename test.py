
# from mfrc522 import SimpleMFRC522 as SMFRC
# import RPi.GPIO as GPIO
from time import sleep as wait
import asyncio

from nbformat import write
import websockets
import threading
import requests


# GPIO.setwarnings(False)

writeQueue = []

# r = SMFRC()

clients = []
messages = []

async def handleCard(websocket, path):
    global messages
    messages = []
    while True: 
        m = await websocket.recv()
        while len(messages) < 1:
            wait(0.1)
        await websocket.send(messages.pop(0))

def send_message():
    while True:
        
        
        
        
        try:
            
            obj = requests.get("http://localhost:1337/message").json()
            if(obj["m"] == True):
                writeQueue.append(obj["message"])
            
            if(len(writeQueue) > 0):
                msg = writeQueue.pop(0)
                messages.push(msg)
                print("sending ")
            else:
                r = input("READ: ")
                messages.push(r)
                    
            
            
        except:
            print("Err Reading Card...")
            messages.append("ERROR")
            wait(3)
        # id = input("Sign in ID: ")
        # toGive = "0" + ":" + id
        # messages.append(toGive)
        


card = threading.Thread(target=send_message)
card.start()

start_server = websockets.serve(handleCard, '127.0.0.1', 1338)
asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_until_complete(send_message)
asyncio.get_event_loop().run_forever()

