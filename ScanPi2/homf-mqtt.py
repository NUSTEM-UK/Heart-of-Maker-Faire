import paho.mqtt.client as mqtt
import time

qos = 1
hiccup = 0.01

client = mqtt.Client()
client.connect('localhost')
client.loop_start()

def MQTTsend(location, status, data):
    # turn the data into a string
    MQQTString = str(location) + '-' + str(status) + '-' + str(data)
    client.publish("homf/update", MQQTString)

if __name__ == '__main__':
    print("Sending data...")
    try:
        MQTTsend(244, 0, 56)
    except:
        print("Error sending data...")
