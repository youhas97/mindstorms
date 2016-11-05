from unit import Unit
from time import sleep, time

class FollowTape():

    def __init__(self, unit):
        self.offset = self.offset_prev = 0
        self.refl = self.refl_prev = unit.reflect()
        self.refl_min = self.refl_max = self.refl
        self.refl_interval = self.refl_max - self.refl_min
        self.k_p = 1
        self.k_d = 1
        self.time_update = 0
        self.update_interval = 0
        self.turn = self.turn_prev = 0
        self.direction = 1

        self.refl_min_turn = self.refl_max_turn = self.refl

        unit.forward(10)

    def update_reflection(self, unit):
        self.refl = unit.reflect()
        self.refl_min = min(self.refl_min, self.refl)
        self.refl_max = max(self.refl_max, self.refl)
        self.refl_interval = self.refl_max - self.refl_min
        print(self.refl_min, self.refl, self.refl_max)

    def set_offset(self, unit):
        if time() > self.time_update + self.update_interval:
            self.offset_prev = self.offset
        pivot = (self.refl_max - self.refl_min) / 2 + self.refl_min
        if self.refl_max != self.refl_min:
            self.offset = (self.refl - pivot) / (self.refl_interval / 2)
        else:
            self.offset = 0

    def set_speed(self, unit):
        if abs(self.refl != self.refl_prev) < 2:
            unit.set_speed(unit.speed+1)
        else:
            unit.set_speed(unit.speed-10*abs(self.refl-self.refl_prev))

    def set_direction(self):
        if self.turn * self.turn_prev > 0:
            self.refl_min_turn = min(self.refl_min_turn, self.refl)
            self.refl_max_turn = max(self.refl_max_turn, self.refl)
            if self.refl_max_turn - self.refl_min_turn > self.refl_interval * 0.5:
                self.direction = not self.direction
        else:
            self.refl_min_turn = self.refl_max_turn = self.refl

    def run(self, unit):
        self.update_reflection(unit)
        self.set_offset(unit)
        self.set_speed(unit)
        self.set_direction()
        self.turn_prev = self.turn
        self.turn = self.offset_prev*self.k_p+self.k_d*(self.offset-self.offset_prev) * self.direction
        unit.turn(self.turn)

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    follow_tape_mode = FollowTape(unit)

    while True:
        follow_tape_mode.run(unit)

