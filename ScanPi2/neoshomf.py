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

def millis():   # a function to return the current time in millis
    millis = int(round(time.time()*1000))
    return millis

def pulsefeedback (strip, spread):
    for i in range(8):
        strip.setPixelColor(i, Color(0,0,0))
    if 30 <= spread < 60:
        for i in range(8,10):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(10,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif 10 <= spread < 30:
        for i in range(8,12):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(12,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif 3 <= spread < 10:
        for i in range(8,14):
            strip.setPixelColor(i, Color(255,0,0))
        for i in range(14,16):
            strip.setPixelColor(i, Color(0,255,0))
    elif spread < 3:
        for i in range(8,16):
            strip.setPixelColor(i, Color(255,0,0))
    else:
        for i in range(8,16):
            strip.setPixelColor(i, Color(0,255,0))
    strip.show()

def pulselight(strip, lasttime, count):
    current_time = millis()
    #what is the elapsed time
    elap_time = current_time - lasttime
    # pulse length is 1 second
    pulse_length = 2
    total_frames = 240
    frame_rate = total_frames / pulse_length
    # multiply the frame rate by the elapsed time accounting for millis
    frames_passed = float(frame_rate * elap_time /1000)
    new_count = count + frames_passed
    if new_count >=240:
        new_count = 0
    strip.setBrightness(frames[frame])
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

if __name__ == '__main__':
    print("Testing the millis() function...")
    current_time = millis()
    print("Current time is %s" % current_time)
    print("")
    print("Testing the pulse feedback() function")
    pulses = [80,40,17,5,2]
    for i in pulses:
        print("Heart rate %s" % i)
        pulsefeedback(strip, i)
        time.sleep(1)
    print("Test complete")
    print("")
    print("Testing the setColour() function")
    colours = ['red', 'blue', 'green', 'black']
    for i in colours:
        setColour(strip, i, 1, True)
        time.sleep(1)
    print("Colour test complete")
