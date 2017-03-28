from gpiozero import LightSensor # The gpio Lightsensor
from time import sleep

ldr = LightSensor(23, charge_time_limit=0.3, threshold = 0.1) # LDR sensor

while True:
    ldr.wait
