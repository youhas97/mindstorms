from unit import Unit
from time import sleep, time

class FollowTape():
    """Follow tape on the floor.
    
    Public methods:
        run -- Run an iteration of the follow tape mode.
    """

    def __init__(self, unit):
        self.offset = self.offset_prev = 0
        self.refl = self.refl_prev = unit.reflect()
        self.refl_min = self.refl_max = self.refl
        self.refl_interval = 0
        self.turn = self.turn_prev = 0
        self.direction = 1
        self.refl_min_turn = self.refl_max_turn = self.refl = 0

    def update_reflection(self, unit):
        """Parse reflection from unit and set min/max values."""
        self.refl = unit.reflect()
        self.refl_min = min(self.refl_min, self.refl)
        self.refl_max = max(self.refl_max, self.refl)

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
        self.refl_interval = self.refl_max - self.refl_min
        if self.interval != 0:
            self.offset = (self.refl-pivot) / (self.refl_interval/2)
        else:
            self.offset = 0

    def adjust_speed(self, unit):
        """Control speed of unit.
    
        Description:
            Increases speed if reflection has low variation.
            Decreases speed if reflection has high variation.
        """
        if abs(self.refl != self.refl_prev) < 2:
            if self.offset < 0:
                unit.set_speed(unit.speed+1)
        else:
            unit.set_speed(unit.speed-10*abs(self.refl-self.refl_prev))

    def adjust_direction(self):
        """Control direction multiplier.

        Description:
            If the unit passes the tape during a turn
            it encounters the other edge and the offset
            becomes inverted (it turns right when it should
            turn left and vice versa). This method changes
            a multiplier and inverts the direction when
            the unit passes the tape.
        """
        if self.turn * self.turn_prev > 0:
            self.refl_min_turn = min(self.refl_min_turn, self.refl)
            self.refl_max_turn = max(self.refl_max_turn, self.refl)
            if self.refl_max_turn - self.refl_min_turn > self.refl_interval * 0.5:
                self.direction = -self.direction
        else:
            self.refl_min_turn = self.refl_max_turn = self.refl

    def adjust_turn(self, unit):
        """Control turn value for unit."""
        DERIVATIVE_COEFF = 1
        PROPORTIONAL_COEFF = 1.5

        self.turn_prev = self.turn
        self.turn = PROPORTIONAL_COEFF * self.offset \
                  + DERIVATIVE_COEFF * (self.offset - self.offset_prev)
        self.turn *= self.direction
        self.turn /= float(PROPORTIONAL_COEFF + DERIVATIVE_COEFF)
        unit.turn(self.turn)

    def run(self, unit):
        """Run the follow tape mode.

        Description:
            Should be run from a while loop. Executes all 
            methods needed to follow the tape. Variables
            accross iterations are stored in the object.
        """
        self.update_reflection(unit)
        self.calculate_offset()
        self.adjust_speed(unit)
        self.adjust_direction()
        self.adjust_turn(unit)

        return self

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    follow_tape_mode = FollowTape(unit)

    while True:
        follow_tape_mode.run(unit)

