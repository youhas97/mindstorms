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

    def run(unit):
        direction = (0, 0)
        keys_pressed = (0, 0)
        for key, key_state in self.key_states.items():
            if not key_state: continue
            for axis in range(2):
                direction_value = self.dir_keys[key][axis]
                if not direction_value is None:
                    direction[axis] += direction_value
                    keys_pressed[axis] += 1
        for axis in range(2): direction[axis] /= keys_pressed[axis]

        self.
