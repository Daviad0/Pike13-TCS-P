# from MFRC522 import SimpleMFRC522 as SMFRC
# import RPi.GPIO as GPIO
# from time import sleep as wait
import asyncio
import websockets

# GPIO.setwarnings(False)

# r = SMFRC()

clients = []

async def handleCard(websocket, path):
    global clients
    print("New client connected")
    clients.append(websocket)

async def send_message():
    while True:
        text = input("Send a message: ")
        # try:
        #     print("Please scan your card")
        #     id, text = r.read()
            
        # except:
        #     print("Err Reading Card...")
        #     wait(3)
        for client in clients:
            client.send(text.format())
            print("Sent to a client")
    
start_server = websockets.serve(handleCard, '127.0.0.1', 1338)
asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_until_complete(send_message)
asyncio.get_event_loop().run_forever()
