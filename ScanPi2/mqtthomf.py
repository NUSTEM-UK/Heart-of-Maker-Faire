import paho.mqtt.client as mqtt
import time

qos = 1
hiccup = 0.01

client = mqtt.Client()
client.connect('192.168.1.1')
client.loop_start()

def MQTTsend(location, status, data):
    # turn the data into a string
    # heart/[heartnum]/setMode
    # heart/[heartnum]/setrate
    setModeString = "heart/"+str(location).zfill(3)+"/setMode" # zfill adds leading zeros
    setRateString = "heart/"+str(location).zfill(3)+"/setRate"

    client.publish(setModeString, status, 1)
    time.sleep(0.01)
    client.publish(setRateString, data, 1)
    time.sleep(0.01)

if __name__ == '__main__':
    print("Sending data...")
    try:
        MQTTsend(244, 0, 56)
        print("Data sent")
    except:
        print("Error sending data...")
