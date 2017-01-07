import logging
from time import time
from threading import Thread
import tkinter as tk

from unit import Unit
import modes


class GuardDog(Thread):
    """Run and communicate with unit.
    
    Public methods:
        set_mode -- set mode of unit.
        queue_command -- queue function to run when condition is met
        connect -- connect to unit and create object
    """

    def __init__(self):
        Thread.__init__(self)
        
        self.initiate_logger()
        self.set_start_values()

    def set_start_values(self):
        self.unit = None
        self.mode = None
        self.NewMode = None

        self.actual_speed = 0
        self.distance = 0

        self.actual_speed_str = tk.StringVar()
        self.distance_str = tk.StringVar()

        self.queue = []

    def initiate_logger(self):
        """Set up and configure logger."""
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

    def queue_command(self, command, condition=lambda: True):
        """Send command to the queue.

        Param:
            command -- function to execute when condition returns true
            condition -- function that returns true or false
        """
        self.queue.append((command, condition))
        self.log.info('added command, now {} in queue'.format(len(self.queue)))

    def execute_queue(self):
        """Execute commands in queue if conditions are met.

        Returns:
            amount of commands executed
        """
        executed = []
        for item in self.queue:
            command, condition = item
            if condition(): 
                command()
                executed.append(item)
        for item in executed:
            self.queue.remove(item)
        
        exec_count = len(executed)
        if exec_count:
            self.log.info('{} of {} executed.'.format(
                exec_count, len(self.queue)+exec_count)
            )
        return len(executed)

    def calculate_speed_distance(self):
        """Calculate current speed and total distance traveled."""
        self.time_prev = self.time
        self.time = time()
        time_delta = self.time - self.time_prev

        self.actual_speed = self.unit.actual_speed()
        self.distance += abs(self.actual_speed*time_delta)

        self.actual_speed_str.set('{} m/s'.format(round(self.actual_speed, 2)))
        self.distance_str.set('{} m'.format(round(self.distance, 2)))

    def update_mode(self):
        """Change mode if new mode is requested."""
        if self.NewMode:
            self.mode = self.NewMode(self.unit)
            self.log.info('mode changed to {}'.format(self.NewMode.__name__))
            self.NewMode = None
    
    def run(self):
        """Run the main loop of the unit thread."""
        self.mode = modes.IdleMode(self.unit)
        self.time_prev = self.time = time()

        while True:
            self.update_mode()
            self.execute_queue()
            self.calculate_speed_distance()
            self.mode = self.mode.run(self.unit)

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
