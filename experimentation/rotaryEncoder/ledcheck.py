from RPi import GPIO
from time import sleep

from gpiozero import LED

red = LED(21, active_high=False)
blue = LED(22, active_high=False)
green = LED(20, active_high=False)

clk = 18
dt = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

try:

        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print counter/2
                if counter/2 < 10:
                    red.on()
                    green.off()
                    blue.off()
                elif 10 <= counter/2 < 20:
                    red.off()
                    green.on()
                    blue.off()
                elif 20 <= counter/2 < 30:
                    red.off()
                    green.off()
                    blue.on()
                else:
                    red.off()
                    green.off()
                    blue.off()
                clkLastState = clkState
                sleep(0.001)
finally:
        GPIO.cleanup()
