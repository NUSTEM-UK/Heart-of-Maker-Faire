#!/usr/bin/python3
import random
#create the empty map - 0 shows an empty space in the HOMF
QR_MAPPING = [0] * 50

#for testing choose a random QR code number
SCANNED_QR = random.randint(0, 500)

#check if the QR code is already in use
for i in QR_MAPPING:
    if SCANNED_QR == QR_MAPPING[i]:
        NEW_QR = False
    else:
        NEW_QR = True
# choose a random position in the QRMapping list
RETRY = True

#loop until an empty cell is found
while RETRY:
#choose a random position in the map
    INDEX = random.randint(0, len(QR_MAPPING)-1)
    print(INDEX)
#check if that random position is empty (ie 0)
    if QR_MAPPING[INDEX] == 0:
        print('You can use this cell')
#add the QR code to the position
        QR_MAPPING[INDEX] = SCANNED_QR
        RETRY = False
    else:
        RETRY = True
