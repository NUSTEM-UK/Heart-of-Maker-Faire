import time

init_time = int(round(time.time()*1000))

def millis():
    millis = int(round(time.time()*1000))
    return millis

if __name__ == '__main__':
    while True:
        prog_time = millis() - init_time
        sec_time = prog_time % 1000
        frame_count = sec_time % 255
        print(frame_count)
