"""Try out some features of MQTT to see how they work with Paho.

This works well run from the REPL. Wooh, interactive. Get us.
Run `mqttsub.py` in another shell to see what's going on at the broker
"""

import paho.mqtt.client as mqtt
import time

qos = 1
hiccup = 0.01

client = mqtt.Client()
client.connect("localhost")

# This call threads off the broker connection and leaves it open,
# which neatly avoids the issue (in much example code) of having
# to call connect() prior to every publush().
client.loop_start()

# We're going to publish with QOS=1 to ensure each message is delivered
# the broker at least once. That doesn't mean it's ever received, however.
# The brief sleeps seem to be required for localhost Mosquitto to cope.
# ...which is a bit weird.

# A basic initial test string to the root topic.
client.publish("heart", "test message", qos)
time.sleep(hiccup)

# Define a subtopic and publish to that.
client.publish("heart/01", "test message 2", qos)
time.sleep(hiccup)

# Define a subtopic of the right sort of structure for our purposes,
# and publish to that.
client.publish("heart/037/setMode", "1", qos)
time.sleep(hiccup)

# ...and we're close to defining an API
client.publish("heart/037/setRate", "68", qos)
time.sleep(hiccup)
client.publish("heart/037/setMode", "0", qos)
time.sleep(hiccup)

# On the Processing end, we should be able to use `strtok` to tokenise strings
# and hence navigate the subtopic tree.

# However, Processing/Arduino MQTT clients can't handle QOS=2
