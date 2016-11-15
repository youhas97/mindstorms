from unit import Unit
from time import sleep
from random import randint, choice
import threat

class Patrol():
    
    def __init__(self, speed=50, mode='peaceful'):
        self.speed = speed
        self.distance = 40
        self.mode = mode
        
    def set_speed(speed):
        self.speed = speed
    
    def change_direction(self, unit):
        direction = choice([-1,1])
        unit.forward(-self.speed)
        sleep(0.8)
        unit.stop()
        unit.rotate(100, direction*randint(90,180))
        sleep(2)

    def check_activation(unit):
        channel = 1
        angle, distance = unit.seek(channel)
        print(angle, distance)
        return distance != -128
        
    def activation_dance(unit):
        unit.stop()
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
            
    def run(self, unit):
        if self.check_activation(unit):
            self.activation_dance(unit)
            if self.mode == 'guard':
                self.mode = 'peaceful'
            else:
                self.mode = 'guard'
            unit.speak('{} mode activated'.format(self.mode))
        prox = unit.ir_sensor.get_prox()
        #reflection = unit.color_sensor.get_reflect()
        reflection = 1000
        color = unit.color()
        #color = 10
        print(prox, reflection, color)
        if prox >= self.distance and color=='brown':
            unit.forward(self.speed)
        elif reflection <=10 or color!='brown':
            self.change_direction(unit)
        elif prox <= self.distance *1.25:
            if self.mode == 'peaceful':
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                self.change_direction(unit)
            elif self.mode == 'guard':
                return threat.ThreatMode()
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Patrol(speed=100)
    while True:
        mode = mode.run(unit)
   
        
            
