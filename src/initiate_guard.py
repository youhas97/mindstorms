from unit import Unit
from time import sleep

def check_activation(unit):
    channel = 1
    FOV = 90
    RANGE = 20
    angle, distance = unit.seek(channel)
    print(angle, distance)
    return distance != -128
    
if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    while True:
        if check_activation(unit):
            unit.speak('hello this is dog')
            sleep(2.5)
            unit.rotate_forever(100)
            sleep(0.05)
            unit.rotate_forever(-100)
            sleep(0.1)
            unit.rotate_forever(100)
            sleep(0.05)
            unit.stop()
