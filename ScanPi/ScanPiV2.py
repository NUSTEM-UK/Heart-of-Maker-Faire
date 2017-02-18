# modules
from picamera import *
from PIL import Image
import zbarlight
from gpiozero import LightSensor, LED, Button
import serial
import time
from collections import Counter
import sys
import random
import paho.mqtt.client as mqtt

# setup
# setup for the PiCamera to record the QR codes
camera = PiCamera()
camera.resolution = (1024, 768)
file_path = "newQR.png"

# setup the LDR to detect presence of a heart
# the sensor is on Pin19, a charge_time_limit is chosen to suit the capacitor (220uF)
# the threshold ensures the clear jar can be detected
ldr = LightSensor(19, charge_time_limit=0.3, threshold = 0.2)
# these LEDS (on Pin17,16) represent the relays controlling illumination at the stations
qrscannerlight = LED(17)
hrscannerlight = LED(16)
# heart placed button on pin 4
heartButton = Button(4)

# functions
def QRread ():
# take image of the QR code and save
    camera.capture("newQR.png")
# open the image file for use by zbarlight
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
# use zbarlight to scan the QR image for codes
    code = zbarlight.scan_codes('qrcode', image)
    return code

def getheartrate():
# open the serial connetion, you'll need to find the port and baud rate
    ser = serial.Serial('/dev/ttyUSB0', 9600)
# create an empty array
    RecentHrs = [0] * 10
    while True:
# read the current line of the serial connection from the arduino
        serial_line = ser.readline()
# add the new HR data to the end of the list
        RecentHrs.append(serial_line)
# remove the oldest data from the list (first in the list)
        del RecentHrs[0]
# find the range of the heart rate list
        RANGE = max(RecentHrs) - min(RecentHrs)
# is the range less than two?
        if RANGE < 2:
# count the data, close the serial connetion and return the most common HR value
            data = Counter(RecentHrs)
            ser.close()
            return data.most_common
        time.sleep(0.1)

def MQTTsend (location, status, data):
# turn the data into a string
    MQQTString = str(location) + '-' + str(status) + '-' + str(data)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect('localhost', 1883)
    mqttc.publish("homf/update", MQQTString)

# decide whether to load previously saved data
if len(sys.argv) > 2:
    pass
else:
    QRmap = [0] * sys.argv[1]

while True:
# turn on heart scanner light
    qrscannerlight.on()
# wait for a heart to be placed
    if (ldr.light_detected == False):
# read the QR on the heart
        scannedQR = QRread()
# check whether the QR is new or already in use
        for i in QRmap:
            if scannedQR == QRmap[i]:
                pass
            else:
#loop until an empty cell is found
                while True:
#choose a random position in the map
                    INDEX = random.randint(0, len(QRmap)-1)
#check if that random position is empty (ie 0)
                    if QRmap[INDEX] == 0:
#add the QR code to the position
                        QRmap[INDEX] = scannedQR
                        location = INDEX
                        break
# turn off the heart scanner Light
                qrscannerlight.off()
# turn on the heart rate sensor Light
                hrscannerlight.on()
# get heart rate data
                heartrate = getheartrate()
# turn off the heart scanner light
                hrscannerlight.off()
# send the cell location, status and heart rate to the mqtt
                MQTTsend (location, 1, heartrate)
# wait for the confirmation button to be pressed
                heartButton.wait_for_press()
# send the new status to the MQTT
                MQTTsend (location, 0, heartrate)
