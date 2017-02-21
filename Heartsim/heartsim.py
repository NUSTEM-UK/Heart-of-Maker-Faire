"""First animation attempt, using Python / OPC / FadeCandy.

Let's light this sucker up.
"""

import opc
import time
from generate_pulse import sinedata

# ...because we're using the last LEDs on the FadeCandy. [facepalm]
numLEDs = 512
LEDstart = 448
LEDstop = 512

# Fire up the OPC connection
ADDRESS = "localhost:7890"
# Create a client object
client = opc.Client(ADDRESS)

# Initialise the pixel data structure
pixels = [(0, 0, 0)] * numLEDs

# Now let's populate some heartbeat data
hearts = []
number_of_hearts = 12
for heart in range(number_of_hearts):
    # 60 to 180 bpm
    heartrate = 60 + 10*heart
    fps = 60.0
    hearts.append(sinedata(heartrate, fps))
    # print "Heart: ", heart, "Frames: ", len(hearts[heart])

framecount = 0
maxframes = 5000

# time.sleep(3)

for framecount in xrange(maxframes):
    for i in range(number_of_hearts):
        brightness = hearts[i][framecount % len(hearts[i])]
        pixel_start = LEDstart + (i*5)
        for pixel in range(5):
            pixels[pixel_start + pixel] = (brightness, 0, 0)
    client.put_pixels(pixels)
    # time.sleep(1/fps)

pixels = [(0, 0, 0)] * numLEDs
client.put_pixels(pixels)
