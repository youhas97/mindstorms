from unit import Unit
from time import sleep
import threat

import tkinter as tk

class Patrol():
    PEACEFUL = 0
    GUARD = 1

    DISTANCE_THRESHOLD = 40

    def __init__(self, unit, mode=0):
        self.speed = 40
        self.mode_changed = False
        self.patrol_mode = mode
        self.patrol_square = True

    def set_speed(self, speed):
        """sets the speed"""
        self.speed = speed

    def set_patrol_mode(self, mode):
        """switches mode"""
        if self.patrol_mode != mode:
            self.mode_changed = True

    def update_mode(self, unit):
        """updates mode"""
        if self.mode_changed:
            self.toggle_mode(unit)
            self.mode_changed = False

    def activation_dance(self, unit):
        """dance used for activation of robot"""
        unit.stop()
        unit.rotate_forever(100)
        sleep(0.15)
        unit.rotate_forever(-100)
        sleep(0.1)
        unit.stop()

    def toggle_mode(self, unit):
        """toggles between peaceful and guard mode"""
        self.patrol_mode ^= True
        MODE_NAMES = ['peaceful', 'guard']
        self.activation_dance(unit)
        unit.speak('{} mode activated'.format(MODE_NAMES[self.patrol_mode]))
        sleep(2.5)

    def object_in_prox(self):
        """checks if object is in sight range"""
        return self.prox < Patrol.DISTANCE_THRESHOLD

    def run(self, unit):
        """run an iteration of patrol"""
        self.prox = unit.ir_sensor.get_prox()
        unit.forward(self.speed)

        self.update_mode(unit)
        if self.patrol_square and unit.reflect() < 15:
            unit.change_direction(self.speed)
        elif self.object_in_prox():
            print('prox')
            if self.patrol_mode == Patrol.PEACEFUL:
                print('pec')
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                unit.change_direction(self.speed)
            elif self.patrol_mode == Patrol.GUARD:
                print('gud')
                return threat.ThreatMode(unit, speed=self.speed)
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Patrol(speed=50)
    while True:
        mode = mode.run(unit)
