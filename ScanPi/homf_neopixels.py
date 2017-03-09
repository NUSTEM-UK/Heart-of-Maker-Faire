import time
from neopixel import *


# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def pulsing():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 255))
    for i in range
    for j in range(20):
        strip.setBrightness((10*j)+55)
        strip.show()
        time.sleep(0.04)
    for k in range(20):
        strip.setBrightness(255-(10*k))
        strip.show()
        time.sleep(0.04)

if __name__ == '__main__':
    try:
        #set up the neopixel strip
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        
        while True:
            pulsing()
        
        while False:
            for i in range(8):
                strip.setPixelColor(i, Color(255, 0, 0))
                strip.show()
                time.sleep(1)
                
            strip.setBrightness(0)
            
            for i in range(LED_COUNT):
                strip.setPixelColor(i, Color(0, 255, 0))
                time.sleep(1)
                strip.show()
    except KeyboardInterrupt:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
