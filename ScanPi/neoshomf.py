""" Insert links to Neopixel on Raspberry Pi guidance, in github and on Adafruit
This needs to be imported as sudo"""

import time
from neopixel import *
from pulsevalueshomf import *

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255) # neopixel setup
strip.begin()

colourDict = {'green':(0,255,0), 'yellow':(255,255,0), 'purple':(0,255,255), 'cyan':(255,0,255), 'blank':(0,0,0)}

def millis():   # a function to return the current time in millis
    millis = int(round(time.time()*1000))
    return millis

def ringSelect(strip, colour, ring, update):
    if ring == 1:
        for i in range(16):
            strip.setPixelColor(i, Color(colourDict[colour]))
        for i in range(16,32):
            strip.setPixelColor(i, Color(colourDict['blank']))
    else:
        for i in range(16):
            strip.setPixelColor(i, Color(colourDict['blank']))
        for i in range(16,32):
            strip.setPixelColor(i, Color(colourDict[colour]))
    if update:
        strip.show()

def pulsefeedback (strip, spread):
    for i in range(8):
        strip.setPixelColor(i, Color(0,0,0))
    if 30 <= spread < 60:
        for i in range(9,10):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(10,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif 10 <= spread < 30:
        for i in range(9,12):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(12,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif 3 <= spread < 10:
        for i in range(9,14):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(14,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif spread < 3:
        for i in range(8,16):
            strip.setPixelColor(i, Color(255,0,0))
    else:
        for i in range(9,16):
            strip.setPixelColor(i, Color(0,255,0))
    strip.show()

def pulselight(strip, lasttime, count, rate):
    time.sleep(0.01)
    current_time = millis()
    #what is the elapsed time
    elap_time = current_time - lasttime
    # pulse length is 1 second
    pulse_length = rate
    total_frames = 240
    frame_rate = total_frames / pulse_length
    # multiply the frame rate by the elapsed time accounting for millis
    frames_passed = float(frame_rate * elap_time /1000)
    new_count = count + int(frames_passed)
    if new_count >=240:
        new_count = 0
    strip.setBrightness(frames[new_count])
    strip.show()
    return current_time, new_count

def setColour(strip, colour, location, show): # colour 'red', 'blue', 'green', 'black'
    strip.setBrightness(255)
    if location == 1:
        if colour == 'red':
            for i in range(8):
                strip.setPixelColor(i, Color(0,255,0))
            for i in range(8,16):
                strip.setPixelColor(i, Color(0,0,0))
            strip.show()
        elif colour == 'blue':
            for i in range(8):
                strip.setPixelColor(i, Color(0,0,255))
            for i in range(8,16):
                strip.setPixelColor(i, Color(0,0,0))
        elif colour == 'green':
            for i in range(8):
                strip.setPixelColor(i, Color(255,0,0))
            for i in range(8,16):
                strip.setPixelColor(i, Color(0,0,0))
        else:
            for i in range(16):
                strip.setPixelColor(i, Color(0,0,0))
    else:
        if colour == 'red':
            for i in range(8, 16):
                strip.setPixelColor(i, Color(0,255,0))
            for i in range(8):
                strip.setPixelColor(i, Color(0,0,0))
            strip.show()
        elif colour == 'blue':
            for i in range(8, 16):
                strip.setPixelColor(i, Color(0,0,255))
            for i in range(8):
                strip.setPixelColor(i, Color(0,0,0))
        elif colour == 'green':
            for i in range(8, 16):
                strip.setPixelColor(i, Color(255,0,0))
            for i in range(8):
                strip.setPixelColor(i, Color(0,0,0))
        else:
            for i in range(16):
                strip.setPixelColor(i, Color(0,0,0))
    if show == True:
        strip.show()
    else:
        pass

def neocleanup(strip):
    setColour(strip, 'blank', 1, True)

def hrblink(strip):
    strip.setBrightness(255)
    strip.setPixelColor(8, Color(0,255,0))
    strip.show()
    time.sleep(0.1)
    strip.setPixelColor(8, Color(0,0,0))
    strip.show()
    time.sleep(0.1)

def main():
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
    while True:
        setColour(strip, 'green', 1, False)
        last_time_checked, frame = pulselight(strip, last_time_checked, frame)

if __name__ == '__main__':
    try:
        main()
    finally:
        neocleanup(strip)
