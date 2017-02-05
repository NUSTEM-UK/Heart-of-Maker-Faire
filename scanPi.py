# load all the necessary modules
from gpiozero import LightSensor
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from PIL import Image
import zbarlight
import serial

# decide whether to load previously saved data
#loadSavedData = raw_input("Do you wish to load previous data? y/n ")

# If saved data is to be loaded do...
#if loadSaved == 'y':

# input the total number of space in the Heart of Maker Faire
totalHearts = int(raw_input("What is the total number of heart cells?  "))
# Create the empty list HeartQR to store the QR mapping
heartCells = [0] * totalHearts
# Create the list emptyCells that will store any remaining empty cells
emptyCells = []
#fill them with the values 0 - totalHearts
for i in range(0,totalHearts):
    EmptyCells.append(i)

# setup the LDR to detect presence of a heart
# the sensor is on Pin19, a charge_time_limit is chosen to suit the capacitor (220uF)
# the threshold ensures the clear jar can be detected
ldr = LightSensor(19, charge_time_limit=0.3, threshold = 0.2)

# setup for the PiCamera to record the QR codes
camera = PiCamera()
camera.resolution = (1024, 768)
file_path = "newQR.png"

# Setup the Serial read to get HR from Arduino, adjust to suit settings
ser = serial.Serial('/dev/ttyUSB0', 9600)

# tell the code to check for a new heart placed on the LDR
QRdetect = True
# set the newQR checker to True,
newQR = True

# open the main loop
while True:
# three things can happen here:
# 2. the heart can now be removed
# 3. no heart is detected
    # 1. a new heart is detected
    if (ldr.light_detected == False) and (QRdetect == True):
        newQR = True
        detect = False

        # read the QR code
        QRread()

        # check if the code is already logged
        for i in heartCells:
            if code == i:
                print("We've already had this code")
                newQR = False

        # if QR is new
        if newQR == True:
            #check if there are any spaces left
            if not emptyCells:
                break
            else:
                # choose a random empty cell from the list
                heartPosition = random.choice(emptyCells)
                # remove the position from emptyCells to avoid repetition
                emptyCells.remove(heartPosition)
                # assign the QR code to the new position
                heartCells[heartPosition] = code






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
