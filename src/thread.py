import logging
from threading import Thread

from unit import Unit

import idle

class GuardDog(Thread):
    """Run and communicate with unit.
    
    Public methods:
        set_mode -- set mode of unit.
        get_speed -- get current speed of unit
        connect -- connect to unit and create object
    """

    def __init__(self):
        Thread.__init__(self)
        self.unit = None
        self.log = logging.getLogger('dog')
        self.log.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        formatter = logging.Formatter('%(levelname)s - %(name)s: %(message)s')
        console.setFormatter(formatter)
        self.log.addHandler(console)

    def set_mode(self, Mode):
        """Set mode."""
        self.NewMode = Mode

    def get_speed(self):
        """Get the current speed of the unit."""
        return self.unit.actual_speed()

    def run(self):
        """Run an iteration of the unit's current mode."""
        self.mode = idle.IdleMode(self.unit)
        while True:
            self.mode = self.mode.run(self.unit)
            if self.new_mode:
                self.mode = self.NewMode(self.unit)
                self.NewMode = None

    def connect(self, address):
        """Connect to unit and create object."""
        try:
            self.unit = Unit(address)
            self.start()
            self.log.info('successfully connected -- \'{}\''.format(address))
            return True
        except OSError as err:
            self.log.error('failed to connect -- \'{}\''.format(address))
            self.log.error(err)
            return False
