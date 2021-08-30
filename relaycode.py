import time
import pigpio
pi = pigpio.pi()
RELAY1 = 26
RELAY2 = 20
RELAY3 = 21
pi.set_mode(RELAY1,pigpio.OUTPUT)
pi.set_mode(RELAY2,pigpio.OUTPUT)
pi.set_mode(RELAY3,pigpio.OUTPUT)

BUTTON1 = 2
BUTTON2 = 3
BUTTON3 = 4

while True:
    selection = input("Select Testing Device")
    if selection == "1":
        print("Device 1 Selected")
        
