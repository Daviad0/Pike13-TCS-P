from mfrc522 import SimpleMFRC522 as SMFRC
import RPi.GPIO as GPIO
from time import sleep as wait

GPIO.setwarnings(False)

r = SMFRC()

while True:
    try:
        c = input("Content to Write: ")
        r.write(c)
    except:
        print("ERROR")
        wait(1)