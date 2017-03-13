Raspberry Pi Dependancies:
- OpenCV
- ZBar
- PILLOW
- MySQLdb
- Neopixels on a Pi3
- The Adafruit Thermal Printer

MySQLbd
`sudo apt-get install python-dev libmysqlclient-dev`
`sudo apt-get install python3-dev`
`pip install mysqlclient`

ZBar and ZBarlight python wrapper --
`sudo apt-get install zbar-tools python-zbar libzbar0`
`pip3 install zbarlight`
Usage docs here: https://pypi.python.org/pypi/zbarlight

Neopixels --
This takes an amalgamation of two tutorials to run:
https://github.com/jgarff/rpi_ws281x - Read Build, Running and Limitations
and
https://learn.adafruit.com/neopixels-on-raspberry-pi/software - in particular these steps:
`sudo apt-get install build-essential python-dev git scons swig`

Adafruit Thermal Printer --
https://github.com/adafruit/Adafruit-Thermal-Printer-Library - - The Arduino Files (for Processing
  of BMP files for QR codes)
https://github.com/adafruit/Python-Thermal-Printer - - To install the Thermal Printer working with
  python on the Pi
https://learn.adafruit.com/pi-thermal-printer/overview - - Adafruit's Tutorial

Install OpenCv -- [this tutorial](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)
