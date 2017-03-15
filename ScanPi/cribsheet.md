MQTT Functions:

MQTTsend(location, 'status', heartrate)
location, heartrate are integer values
'status' is a colour - 'cyan', 'yellow', 'purple', 'green' or 'clear'

Neopixel Functions:

pulsefeedback (strip, spread)
Strip is the Neopixel strip initiated by strip = Adafruit...
Spread is an range of HR data, integer value

setColour(strip, colour, location, show)
Colour - 'red', 'blue', 'green', 'blank'
Location 1 or 2, depending on which bank of Neos we want to control
