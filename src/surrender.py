from unit import Unit
from time import sleep
from follow_tape import FollowTape

class FindCorner(FollowTape):

    def __init__(self, unit):
        super().__init__(unit)
        unit.set_speed(10)
        
    def in_corner(self, unit):
        pass
     
    def run(self, unit):
        super().run(unit)
        if self.in_corner(unit):
            print('hej')
            
        return self.run

class Surrender():

    def __init__(self, unit):
        unit.speak('I surrender')
        sleep(2)
        unit.rotate(100,150)
        sleep(2.3)
        unit.forward(100)
        self.mode = FindCorner(unit).run
        
        
    def run(self, unit):
        self.mode = self.mode(unit)
        
        return self
        
    def find_tape(self, unit, next_mode):
        if unit.reflect() <= 8:
            self.mode = self.rotate_from_wall
            
            
if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Surrender(unit)
    while True:
        mode = mode.run(unit)