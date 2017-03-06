from gpiozero import LightSensor


ldr = LightSensor(18, charge_time_limit=0.3, threshold=0.2)

def main():
    if (ldr.light_detected == False):
        print("Light sensor is covered")
    else:
        print("Light sensory is covered")

if __name__ == '__main__':
    main()
