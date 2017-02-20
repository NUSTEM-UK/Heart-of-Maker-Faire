#Import the necessary modules
from gpiozero import LightSensor
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from PIL import Image
import zbarlight

# I'm using a 220 microfarad capicitor so charge time of 0.3 is needed
# Threshold adjust for the plastic tubs that will be used to cover
# the LDR
ldr = LightSensor(18, charge_time_limit=0.3, threshold = 0.2)

# Setup the PiCamera
camera = PiCamera()
camera.resolution = (1024, 768)

file_path = "newQR.png"

detect = True

while True:
    if (ldr.light_detected == False) and (detect == True):
        detect = False
        print("We have detected your heart")
        
        time.sleep(1)
        camera.capture("newQR.png")
        
        print("Processing")
            
        with open(file_path, 'rb') as image_file:
            image = Image.open(image_file)
            image.load()
        codes = zbarlight.scan_codes('int', image)
        print ("Your heart is stored in jar number: %s" % codes)
        time.sleep(3)
        print(int(codes[0]))
           
    elif ldr.light_detected != True and detect == False:
        print("Please remove your heart")
        time.sleep(1)
    else:
        print("No heart detected")
        time.sleep(1)
        detect = True
