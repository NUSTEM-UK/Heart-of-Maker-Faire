def sinedata(heartrate, fps):
    """Returns sine wave to fill animation sequence.

    Takes heartrate and fps data; returns list of normalised
    sine wave, in range 0...254.
    """
    import math

    # heartrate = 85.0
    # fps = 60
    number_frames = (60 * fps) / heartrate
    # print "Number of frames: ", number_frames

    y = []
    angle = 0
    normalised_sin_angle = 0

    for frame in range(int(number_frames)):
        angle = math.radians((360.0/number_frames)*frame)
        normalised_sin_angle = (math.sin(angle) + 1) * 127
        y.append(int(normalised_sin_angle))

        # y.append((math.sin(math.radians((360.0/number_frames)*frame)) + 1)
        #          * 127)
        # print frame, y

    return y
