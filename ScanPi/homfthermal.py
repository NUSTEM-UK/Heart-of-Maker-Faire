"""Functions for the Thermal Printer - availble from GITHUB
https://github.com/adafruit/Python-Thermal-Printer """

from Adafruit_Thermal import *
import time

def printout(hr, qr):
    date_string = time.strftime("Maker Faire UK %Y%m%d-%H%M")
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

    printer.justify('C')
    printer.println("The Heart of Maker Faire")
    printer.println("")

    import gfx.qrs as qrs
    
