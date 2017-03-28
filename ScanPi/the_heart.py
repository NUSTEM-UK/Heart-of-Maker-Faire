import time
from mqtthomf import *
from neoshomf import *
from printcommands import *
from rategethomf import *
from scanninghomf import *
from sqlhomf import *
from gpiozero import LightSensor # The gpio Lightsensor
from rotaryhomf import *

def main():
    print("It begins")
    ldr = LightSensor(23, charge_time_limit=0.2, threshold = 0.1) # LDR sensor
    last_time_checked = int(round(time.time()*1000)) # record the start time
    frame = 0 # set the initial frame to zero for the blinky lights
    repeatcode = False # set the QR repetition bool to False
    while True:
        ringSelect(strip, 'green', 1, False)
        last_time_checked, frame = pulselight(strip, last_time_checked, frame, 60) # get the current pulse frame
        print(ldr.value)
        if (ldr.value > 0.9):   # a heart has been placed on the scanner
            print("Heart detected")
            ringSelect(strip, 'cyan', 1, True)
            scannedQR = QRread()    # read the QR on the heart

            if scannedQR == False:  # if zbar can't read the QR code
                for i in range(6):
                    ringSelect(strip, 'red', 1, True)
                    time.sleep(0.5)
                    ringSelect(strip, 'blank', 1, True)
                    time.sleep(0.5)
                    continue

            repeatcode = QR_usage_checker(conn, scannedQR) # check for an already used QR
            if repeatcode == True:
                cell_num = unique_cell_picker(conn) # choose a unique cell
                update_heart(conn, cell_num, scannedQR, 0) # bagsey the cell from the database
                status = watch_colour_picker(conn, cell_num)
                if status == False: # what if we've run out of indication colours
                    continue
                ringSelect(strip, status, 2, True)
                heartrate = encoder(status)

                update_heart(conn, cell_num, scannedQR, heartrate)
                MQTTsend(cell_num, status, heartrate)
                HRprinter(scannedQR, heartrate, status)
                repeatcode = False
            else:
                pass

if __name__ == "__main__":
    try:
        main()
    finally:
        neocleanup(strip)
