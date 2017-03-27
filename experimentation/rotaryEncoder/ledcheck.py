from RPi import GPIO
from time import sleep
from microdotphat import *

from gpiozero import LED, Button

green = LED(8, active_high=False)
red = LED(11, active_high=False)
blue = LED(10, active_high=False)


greenB = LED(5, active_high=False)
redB = LED(6, active_high=False)
blueB = LED(13, active_high=False)

button = Button(26)

clk = 27
dt = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def encoder(colour):
    red.on()
    blue.off()
    green.off()
    if colour == 'magenta':
        redB.on()
        blueB.on()
        greenB.off()
    elif colour == 'yellow':
        redB.on()
        blueB.off()
        greenB.on()
    elif colour == 'cyan':
        redB.on()
        blueB.off()
        greenB.on()
    elif colour == 'green':
        redB.on()
        blueB.off()
        greenB.on()
    else:
        redB.on()
        blueB.off()
        greenB.on()
    counter = 40
    clkLastState = GPIO.input(clk)
    while True:
        clear()
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            countString = " " + str(counter/2)
            print(countString)
            write_string(countString, kerning=False)
            show()

        clkLastState = clkState
        sleep(0.001)
        if button.is_pressed:
            print('Button pressed')
            return True

if __name__ == '__main__':
    encoder('magenta')
