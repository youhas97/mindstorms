from unit import Unit
from time import sleep
from random import randint, choice
import threat

import tkinter as tk

class Patrol():
    PEACEFUL = 0
    GUARD = 1
    MODE_NAMES = ['guard', 'peaceful']

    DISTANCE_THRESHOLD = 40

    def __init__(self, unit):
        self.speed = 40
        self.patrol_mode = Patrol.PEACEFUL

    def set_speed(self, speed):
        self.speed = speed

    def set_mode(self, mode):
        if self.patrol_mode != mode:
            self.toggle_mode

    def change_direction(self, unit):
        direction = choice([-1,1])
        unit.forward(-self.speed)
        sleep(0.8)
        unit.stop()
        unit.rotate(100, direction*randint(90,180))
        sleep(2)

    def activation_dance(self, unit):
        unit.stop()
        """"
        unit.speak('choke me daddy')
        sleep(2.5)
        unit.rotate_forever(100)
        sleep(0.15)
        unit.rotate_forever(-100)
        sleep(0.6)
        unit.rotate_forever(100)
        sleep(3)
        unit.rotate_forever(-100)
        sleep(0.15)
        unit.stop()
        """
        sleep(2)

    def toggle_mode(self, unit):
        self.patrol_mode ^= True
        unit.speak('{} mode activated'.format(Patrol.MODE_NAMES[self.patrol_mode]))
        self.activation_dance(unit)

    def object_in_prox(self):
        return self.prox < Patrol.DISTANCE_THRESHOLD

    def run(self, unit):
        self.prox = unit.ir_sensor.get_prox()
        self.refl= unit.reflect()
        unit.forward(self.speed)

        print(self.prox, self.refl)
        if self.refl < 10:
            self.change_direction(unit)
        elif self.object_in_prox():
            if self.patrol_mode == Patrol.PEACEFUL:
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                self.change_direction(unit)
            elif self.patrol_mode == Patrol.GUARD:
                return threat.ThreatMode()
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Patrol(speed=50)
    while True:
        mode = mode.run(unit)
