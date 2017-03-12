import time
from homf-mqtt import *
from homf-neos import *
from homf-printing import *
from homf-rateget import *
from homf-scanning import *
from gpiozero import LightSensor # The gpio Lightsensor

def main():
    ldr = LightSensor(12, charge_time_limit=0.2, threshold = 0.5) # LDR sensor
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
    repeatcode = False # set the QR repetition bool to False
    while True:
        setColour('green', 1, False)
        last_time_checked, frame = pulselight(last_time_checked, frame) # get the current pulse frame

        if (ldr.light_detected == False):   # a heart has been placed on the scanner
            setColour('blue', 1, True)
            scannedQR = QRread()    # read the QR on the heart

            if scannedQR == False:  # if zbar can't read the QR code
                setColour('red', 1, True)
                ldr.wait_for_light()    # wait for the heart to be removed
                continue    # go back to the start of the while loop

            repeatcode = QR_usage_checker(conn, scannedQR) # check for an already used QR
            if repeatcode == True:
                cell_num = unique_cell_picker(conn) # choose a unique cell
                update_heart(conn, cell_num, scannedQR, 0) # bagsey the cell from the database
                setColour('blue', 2, True)
                heartrate = getheartrate()
                update_heart(conn, cell_num, scannedQR, heartrate)
                MQTTsend(cell_num, 1, heartrate)
                qrprintout(heartrate, scannedQR)
                repeatcode = False
            else:
                pass

if __name__ - "__main__":
    try:
        main()
    except KeyboardInterrupt:
        setColour('black', 1, True)
