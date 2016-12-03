import os

class LiveMode():
    
    def __init__(self, unit):
        os.system('xset r off') # repeat keys mess up key states
        self.unit = unit

        self.initiate_keys()

        self.speed = 100
        self.shoot_flag = False
        unit.stop()

    def initiate_keys(self):
        """Create instance variables for keys.

        Description:
            Set up a dict with constants that define
            properties of direction keys and a dict that
            stores current state (pressed/not_pressed).
        """
        TURN_RATE = 2
        TURN_SPEED = 0.5
        self.dir_keys = {
            'Left': (-TURN_RATE, TURN_SPEED),
            'Right': (TURN_RATE, TURN_SPEED),
            'Up': (0, 1),
            'Down': (0, -1)
        }
        self.dir_key_states = {key: False for key in self.dir_keys}

    def bind_keys(self, master):
        """Bind keys to functions."""
        for key in self.dir_keys:
            master.bind('<{}>'.format(key), self.dir_key_pressed)
            master.bind('<KeyRelease-{}>'.format(key), self.dir_key_released)
        master.bind('<space>', self.shoot)

    def dir_key_pressed(self, event):
        key = event.keysym
        self.dir_key_states[key] = True

    def dir_key_released(self, event):
        key = event.keysym
        self.dir_key_states[key] = False

    def shoot(self, event):
        self.shoot_flag = True
        
    def calculate_movement(self):
        """Calculate x,y direction from keys.
        
        Description:
            With regard to current keys pressed a turn radius
            and speed multiplier is calculated.
       
        Returns:
            direction -- direction in [-2, 2]
            speed -- speed in [-1,1]
        """
        dirs = []
        speeds = []
        any_key_pressed = False
        for key, key_state in self.dir_key_states.items():
            if key_state:
                any_key_pressed = True
                direction = self.dir_keys[key][0]
                speed = self.dir_keys[key][1]
                dirs.append(direction)
                speeds.append(speed)

        if any_key_pressed:
            direction = sum(dirs)/len(dirs)
            speed = sum(speeds)/len(speeds)
        else:
            direction = speed = 0
        return direction, speed

    def run(self, unit):
        direction, speed = self.calculate_movement()

        self.unit.set_speed(self.speed*speed)
        self.unit.turn(direction)

        if self.shoot_flag:
            self.unit.shoot()
            self.shoot_flag = False
        
        return self


if __name__ == '__main__':
    from unit import Unit
    unit = Unit('192.168.0.112')
    mode = LiveMode(unit)
    while True:
        mode.run()
