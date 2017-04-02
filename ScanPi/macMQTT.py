import paho.mqtt.client as mqtt
from sqlhomf import *
import time
import re
import socket

def on_message(client, userdata, msg):
    """Output diagnostic when message sent via broker."""
    msg.payload = msg.payload.decode("utf-8")
    print('Message received')
    if msg.payload == "clear":
        print('We made it')
        m = re.search('heart/(.+?)/setMode', msg.topic)
        if m:
            cellNum = int(m.group(1))
            print(cellNum)
            watch_colour_reset(conn, cellNum)

def on_connect(client, userdata, rc):
    # Connect to MQTT broker.
    print ("Connected with result code: " + str(rc))
    # We can subscribe to wildcard topics, which are matched
    # as new topics are created.
    client.subscribe("heart/#")

try:
    client = mqtt.Client()
    client.connect('192.168.1.1')
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
except:
    print("Error connecting to MQTT, are you on the correct network?")

while True:
    pass
