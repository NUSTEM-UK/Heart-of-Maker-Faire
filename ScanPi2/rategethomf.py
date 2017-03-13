import serial   # for connection with the Arduino HR reader
import time
from homf-neos import *
from statistics import mode

ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'


def getheartrate():
    ser.open()
    RecentHrs = [0] * 5
    while True:
        try:
            serial_line = str(ser.readline())
            newSerial = int(serial_line[2:(len(serial_line)-5)])# cut the unecessary gubbins off the  serial_line
            print(newSerial)
            RecentHrs.append(newSerial) # add the new HR data to the end of the list
            del RecentHrs[0] # remove the oldest data from the list (first in the list)
            RANGE = max(RecentHrs) - min(RecentHrs) # find the range of the heart rate list

            pulsefeedback(RANGE) # visual light feedback for heart rate

            if RANGE < 3 and 50 < newSerial < 150:
                time.sleep(0.5) # keep the green light on for a moment
                data = mode(RecentHrs) # get the mode of the data
                ser.close() # close the connection
                return int(data) # return the HR data
            time.sleep(0.1)
        except ValueError: # mitigate for serial errors
            pass

if __name__ == '__main__':
    try:
        getheartrate()
    except:
        print("Error")
