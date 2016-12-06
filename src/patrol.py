from unit import Unit
from time import sleep
from random import randint, choice
import threat

import tkinter as tk

class Patrol():
    PEACEFUL = 0
    GUARD = 1

    DISTANCE_THRESHOLD = 40

    def __init__(self, unit):
        self.speed = 40
        self.mode_changed = False
        self.patrol_mode = Patrol.PEACEFUL
        self.patrol_square = True

    def set_speed(self, speed):
        self.speed = speed

    def set_patrol_mode(self, mode):
        if self.patrol_mode != mode:
            self.mode_changed = True

    def update_mode(self, unit):
        if self.mode_changed:
            self.toggle_mode(unit)
            self.mode_changed = False

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
        MODE_NAMES = ['peaceful', 'guard']
        unit.speak('{} mode activated'.format(Patrol.MODE_NAMES[self.patrol_mode]))
        self.activation_dance(unit)

    def object_in_prox(self):
        return self.prox < Patrol.DISTANCE_THRESHOLD

    def run(self, unit):
        self.prox = unit.ir_sensor.get_prox()
        unit.forward(self.speed)

        self.update_mode(unit)
        if self.patrol_square and unit.reflect() < 10:
            self.change_direction(unit)
        elif self.object_in_prox():
            if self.patrol_mode == Patrol.PEACEFUL:
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                self.change_direction(unit)
            elif self.patrol_mode == Patrol.GUARD:
                return threat.ThreatMode(unit)
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Patrol(speed=50)
    while True:
        mode = mode.run(unit)
