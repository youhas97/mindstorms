from unit import Unit
from time import sleep

def main():
    unit = Unit('192.168.43.11')
    channel = 1
    FOV = 90
    RANGE = 20
    while True:
        prox = unit.prox()
        angle, distance = unit.seek(channel)
        print(angle, distance, prox)
        unit.forward(prox)
        #if prox < 20:
        #    unit.rotate(100, 180)
        #    sleep(3)
        if 0 <= distance < RANGE and abs(angle) < FOV/2:
            print('activate')

if __name__ == '__main__':
    main()
