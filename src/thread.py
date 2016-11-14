import logging
from threading import Thread

from unit import Unit
import patrol

class GuardDog(Thread):

    def __init__(self):
        Thread.__init__(self)

        self.unit = None

    def run(self):
        self.mode = patrol.Patrol()
        while True:
            self.mode = self.mode.run(self.unit)

    def connect(self, address):
        try:
            self.unit = Unit(address)
        except OSError as err:
            logging.error('GuardDog: failed to connect -- {}'.format(address))
            return False
        return True
