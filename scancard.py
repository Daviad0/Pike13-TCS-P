
from mfrc522 import SimpleMFRC522 as SMFRC
import RPi.GPIO as GPIO
from time import sleep as wait
import asyncio
import websockets
import threading


GPIO.setwarnings(False)

writeQueue = ["0:7852099"]

r = SMFRC()

clients = []
messages = []

async def handleCard(websocket, path):
    global clients
    clients.append(websocket)
    while True:
        m = await websocket.recv()
        while len(messages) < 1:
            wait(0.1)
        await websocket.send(messages.pop(0))

def send_message():
    while True:
        
        try:
            if(len(writeQueue) > 0):
                print("Please scan to WRITE (" + writeQueue[0] + ")")
                r.write(writeQueue[0])
                print("Successfully wrote to card")
                writeQueue.pop(0)
            else:
                print("Please scan to READ:")
                id, t = r.read()
                textParts = str(t).split(":")
                print("Read",textParts)
                toGive = textParts[0] + ":" + textParts[1]
                messages.append(toGive)
                    
            
            
        except:
            print("Err Reading Card...")
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

