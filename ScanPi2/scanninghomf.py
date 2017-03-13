from picamera import *
from PIL import Image
import zbarlight

camera = PiCamera() # picamera setup
camera.resolution = (1024, 768)

# functions
def QRread():
    camera.capture("newQR.png")
    with open("newQR.png", 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    code = zbarlight.scan_codes('qrcode', image)
    if code is None:
        return False
    else:
        QRstr = str(code[0])
        QRint = int(QRstr[2:len(QRstr)-1])
        return QRint

if __name__ == '__main__':
    print(QRread())
