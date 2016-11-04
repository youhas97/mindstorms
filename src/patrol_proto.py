from unit import Unit
from time import sleep
from random import randint, choice

class Patrol():
    
    def __init__(self, speed=50):
        self.speed = speed
        self.distance = 40
        
    def set_speed(speed):
        self.speed = speed
    
    def run(self, unit):
        direction = choice([-1,1])
        prox = unit.ir_sensor.get_prox()
        reflection = unit.color_sensor.get_reflect()
        color = unit.color_sensor.get_color()
        if prox >= self.distance and reflection >= 7:
            unit.forward(self.speed)
        elif prox <= self.distance * 1.25 or reflection <=6 or color==0:
            unit.stop()
            if prox <= self.distance * 1.25:
                unit.speak('piss off cunt')
                sleep(1.7)
            
            unit.rotate(100,direction*randint(90,180))
            sleep(2)

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    patrol_mode = Patrol(speed=100)
    while True:
        patrol_mode.run(unit)
        
            
