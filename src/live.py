import os


class LiveMode():
    
    def __init__(unit, master):
        os.system('xset r off')
        self.master = master
        self.dir_keys = {
            'Left': (-2, None),
            'Right': (2, None),
            'Up': (0, 1),
            'Down': (0, -1)
        }
        self.dir_key_states = {key: False for key in self.keys}
        self.unit.stop()

        self.bind_keys()

    def bind_keys():
        for key in self.keys:
            self.master.bind('<{}>'.format(key), self.key_pressed)
            self.master.bind('<KeyRelease-{}>'.format(key), self.key_released)

    def dir_key_pressed(event):
        key = event.keysym
        self.dir_key_states[key] = True

    def dir_key_released(event):
        key = event.keysym
        self.dir_key_states[key] = False

    def calculate_movement(self):
        """Calculate x,y direction from keys.
        
        Description:
        Depending on current keys pressed a turn radius and
        a positive or negative speed multiplier will be 
        calculated.
       
        Returns:
            direction -- direction in [-2, 2]
            speed -- speed in [-1,1]
        """
        dirs = []
        speeds = []
        any_key_pressed = False
        for key, key_state in self.dir_key_states:
            if key_state:
                any_key_pressed = True
                direction = self.dir_keys[key][0]
                speed = self.dir_keys[key][1]
                if not direction is None: dirs.append(direction)
                if not speed is None: speeds.append(speed)

        direction = sum(dirs)/len(dirs)
        speed = sum(speeds)/len(speeds) if any_key_pressed else 0
        return direction, speed

    def run(unit):
        direction, speed = self.calculate_movement()

        self.unit.set_speed(self.speed*speed)
        self.unit.turn(direction)
