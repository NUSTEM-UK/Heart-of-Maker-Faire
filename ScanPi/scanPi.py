# modules
import time
from picamera import *
from PIL import Image
import zbarlight
from gpiozero import LightSensor, LED, Button
import serial
import sys
import paho.mqtt.client as mqtt
from statistics import mode
from homfsql import *
#from heartprint import *
from Adafruit_Thermal import *
from homf_neopixels import *
from neopixel import *
from pulsevalues import frames

# setup
# setup for the PiCamera to record the QR codes
camera = PiCamera()
camera.resolution = (1024, 768)
file_path = "newQR.png"

# get the initial programme start time for our delay-less Neopixel update
last_time_checked = int(round(time.time()*1000))
frame = 0

#setup the neo pixel strip
# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#set up the neopixel strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

# setup the LDR to detect presence of a heart
# the sensor is on Pin19, a charge_time_limit is chosen to suit the capacitor (220uF)
# the threshold ensures the clear jar can be detected
ldr = LightSensor(12, charge_time_limit=0.2, threshold = 0.5)
# these LEDS (on Pin17,16) represent the relays controlling illumination at the stations
qrscannerlight = LED(17)
hrscannerlight = LED(27)
# heart placed button on pin 4
heartButton = Button(21)

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
    ser = serial.Serial('/dev/ttyACM0', 9600)
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
            # cut the unecessary gubbins off the  serial_line
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
    MQQTString = str(location) + '-' + str(status) + '-' + str(data)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect('localhost', 1883)
    mqttc.publish("homf/update", MQQTString)

# connect to the SQL database
conn = create_connection("homf.db")

try:
    loadNew = sys.argv[1]
    if loadNew == "y":
        print("Storing old data")
        store_old_data(conn)
except:
    print("No argument")

while True:
    repeatcode = False
    # turn on heart scanner light
    qrscannerlight.on()
    last_time_checked, frame = pulselight(last_time_checked, frame)
    for i in range(8):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.setBrightness(frames[int(frame)])
    strip.show()
    # wait for a heart to be placed
    if (ldr.light_detected == False):
        print("Jar detected")
        for i in range(8):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        # read the QR on the heart
        scannedQR = QRread()
        if scannedQR == False:
            print("Remove and reposition your heart cell")
            ldr.wait_for_light()
            continue
        else:
            print("Successful scan, qr is %s" % scannedQR)

        # check if we already have this HR stored
        repeatcode = QR_usage_checker(conn, scannedQR)
        print(repeatcode)
        #loop until an empty cell is found
        if repeatcode == True:
            cell_num = unique_cell_picker(conn)
            update_heart(conn, cell_num, scannedQR, 0)

            # turn off the heart scanner Light
            qrscannerlight.off()
            # turn on the heart rate sensor Light
            hrscannerlight.on()

            # get heart rate data
            heartrate = getheartrate()
            # update SQL avoiding corruption
            update_heart(conn, cell_num, scannedQR, heartrate)

            print("We've got a heart rate = %s" % heartrate)

            # turn off the heart scanner light
            hrscannerlight.off()
            # send the cell location, status and heart rate to the mqtt
            MQTTsend (cell_num, 1, heartrate)

            #qrprintout(heartrate, scannedQR)
            # wait for the confirmation button to be pressed
            print("Waiting for button")
            # heartButton.wait_for_press()
            # send the new status to the MQTT
            print("Button pressed, sending confirmation")
            MQTTsend (cell_num, 0, heartrate)
            # save the data to the revelant file

        else:
            # What do we do when we see a repeated code
            print("Do something")
    else:
        pass
        #print("Jar not detected")
    #print("End of loop")
