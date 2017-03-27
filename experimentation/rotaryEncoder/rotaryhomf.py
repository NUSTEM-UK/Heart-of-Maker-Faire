from RPi import GPIO
from gpiozero import Button
from time import sleep, time
from microdotphat import write_string, set_decimal, clear, show
#from neoshomf import *

clkPin = 27
dtPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(clkPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dtPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#button = Button(8)

#def setEncoderColour(colour):
 #   if colour == 'cyan':
   #     #set colour to blue
  #  elif colour == 'yellow':
#
  #  elif colour == '???'
#
#    else:


def heartEncoder():
    counter = 40
    clkLastState = GPIO.input(clkPin)
    #clear()
    #last_time_checked = int(round(time.time()*1000))
    while True:
        #last_time_checked, frame = pulselight(strip, last_time_checked, frame, 60/counter) # Can I make the neopixel ring pulse with HR
        clkState = GPIO.input(clkPin)
        dtState = GPIO.input(dtPin)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
        clkLastState = clkState
        write_string(str(int(counter/2)), kerning = False)
        show()
        #if button.is_pressed():
         #   # do a triple flash
         #   return counter
        #sleep(0.001)
while True:
    heartEncoder()
