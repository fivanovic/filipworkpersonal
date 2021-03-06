import time
import pigpio
pi = pigpio.pi()
RELAY1 = 26
RELAY2 = 20
RELAY3 = 21

BUTTON1 = 2
BUTTON2 = 3
BUTTON3 = 4

pi.set_mode(RELAY1,pigpio.OUTPUT)
pi.set_mode(RELAY2,pigpio.OUTPUT)
pi.set_mode(RELAY3,pigpio.OUTPUT)

pi.set_mode(BUTTON1,pigpio.OUTPUT)
pi.set_mode(BUTTON2,pigpio.OUTPUT)
pi.set_mode(BUTTON3,pigpio.OUTPUT)

class Relay:
    def __init__(self, numb, button, status, id):
        self.numb = numb
        self.button = button
        self.status = status
        self.id = id

R1 = Relay(RELAY1,BUTTON1,0,1)
R2 = Relay(RELAY2,BUTTON2,0,2)
R3 = Relay(RELAY3,BUTTON3,0,3)


def RelayController(rel, reloff1, reloff2):
    global R1
    global R2
    global R3

    print("Device %d Selected" % rel.id)
    pi.write(reloff1.numb, 1)
    pi.write(reloff2.numb, 1)
    pi.write(rel.numb,0)
    pi.gpio_trigger(rel.button, 10, 1) #needs to be looked at in terms of polarity of buttons and potential necessity of pullup resistor
    rel.status = 1
    #if reloff1.status == 1:
        #pi.gpio_trigger(reloff1.button, 10, 1)
        #reloff1.status = 0
    #if reloff2.status == 1:
        #pi.gpio_trigger(reloff2.button, 10 ,1)
        #reloff2.status = 0


def RelayClear(rel1, rel2, rel3):
    print("Clearing All relays, turning off all devices")
    #if rel1.status == 1:
        #pi.gpio_trigger(rel1.button, 10, 1)
        #rel1.status = 0
    #if rel2.status == 1:
        #pi.gpio_trigger(rel2.button, 10, 1)
        #rel2.status = 0
    #if rel3.status == 1:
        #pi.gpio_trigger(rel3.button, 10, 1)
        #rel3.status = 0
    pi.write(rel1.numb, 1)
    pi.write(rel2.numb, 1)
    pi.write(rel3.numb, 1)

while True:
    selection = input("Select Testing Device")
    if selection == "1":
        RelayController(R1,R2,R3)

    elif selection == "2":
        RelayController(R2,R1,R3)

    elif selection == "3":
        RelayController(R3,R2,R1)

    elif selection == "4":
        RelayClear(R1,R2,R3)
    else:
        print("Please select 1, 2 or 3. Press 4 to clear all relays")
