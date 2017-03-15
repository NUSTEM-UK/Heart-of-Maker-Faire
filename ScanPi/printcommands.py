"""The Adafruit Thermal Printer isoftware is designed for Python2, we
are using Python3 so we're using OS.system to write the print command 
to the terminal"""

import os
def HRprinter(location, heartrate, colour):
    print("Printing")
    os.system("python printerhomf.py " +str(location) + " " + str(heartrate) + " " + colour + " &")
