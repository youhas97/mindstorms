from time import sleep

class IdleMode():

    """Let unit run idle."""

    def __init__(self, unit):
        unit.stop()

    def run(self, unit):
        sleep(1)
        return self

        
