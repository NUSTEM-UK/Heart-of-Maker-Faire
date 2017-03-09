"""Listen for (and output) commands issued via MQTT broker.

Use for basic diagnostic purposes, debugging, and to
see if anything we're doing makes even the vaguest bit of sense.
"""

import paho.mqtt.client as mqtt


def on_connect(client, userdata, rc):
    # Connect to MQTT broker.
    print "Connected with result code: " + str(rc)
    # We can subscribe to wildcard topics, which are matched
    # as new topics are created.
    client.subscribe("heart/#")


def on_message(client, userdata, msg):
    """Output diagnostic when message sent via broker."""
    print "Topic:", msg.topic + '  :  Message: ' + msg.payload


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('localhost', 1883)
client.loop_forever()
