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
last_time_checked = int(round(time.time()*1000))
frame = 0
def millis():
    millis = int(round(time.time()*1000))
    return millis

def pulselight(lasttime, count):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(255, 0, 0))
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
    time.sleep(0.01)
    if new_count >=240:
        new_count = 0
    strip.setBrightness(frames[int(frame)])
    strip.show()
    return current_time, new_count


if __name__ == '__main__':
    try:
        #set up the neopixel strip
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        while True:
            last_time_checked, frame = pulselight(last_time_checked, frame)


    except KeyboardInterrupt:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
