from RPi import GPIO
from time import sleep
from microdotphat import *
from gpiozero import LED, Button

# setup the LED pins for the Rotary Encoder, common anode so active_high = False
green = LED(8, active_high=False)
red = LED(11, active_high=False)
blue = LED(10, active_high=False)

# setup the LED pins for the 'Go' button, common anode so active_high = False
greenB = LED(5, active_high=False)
redB = LED(6, active_high=False)
blueB = LED(13, active_high=False)

# the 'go' button sits on pin 26
button = Button(26)

# the Encoder pins are on 27 and 17.
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
        redB.off()
        blueB.off()
        greenB.off()
    counter = 40
    clkLastState = GPIO.input(clk)
    while True:
        clear()
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                if int(counter/2) > 240:
                    counter = 240
            else:
                counter -= 1
                if counter < 40:
                    counter = 40

# Add the leading spaces
            if len(str(counter/2)) == 1:
                countString = "  " + str(counter/2)
            elif len(str(counter/2)) == 2:
                countString = " " + str(counter/2)
            else:
                countString = str(counter/2)
            print(countString)
            write_string(countString, kerning=False)
            show()

        clkLastState = clkState
        sleep(0.001)
        if button.is_pressed:
            print('Button pressed')
            return counter/2

if __name__ == '__main__':
    encoder('magenta')
