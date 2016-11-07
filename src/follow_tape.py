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
        self.refl_interval = self.refl_max - self.refl_min
        self.k_p = 1
        self.k_d = 1.5
        self.turn = self.turn_prev = 0        self.direction = 1
        self.refl_min_turn = self.refl_max_turn = self.refl

        unit.forward(10)

    def update_color(self, unit):
        self.color = unit.color()

    def update_reflection(self, unit):
        """Parse reflection from unit and set min/max values."""
        self.refl = unit.reflect()
        self.refl_min = min(self.refl_min, self.refl)
        self.refl_max = max(self.refl_max, self.refl)
        self.refl_interval = self.refl_max - self.refl_min

    def set_offset(self, unit):
        """Adjust offset value to edge of tape.

        Description:
            The reflection has a min and max value. The value
            in between (pivot) min and max is considered the
            edge of the tape. The offset is set to 1 if
            reflection is at max, 0 if in the middle, -1 if
            at min, and any value between those (continous).
        """
        self.offset_prev = self.offset
        self.pivot = (self.refl_max - self.refl_min) / 2 + self.refl_min
        if self.refl_max != self.refl_min:
            self.offset = (self.refl - self.pivot) / (self.refl_interval / 2)
        else:
            self.offset = 0

    def set_speed(self, unit):
        """Automatically adjust speed of vehicle.
    
        Description:
            Increases speed if reflection has low variation.
            Decreases speed if reflection has high variation.
        """
        if abs(self.refl != self.refl_prev) < 2:
            if self.offset < 0:
                unit.set_speed(unit.speed+1)
        else:
            unit.set_speed(unit.speed-10*abs(self.refl-self.refl_prev))

    def set_direction(self):
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

    def set_turn(self):
        self.turn_prev = self.turn
        self.turn = self.offset * self.k_p \
                  + self.k_d * (self.offset - self.offset_prev)
        self.turn *= self.direction
        self.turn /= float(max(self.k_d, self.k_p))

    def run(self, unit):
        """Run the follow tape mode.

        Description:
            Should be run from a while loop. Executes all 
            methods needed to follow the tape. Variables
            accross iterations are stored in the object.
        """
        #self.update_color(unit) #slows down main loop, slow enough to fail tape follow
        self.update_reflection(unit)
        self.set_offset(unit)
        self.set_speed(unit)
        #self.set_direction()
        self.set_turn()
        print(self.offset, self.turn)
        unit.turn(self.turn)

        """"
        # turn right at red tape
        if 8 <= self.refl <= 21:
            if unit.color() == 'red':
                print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeej')
                self.turn = 1
                unit.set_speed(0)
        """

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    follow_tape_mode = FollowTape(unit)

    while True:
        follow_tape_mode.run(unit)

