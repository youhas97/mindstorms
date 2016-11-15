from unit import Unit
from time import sleep
from follow_tape import FollowTape

import idle

class Surrender(FollowTape):
    def __init__(self, unit):
        super().__init__(unit)
    
    def __init__(self, unit):
        super().__init__(unit)
        unit.speak('I surrender')
        sleep(2)
        unit.rotate(100,150)
        sleep(2.3)
        unit.forward(80)

    def in_corner(self, unit):
        return 18 <= self.refl <= 22 and unit.color() == 'red'
     
    def run(self, unit):
        super().run(unit)
        if self.in_corner(unit):
            return idle.IdleMode(unit)
        return self
        
if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Surrender(unit)
    while True:
        mode = mode.run(unit)
