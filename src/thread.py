import logging
from threading import Thread

from unit import Unit

import idle

class GuardDog(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.unit = None
        self.log = logging.getLogger('dog')
        self.log.setLevel(logging.INFO)

    def run(self):
        self.mode = idle.IdleMode(self.unit)
        while True:
            self.mode = self.mode.run(self.unit)

    def connect(self, address):
        try:
            self.unit = Unit(address)
            self.start()
            self.log.info('successfully connected -- \'{}\''.format(address))
            return True
        except OSError as err:
            self.log.error('failed to connect -- \'{}\''.format(address))
            self.log.error(err)
            return False
