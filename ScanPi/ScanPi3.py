""" The ScanPi programme reads a QR code from the heart jar and assigns it
a cell in wall. A heart rate is read from serial via an Arduino. The data is
stored in and SQL database and is pushed to the Heart via MQTT"""

# Module imports
import time # used in various functions
import serial   # for connection with the Arduino HR reader
import sys # for initial loading of arguemnts from command line

from picamera import *  # Raspberry Pi camera
from gpiozero import LightSensor # The gpio Lightsensor

import zbarlight # to decode the QR code
from PIL import Image # to decode the QR code

import paho.mqtt.client as mqtt
from statistics import mode

from homf-sql import *  # import the sqlite3 functions
from Adafruit_Thermal import *  # import the base code for the thermal printer

from homf-pixels import * # import the custom Neopixel functions
from homf-pulsevalues import frames



def main():
    # setup functions
    camera = PiCamera() # picamera setup
    camera.resolution = (1024, 768)
    file_path = "newQR.png"
    strip = Adafruit_NeoPixel(8, 18, 800000, 5, False, 255) # neopixel setup
    strip.begin()
    ldr = LightSensor(12, charge_time_limit=0.2, threshold = 0.5) # LDR sensor
    conn = create_connection("homf.db") # SQL database connection
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
    repeatcode = False # set the QR repetition bool to False
    ser = serial.Serial('/dev/ttyACM0', 9600) # initialise serial reader

    loadNew = sys.argv[1]     # check command line arguments
    try:
        if loadNew == "y":
            print("Storing old data")
            store_old_data(conn)
    except:
        print("Using previous data")

    while True:
        last_time_checked, frame = pulselight(last_time_checked, frame) # get the current pulse frame
        for i in range(8):
            strip.setPixelColor(i, Color(255, 0, 0)) # set the first 8 pixels to green
        for i in range(8, 16):
            strip.setPixelColor(i, Color(0, 0, 0)) # set the next 8 pixels to blank
        strip.setBrightness(frames[int(frame)]) # set the brightness to the correct avlue for the pulse
        strip.show()

        if (ldr.light_detected == False): # a heart has been placed on the scanner
            for i in range(8):  # turn the lights of on the heart detector
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            scannedQR = QRread()    # read the QR on the heart

            if scannedQR == False:  # is zbar can't read the QR code
                for i in range(8):  # turn the station red
                    strip.setPixelColor(i, Color(0, 255, 0))
                strip.show()
                ldr.wait_for_light()    # wait for the heart to be removed
                continue    # go back to the start of the while loop (line 48)

        repeatcode = QR_usage_checker(conn, scannedQR) # check for an already used QR

        if repeatcode == True:
            cell_num = unique_cell_picker(conn) # choose a unique cell
            update_heart(conn, cell_num, scannedQR, 0) # bagsey the cell from the database

            for i in range(8, 16):  # shed some light on the HR detector
                strip.setPixelColor(i, Color(0, 255, 0))
            strip.show()

            serial_line = str(ser.readline()) # get the line from serial
            newSerial = int(serial_line[2:(len(serial_line)-5)]) #trim it!
            RecentHrs.append(newSerial) # add it to the list
            del RecentHrs[0] # delete the oldest item in the list
            RANGE = max(RecentHrs) - min(RecentHrs) # find the range of the data







if __name__ == "__main__":
    try:



    except KeyboardInterrupt:
        for i in range(8):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
