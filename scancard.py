from nbformat import write
from mfrc522 import SimpleMFRC522 as SMFRC
import RPi.GPIO as GPIO
from time import sleep as wait
import asyncio
import websockets
import threading


GPIO.setwarnings(False)

writeQueue = ["0:12345678"]

r = SMFRC()

clients = []

def handleCard(websocket, path):
    global clients
    print("New client connected")
    clients.append(websocket)

def send_message():
    while True:
        
        try:
            if(len(writeQueue) > 0):
                print("Please scan to WRITE (" + writeQueue[0] + ")")
                r.write(writeQueue[0].encode())
                print("Successfully wrote to card")
                writeQueue.pop(0)
            else:
                print("Please scan to READ:")
                id, t = r.read()
                t = t.decode()
                textParts = str(t).split(":")
                print("Read",textParts)
                for client in clients:
                    client.send(text.format())
                    
            
            
        except:
            print("Err Reading Card...")
            wait(3)
        


card = threading.Thread(target=send_message)
card.start()

start_server = websockets.serve(handleCard, '127.0.0.1', 1338)
asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_until_complete(send_message)
asyncio.get_event_loop().run_forever()

