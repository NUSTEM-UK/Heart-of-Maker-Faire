""" For the Heart of Maker Faire we need to generate a lot of paired QR codes
and print them on stickers, this code generates the qr codes and places them
onto a pdf
"""
# pyqrcode generates the QR codes
# pip install pyqrcode
import pyqrcode

# pypng allows the codes to be saved as png files
# pip install pypng
import png

# reportlab is used to generate the pdf
# pip install reportlab
from reportlab.pdfgen import canvas

# we need to import os for the cleanup
import os

# initialise the coordinate system
x = 0
y = 0

# set the max row and column values
maxY = 10
maxX = 8

# set the first coordinate position of the bottom left QR coordinate in pts
initX = 31
initY = 65.7

# set the gap in pts between the bottom left corner of each image to be displayed
gapX = 63.3
gapY = 76.587

# set the number of paired stickers you wish to create
stickerNum = int(input("How many stickers would you like to make?"))

# create the PDF canvas
c = canvas.Canvas("QRstickers-%s.pdf" % stickerNum)

for qrNum in range(stickerNum):

    # repeat so there are two copies of each code
    for repeat in range(2):
        # create the QR code
        img = pyqrcode.create('%s' % qrNum)
        # save it as a png
        img.png('QR-%s.png' % qrNum, scale = 2)

        # draw the code to the canvas
        c.drawImage('QR-%s.png' % qrNum, initX + (x * gapX), initY + (y * gapY))

        # increment the x position
        x += 1

        # if we get to last image in a row, increment the column
        if x == maxX:
            y += 1
            x = 0

        # when we get to the end of the page, increment the page and reset x and y
        if y == maxY:
            c.showPage()
            x=0
            y=0

    # cleanup the directory by removing the png files
    os.remove('QR-%s.png' % qrNum)

# save the pdf
c.save()
