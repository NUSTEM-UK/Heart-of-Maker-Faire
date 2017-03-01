from Adafruit_Thermal import *
#defining the printer
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


def qrprintout(heartRate, qrCode):
    #Thank you for contributing to the heart of maker Faire
    #print in centre
    printer.justify('C')

    #print in double height and bold
    printer.doubleHeightOn()  #bigger font size
    printer.println("Thank you for")  #text being printed
    printer.println("contributing to:")  #text being printed
    printer.setSize('L')  #larger font size and b
    printer.println("The Heart Of\n Maker Faire")
    printer.setDefault()  #resetting the printing options such as text size


    #Your heart rate is ...
    printer.justify('C')  #centering the text
    printer.println("Your Heart Rate Is:")  #printing text
    printer.setLineHeight(10)  #setting space size
    printer.println("\n")  #creating space between lines
    printer.doubleHeightOn()  #larger font size
    printer.println(heartRate, " bpm")  #text being printed
    printer.doubleHeightOff()  #resetting the font size

    #Your Heart is stored at...
    printer.setLineHeight(25)
    printer.println("\n")  #creating space between lines
    printer.println("Your Heart Is")  #printing text
    printer.println("stored at QR Location:")  #printing text

    #space between text and qr code
    printer.setLineHeight(10)  #setting space size
    printer.println("\n")  #creating a space between text

    #Print QR code
    import gfx.adaqrcode as adaqrcode  #importing qr code
    printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)  #printing qr code

    #get in touch
    printer.setLineHeight(10)  #setting spaze size
    printer.println("\n")  #creating space between lines
    printer.println("Get in touch:")  #printing text
    printer.println("@thinkphysicsne")  #printing text
    printer.println("nustem.uk")  #printing text
    printer.feed(3)  #adding extra paper to come out of the printer
