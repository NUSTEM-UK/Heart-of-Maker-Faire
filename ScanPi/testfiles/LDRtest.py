from gpiozero import LightSensor


ldr = LightSensor(12, charge_time_limit=0.2, threshold=0.5)

def main():
    if (ldr.light_detected == True):
        print("Light")
    else:
        print("Dark")

if __name__ == '__main__':
    while True:
        main()
