from unit import Unit
from time import sleep, time

class FollowTape():
    """Follow tape on the floor.

    Public methods:
        run -- Run an iteration of the follow tape mode.
    """

    def __init__(self, unit):
        self.hist_len = 5

        self.offset = 0
        self.offset_prev = 0
        self.offset_hist = [0 for _ in range(self.hist_len)]

        self.refl = unit.reflect()
        self.refl_prev = self.refl
        self.refl_min = self.refl
        self.refl_max = self.refl
        self.refl_interval = 0

        self.min_speed = 25

        self.turn = 0

        unit.set_speed(20)

    def update_reflection(self, unit):
        """Parse reflection from unit and set min/max values."""
        self.refl_prev = self.refl
        self.refl = unit.reflect()
        self.refl_min = min(self.refl_min, self.refl)
        self.refl_max = max(self.refl_max, self.refl)
        self.refl_interval = self.refl_max - self.refl_min

    def calculate_offset(self):
        """Calculate offset value to edge of tape.

        Description:
            The reflection has a min and max value. The value
            in between (pivot) min and max is considered the
            edge of the tape. The offset is set to 1 if
            reflection is at max, 0 if in the middle, -1 if
            at min, and any value between those (continous).
        """
        self.offset_prev = self.offset
        pivot = (self.refl_max - self.refl_min) / 2 + self.refl_min
        if self.refl_interval != 0:
            self.offset = (self.refl-pivot) / (self.refl_interval/2)
        else:
            self.offset = 0
        self.offset_hist.append(self.offset)
        self.offset_hist.pop(0)

    def adjust_speed(self, unit):
        """Control speed of unit.

        Description:
            Increases speed if reflection has low variation.
            Decreases speed if reflection has high variation.
        """
        #if abs(self.offset) < 0.3:
        #    unit.set_speed(unit.speed+1)
        if abs(self.refl - self.refl_prev) < 2:
            unit.set_speed(unit.speed+1)
        else:
            unit.set_speed(unit.speed-1)
            if unit.speed < self.min_speed:
                unit.set_speed(self.min_speed)

    def adjust_direction(self):
        """Control direction multiplier."""
        pass

    def adjust_turn(self, unit):
        """Control turn value for unit."""
        proportional_coeff = 1.25
        integral_coeff = 0.5
        derivative_coeff = 0.75

        print(self.offset_hist)

        self.turn = proportional_coeff * self.offset \
                  + integral_coeff * (sum(self.offset_hist) / self.hist_len) \
                  + derivative_coeff * (self.offset - self.offset_prev)

        self.turn /= float(proportional_coeff+integral_coeff+derivative_coeff*2)
        self.turn *= 2 # max turn value

    def run(self, unit):
        """Run an iteration of the follow tape mode.

        Description:
            Should be run from a loop. Executes all
            methods needed to follow the tape. Variables
            accross iterations are stored in the object.
        """
        self.update_reflection(unit)
        print(self.refl)
        if self.refl_interval > 10:
            self.calculate_offset()
            self.adjust_speed(unit)
            self.adjust_direction()
            self.adjust_turn(unit)

        unit.turn(self.turn)

        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    follow_tape_mode = FollowTape(unit)

    while True:
        follow_tape_mode.run(unit)
