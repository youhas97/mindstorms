from unit import Unit
from time import sleep

import patrol
import surrender

class ThreatMode():

    def __init__(self):
        self.distance = 50

    def detect_threat(self, unit):
        if unit.prox() <= self.distance:
            unit.stop()
            if unit.check_movement(2,5) and unit.prox() <= self.distance:
                unit.speak('get out')
                sleep(1)
                for seconds in ['five','four','three','two','one']:
                    if unit.prox() <= self.distance:
                        unit.speak(seconds)
                        sleep(1)
                    else:
                        unit.stop()
                        return False
                return True

    def shoot(self, unit):
        unit.rotate(100,150)
        sleep(0.8)
        unit.speak('Say hello to my little friend')
        sleep(3.3)
        unit.shoot(1)
        sleep(1)
        unit.rotate(100,180)
        sleep(2)

    def run(self, unit):
        prox = unit.ir_sensor.get_prox()
        print(prox)
        if self.detect_threat(unit):
            self.shoot(unit)
            if unit.prox() <= self.distance:
                return surrender.Surrender(unit)
        else:
            return patrol.Patrol()
        return self


def main():
    unit = Unit('192.168.0.112')
    mode = ThreatMode()
    while True:
        print(mode)
        mode = mode.run(unit)

if __name__ == '__main__':
    main()

