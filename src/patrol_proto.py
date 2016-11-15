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
            
    def run(self, unit):
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
   
        
            
