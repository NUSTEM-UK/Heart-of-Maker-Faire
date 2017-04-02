from RPi import GPIO
from time import sleep
from microdotphat import *
from gpiozero import LED, Button
from neoshomf import *
from sqlhomf import *

# setup the LED pins for the Rotary Encoder, common anode so active_high = False
green = LED(16, active_high=False)
red = LED(20, active_high=False)
blue = LED(21, active_high=False)

# setup the LED pins for the 'Go' button, common anode so active_high = False
greenB = LED(5, active_high=False)
redB = LED(6, active_high=False)
blueB = LED(12, active_high=False)

# the 'go' button sits on pin 26
button = Button(26)
shortButton = Button(24)
# the Encoder pins are on 27 and 17.
clk = 27
dt = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def error(code):
    code = str(code)
    clear()
    write_string(code, kerning = False)
    show()
    sleep(2)
    clear()
    show()

def encoder(colour, cellNum):
    clear()
    write_string('60', kerning=False)
    show()
    ringSelect(strip, colour, 0, True)
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
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
        redB.off()
        blueB.on()
        greenB.on()
    elif colour == 'green':
        redB.off()
        blueB.off()
        greenB.on()
    else:
        redB.off()
        blueB.off()
        greenB.off()
    counter = 120
    clkLastState = GPIO.input(clk)
    while True:
        #last_time_checked, frame = pulselight(strip, last_time_checked, frame, counter/2)
        clear()
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                if int(counter/2) > 240:
                    counter = 480
            else:
                counter -= 1
                if counter < 80:
                    counter = 80

# Add the leading spaces
            #print(len(str(int(counter/2))))
            if len(str(int(counter/2))) == 2:
                countString = "   " + str(int(counter/2))
            else:
                countString = "  " + str(int(counter/2))
            write_string(countString, kerning=False)
            show()

        clkLastState = clkState
        #sleep(0.001)
        if button.is_pressed:
            if shortButton.is_pressed:
                release(conn,cellNum)
                redB.off()
                blueB.off()
                greenB.off()
                red.off()
                blue.off()
                green.off()
                clear()
                show()
                neocleanup(strip)
                return False
            else:
                print('Button pressed')
                redB.off()
                blueB.off()
                greenB.off()
                red.off()
                blue.off()
                green.off()
                clear()
                show()
                return int(counter/2)

if __name__ == '__main__':

    encoder('green',56)

    #print(encoder('magenta'))
    neocleanup(strip)
