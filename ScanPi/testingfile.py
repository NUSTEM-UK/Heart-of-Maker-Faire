from gpiozero import LightSensor, LED, Button
import time
ldr = LightSensor(18, charge_time_limit=0.3, threshold = 0.2)

while True:
    if (ldr.light_detected == False):
        print("Jar detected")
    else:
        print("No Jar")
    time.sleep(1)
