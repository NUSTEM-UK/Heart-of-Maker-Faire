import serial, time
from collections import Counter

def getheartrate():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    RECENT_HRS = [0] * 10
    while True:
        serial_line = ser.readline()
# add the new HR data to the end of the list
        RECENT_HRS.append(serial_line)
# remove the oldest data from the list
        del RECENT_HRS[0]
        RANGE = max(RECENT_HRS) - min(RECENT_HRS)

        if RANGE < 2:
            data = Counter(RECENT_HRS)
            return data.most_common



    ser.close()
