import zbarlight
from picamera import *
from PIL import Image
from gpiozero import Button

# set up the Pi camera as camera, set resolution and filename
camera = PiCamera()
camera.resolution = (1024, 768)
file_path = "newQR.png"

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
    qrcode = zbarlight.scan_codes('qrcode', image)
    barcode = zbarlight.scan_codes('ean13', image)

    if qrcode is None and barcode is None:
        print("Scanning error, no codes read")
    elif barcode is None and qrcode is not None:
        print("QRcode identified: %s" % qrcode)
    else:
        print("Barcode identified: %s" % barcode)

def main():
    QRread()

if __name__ == '__main__':
    main()
