from picamera import *
from PIL import Image
import zbarlight
from gpiozero import LightSensor, LED, Button
import serial
import time
# from collections import Counter
import sys, os
import random
import paho.mqtt.publish as publish
import re # for turning the styring into a int
from statistics import mode
from homfsql import *

# functions
def QRread():
    # take image of the QR code and save
    print("Capturing  image")
    camera.capture("newQR.png")
    print("Image captured")
    # open the image file for use by zbarlight
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    # use zbarlight to scan the QR image for codes
    code = zbarlight.scan_codes('qrcode', image)

    if code is None:
        print("QR code is None Type")
        return False

    else:
        QRstr = str(code[0])
        QRint = int(QRstr[2:len(QRstr)-1])
        return QRint

def getheartrate():
    # open the serial connetion, you'll need to find the port and baud rate
    ser = serial.Serial('/dev/ttyACM1', 9600)
    print("HR connection successful")
    # create an empty array
    RecentHrs = [0] * 5
    print(RecentHrs)
    while True:
        # read the current line of the serial connection from the arduino
        try:
            serial_line = str(ser.readline())
            time.sleep(0.1)
            size = len(serial_line)
            newSerial = int(serial_line[2:(size-5)])
            print("BPM %s" % newSerial)
            # add the new HR data to the end of the list
            RecentHrs.append(newSerial)
            # remove the oldest data from the list (first in the list)
            del RecentHrs[0]
            # find the range of the heart rate list
            RANGE = max(RecentHrs) - min(RecentHrs)
            print("Range is currently %s" % RANGE)
            # is the range less than three?
            if RANGE < 3 and 50 < newSerial < 150:
                # count the data, close the serial connetion and return the most common HR value
                data = mode(RecentHrs)
                ser.close()
                print("The selected heart rate is: %s" % data)
                return int(data)
            time.sleep(0.1)
        except ValueError:
            print("ValueError, retrying")

def MQTTsend(location, status, data):
    # turn the data into a string
    MQQTString = str(location) + '-' + str(status) + '-' + str(data)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect('localhost', 1883)
    mqttc.publish("homf/update", MQQTString)
