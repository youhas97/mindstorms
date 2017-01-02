from follow_tape import FollowTape

class GetOverHere(FollowTape):

    """Make unit go to the remote."""

    def __init__(self, unit):
        super().__init__(unit)
        unit.stop()

        self.angle, self.distance = unit.seek(2)

    def update_seek(self, unit):
        """update angle and distance values"""
        self.angle_prev, self.distance_prev = self.angle, self.distance
        self.angle, self.distance = unit.seek(2)

    def calculate_offset(self, unit):
        self.offset_prev = self.offset
        pivot = 0
        self.offset = self.angle / 25.0

    def adjust_speed(self, unit):
        """adjust movement speed"""
        super().adjust_speed(unit)
        if self.distance == -128:
            unit.set_speed(0)

    def run(self, unit):
        """start following remote"""
        self.update_seek(unit)
        self.calculate_offset(unit)
        self.adjust_speed(unit)
        self.adjust_turn(unit)
        
        unit.turn(self.turn)

        return self

if __name__ == '__main__':
    from unit import Unit
    unit = Unit('192.168.0.112')
    mode = GetOverHere(unit)
    while True:
        mode = mode.run(unit)

