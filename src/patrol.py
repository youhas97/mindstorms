from unit import Unit
from time import sleep
from random import randint, choice
import threat

class Patrol():
    GUARD = 0
    PEACEFUL = 1
    MODE_NAMES = ['guard', 'peaceful']

    DISTANCE_THRESHOLD = 40
    
    def __init__(self, speed=50, mode='peaceful'):
        self.speed = speed
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

    def check_activation(self, unit):
        channel = 1
        angle, distance = unit.seek(channel)
        print(angle, distance)
        return distance != -128
        
    def activation_dance(self, unit):
        unit.stop()
        """"
        #unit.speak('choke me daddy')
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
        self.mode = not self.mode
        unit.speak('{} mode activated'.format(Patrol.MODE_NAMES[self.mode]))
        self.activation_dance(unit)

    def object_in_prox(self):
        return self.prox < Patrol.DISTANCE_THRESHOLD

    def run(self, unit):
        self.prox = unit.ir_sensor.get_prox()
        self.refl= unit.reflect()
        unit.forward(self.speed)

        if self.check_activation(unit):
            self.toggle_mode(unit)

        print(self.prox, self.refl)
        if self.refl < 10:
            self.change_direction(unit)
        elif self.object_in_prox():
            if self.mode == Patrol.PEACEFUL:
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                self.change_direction(unit)
            elif self.mode == Patrol.GUARD:
                return threat.ThreatMode()
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Patrol(speed=50)
    while True:
        mode = mode.run(unit)
   
        
            
