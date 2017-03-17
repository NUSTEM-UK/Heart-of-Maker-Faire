# Creating a the 'Heart of' scanner
### 1. Begin with a fresh install of Raspbian and a Pi3
[Start here](https://www.raspberrypi.org/documentation/ "Raspberry Pi Setup Guide") and follow the instructions to download and flash Raspbian.
Once your Pi is up and running, you'll need to: `sudo apt-get update` and `sudo apt-get upgrade`.

Next you'll need to enable your PiCamera, setup guide [here](https://www.raspberrypi.org/documentation/configuration/camera.md "PiCamera Setup").
### 2. Installing the necessary dependencies
* #### Thermal Printer

The initial setup of the Adafruit Thermal Printer relied heavily on [this guide](https://learn.adafruit.com/pi-thermal-printer/ "Adafruit Tutorial") - use it to get the wiring correct.

This version of the Thermal Printer code only works with Python2, which is why you'll notice the os.system workaround in **printercommands.py**. You'll need to install a few libraries in order for the printer to work:

`sudo apt-get install python-serial python-imaging python-unidecode`.

Make the following adjustments to the Pi:

`sudo nano /boot/cmdline.txt`

Change: `dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`

to:
`dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`

Then open: `sudo nano /boot/config.txt`
and add this line to the bottom: `enable_uart=1`.

Finally: `git clone https://github.com/adafruit/Python-Thermal-Printer`

* #### Neopixels

These two guides will see you through installation of the Neopixels on the Raspberry Pi, the [readme.md from the Github Repo](https://github.com/jgarff/rpi_ws281x) and the [Adafruit Tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/overview).

_Make sure you power the Neopixels externally from the Raspberry Pi, the Pi ain't powerful enough to run multiple neos_

In summary:

`sudo apt-get install build-essential python-dev python3-dev git scons swig`

`git clone https://github.com/jgarff/rpi_ws281x.git`

`cd rpi_ws281x`

`scons`

Then:
`cd python`

`sudo python3 setup.py install`

You'll need to blacklist the audio kernel for it all to work:
`sudo nano /etc/modprobe.d/snd-blacklist.conf`

Add:
`blacklist snd_bcm2835`
And reboot!

* #### MySQL

We need to install MSQLdb for Python3, which is less simple than it should be:

`sudo apt-get install libmysqlclient-dev`

`pip install MySQL-python`

`sudo pip3 install mysqlclient`

Test it's worked by running:

`python3`

`import MySQLdb`

If it doesn't throw a hissy fit, then you're good!

* #### The MQTT Python Client

For the Python side of things:
`pip3 install paho-mqtt`

For the RaspberryPi broker:
`apt-get install mosquitto`

* #### QR Scanner

You're nearly there! Soon you'll be able to scan your heart rate 'til your heart's content! The scanner uses ZBar and the ZBar light python wrapper.

Installing Zbar:

`sudo apt-get install libzbar0 libzbar-dev`

And then:

`sudo pip3 install zbarlight`

Check the functionality by running `python3` and trying `import zbarlight`.
