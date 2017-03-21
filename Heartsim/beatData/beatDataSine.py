"""Output 240 frames of lovely sine-wave goodness."""

import math

samples = 240

for i in xrange(240):
    mag = math.sin((2 * math.pi * i)/240) + 2
    scaledMag = mag * 30.0
    roundedScaledMag = round(scaledMag)
    print(str(int(roundedScaledMag)) + ",")
