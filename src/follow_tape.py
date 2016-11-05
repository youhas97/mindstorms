from unit import Unit

class FollowTape():

    def __init__(self, unit):
        self.refl = 0
        self.relf_prev = 0
        self.k_p = 1
        self.k_d = 1
        self.turn = 0

        unit.forward(10)

    def update_refl(unit):
        self.refl_prec = self.refl
        self.refl = unit.reflect()

    def run(unit):
        self.update_refl(unit)
        self.turn = self.refl_prev*self.k_p+self.k_d*(self.relf-self.refl_prev)
        unit.turn(self.turn)

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    follow_tape_mode = FollowTape(unit)

