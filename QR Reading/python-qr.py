import cv2
from PIL import Image
import zbarlight
# Code sourced from https://gist.github.com/cbednarski/8450931
# And https://github.com/Polyconseil/zbarlight

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out = cv2.imwrite('capture.jpg', frame)
        break

cap.release()
cv2.destroyAllWindows()

file_path = 'capture.jpg'
with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
print('QR codes: %s' % codes)
