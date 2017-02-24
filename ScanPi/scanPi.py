# modules
from picamera import *
from PIL import Image
import zbarlight
from gpiozero import LightSensor, LED, Button
import serial
import time
from collections import Counter
import sys, os
import random
import paho.mqtt.publish as publish
import pickle
import re # for turning the styring into a int
from statistics import mode

# setup
# setup for the PiCamera to record the QR codes
camera = PiCamera()
camera.resolution = (1024, 768)
file_path = "newQR.png"

# setup the LDR to detect presence of a heart
# the sensor is on Pin19, a charge_time_limit is chosen to suit the capacitor (220uF)
# the threshold ensures the clear jar can be detected
ldr = LightSensor(18, charge_time_limit=0.3, threshold = 0.2)
# these LEDS (on Pin17,16) represent the relays controlling illumination at the stations
qrscannerlight = LED(17)
hrscannerlight = LED(27)
# heart placed button on pin 4
heartButton = Button(21)

# set the filename of this run
ratesfilename = "rates" + time.strftime("%Y%m%d-%H%M%S") + ".p"
print("Rates Filename is %s" % ratesfilename)
qrsfilename = "qrs" + time.strftime("%Y%m%d-%H%M%S") + ".p"
print("QRs Filename is %s" % qrsfilename)

# functions
def QRread():
# take image of the QR code and save
    print("Capturing  image")
    camera.capture("newQR.png")
    print("Image caputred")
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
        print(type(QRint))
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
            print("oops")

def MQTTsend(location, status, data):
# turn the data into a string
    #print("Sednding data to MQTT")
    MQQTString = str(location) + '-' + str(status) + '-' + str(data)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect('localhost', 1883)
    mqttc.publish("homf/update", MQQTString)
    #print("Sccuess")

# decide whether to load previously saved data
if len(sys.argv) > 2:
    print("Loading pickles")
    QRmap = pickle.load(open(sys.argv[2], "rb"))
    heartRateStore = pickle.load(open(sys.argv[3], "rb"))
    for i in range(len(QRmap)):
        MQTTsend( i, 2, heartRateStore[i])
    print(QRmap)
    print(heartRateStore)
else:
    QRmap = [0] * int(sys.argv[1])
    print("QR Map created")
    heartRateStore = [0] * int(sys.argv[1])
    print("HR Store created")

while True:
    repeatcode = False
    # turn on heart scanner light
    print("Turning light on...")
    time.sleep(0.5)
    qrscannerlight.on()

    # wait for a heart to be placed
    if (ldr.light_detected == False):
        print("Jar detected")

        # read the QR on the heart
        scannedQR = QRread()
        if scannedQR == False:
            print("Remove and reposition your heart cell")
            ldr.wait_for_light()
            continue
        else:
            print("Successful scan, qr is %s" % scannedQR)

        # check if we already have this HR stored
        for i in QRmap:
            if i == scannedQR:
                print("Code repetition")
                repeatcode = True

        #loop until an empty cell is found
        if repeatcode == False:
            while True:

                #choose a random position in the map
                INDEX = random.randint(0, len(QRmap)-1)

                #check if that random position is empty (ie 0)
                if QRmap[INDEX] == 0:

                    #add the QR code to the position
                    QRmap[INDEX] = scannedQR
                    location = INDEX
                    print(QRmap)
                    for i in QRmap:
                        print(i)
                    break

            # turn off the heart scanner Light
            qrscannerlight.off()

            # turn on the heart rate sensor Light
            hrscannerlight.on()

            # get heart rate data
            heartrate = getheartrate()

            #heartrate = 75
            print("We've got a heart rate = %s" % heartrate)
            # place the heart rate into the save file list
            heartRateStore[INDEX] = heartrate
            # turn off the heart scanner light
            hrscannerlight.off()
            # send the cell location, status and heart rate to the mqtt
            MQTTsend ( location, 1, heartrate)
            # wait for the confirmation button to be pressed
            print("Waiting for button")
            heartButton.wait_for_press()
            # send the new status to the MQTT
            print("Button pressed, sending confirmation")
            MQTTsend ( location, 0, heartrate)
            # save the data to the revelant file
            print("Dumping pickles")
            pickle.dump(QRmap, open(qrsfilename, "wb"))
            pickle.dump(heartRateStore, open(ratesfilename, "wb"))
            print("Pickles have been dumped")
        else:
            print("Do something")
    else:
        print("Jar not detected")
    print("End of loop")
