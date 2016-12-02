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
        unit.rotate(100,180)
        sleep(2.3)
        unit.forward(50)

    def in_corner(self, unit):
        return (20 <= self.refl <= 39 or self.refl >=45) and unit.color() == 'red'

    def outside_corner(self, unit):
        if abs(self.offset_hist[-1]) >= 0.95:
            for offset in self.offset_hist[:-1]:
                if abs(offset) >= 0.9:
                    pass
                else:
                    return False
            return True
        return False

    def run(self, unit):
        super().run(unit)
        print(self.refl, self.offset_hist)
        if self.in_corner(unit):
            return idle.IdleMode(unit)
        elif self.outside_corner(unit):
            return idle.IdleMode(unit)
        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    mode = Surrender(unit)
    while True:
        mode = mode.run(unit)
