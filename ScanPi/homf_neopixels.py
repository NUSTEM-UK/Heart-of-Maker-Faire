import time
from neopixel import *
from pulsevalues import frames

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# get the initial programme start time for our delay-less Neopixel update
init_time = int(round(time.time()*1000))

def millis():
    millis = int(round(time.time()*1000))
    return millis

def get_frame(time0):
    prog_time = millis() - time0
    # the pulse cycle is 1 second, so find out what fraction we are through that cycle
    sec_time = prog_time % 1000
    # there are 240 diffrent sbrightness settings in the cycle, work out which one we're on
    frame_count = sec_time % 240
    return frame_count


if __name__ == '__main__':
    try:
        #set up the neopixel strip
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(255, 0, 0))

        while True:
            count = get_frame(init_time)
            strip.setBrightness(frames[count])
            strip.show()

    except KeyboardInterrupt:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
