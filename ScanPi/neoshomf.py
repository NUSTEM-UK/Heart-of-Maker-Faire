""" Insert links to Neopixel on Raspberry Pi guidance, in github and on Adafruit
This needs to be imported as sudo"""

import time
from neopixel import *
from pulsevalueshomf import *

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, 800000, 5, False, 255) # neopixel setup
strip.begin()

colourDict = {'green':(255,0,0), 'yellow':(255,255,0), 'magenta':(0,255,255), 'cyan':(255,0,255), 'blank':(0,0,0), 'red':(0,255,0)}

def countdown():
    for i in range(16,32):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(28/16)

def millis():   # a function to return the current time in millis
    millis = int(round(time.time()*1000))
    return millis

def ringSelect(strip, colour, ring, update):
    if ring == 1:
        for i in range(16):
            strip.setPixelColor(i, Color(colourDict[colour][0],colourDict[colour][1],colourDict[colour][2],))
        for i in range(16,32):
            strip.setPixelColor(i, Color(0,0,0))
    else:
        for i in range(16):
            strip.setPixelColor(i, Color(0,0,0))
        for i in range(16,32):
            strip.setPixelColor(i, Color(colourDict[colour][0],colourDict[colour][1],colourDict[colour][2],))
    if update:
        strip.show()

def pulselight(strip, lasttime, count, rate):
    time.sleep(0.005)
    current_time = millis()
    #what is the elapsed time
    elap_time = current_time - lasttime
    # pulse length is 1 second
    pulse_length = 60/rate
    total_frames = 240
    frame_rate = float(total_frames / pulse_length)
    # multiply the frame rate by the elapsed time accounting for millis
    frames_passed = float(frame_rate * elap_time /1000)
    new_count = count + int(frames_passed)
    if new_count >=240:
        new_count = 0
    strip.setBrightness(frames[new_count])
    strip.show()
    return current_time, new_count


def neocleanup(strip):
    for i in range(32):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def main():

    ringSelect(strip, 'green', 1, True)
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
    while True:
        last_time_checked, frame = pulselight(strip, last_time_checked, frame, 100)


if __name__ == '__main__':
    try:
        main()
    finally:
        neocleanup(strip)
