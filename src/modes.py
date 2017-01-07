from unit import Unit
from time import sleep
from os import system


class IdleMode():
    """Let unit run idle

    Public methods:
        run -- Run an iteration of the mode.
    """

    def __init__(self, unit):
        unit.stop()

    def run(self, unit):
        sleep(1)
        return self


class Patrol():
    """Patrol the room either peacefully or guard it.

    Public methods:
        run -- Run an iteration of the mode.
    """
    PEACEFUL = 0
    GUARD = 1

    DISTANCE_THRESHOLD = 40

    def __init__(self, unit, mode=0):
        self.speed = 40
        self.mode_changed = False
        self.patrol_mode = mode
        self.patrol_square = True

    def set_speed(self, speed):
        """sets the speed"""
        self.speed = speed

    def set_patrol_mode(self, mode):
        """switches mode"""
        if self.patrol_mode != mode:
            self.mode_changed = True

    def update_mode(self, unit):
        """updates mode"""
        if self.mode_changed:
            self.toggle_mode(unit)
            self.mode_changed = False

    def activation_dance(self, unit):
        """dance used for activation of robot"""
        unit.stop()
        unit.rotate_forever(100)
        sleep(0.15)
        unit.rotate_forever(-100)
        sleep(0.1)
        unit.stop()

    def toggle_mode(self, unit):
        """toggles between peaceful and guard mode"""
        self.patrol_mode ^= True
        MODE_NAMES = ['peaceful', 'guard']
        self.activation_dance(unit)
        unit.speak('{} mode activated'.format(MODE_NAMES[self.patrol_mode]))
        sleep(2.5)

    def object_in_prox(self):
        """checks if object is in sight range"""
        return self.prox < Patrol.DISTANCE_THRESHOLD

    def run(self, unit):
        """run an iteration of patrol"""
        self.prox = unit.ir_sensor.get_prox()
        unit.forward(self.speed)

        self.update_mode(unit)
        if self.patrol_square and unit.reflect() < 15:
            unit.change_direction(self.speed)
        elif self.object_in_prox():
            if self.patrol_mode == Patrol.PEACEFUL:
                unit.stop()
                unit.speak('oh sorry')
                sleep(2)
                unit.change_direction(self.speed)
            elif self.patrol_mode == Patrol.GUARD:
                return threat.ThreatMode(unit, speed=self.speed)
        return self


class FollowTape():
    """Follow tape on the floor.

    Public methods:
        run -- Run an iteration of the mode.
    """

    def __init__(self, unit):
        self.hist_len = 5

        self.offset = 0
        self.offset_prev = 0
        self.offset_hist = [0 for _ in range(self.hist_len)]

        self.refl = unit.reflect()
        self.refl_prev = self.refl
        self.refl_min = self.refl
        self.refl_max = self.refl
        self.refl_interval = 0

        self.min_speed = 25

        self.turn = 0

        unit.set_speed(20)

    def update_reflection(self, unit):
        """Parse reflection from unit and set min/max values."""
        self.refl_prev = self.refl
        self.refl = unit.reflect()
        self.refl_min = min(self.refl_min, self.refl)
        self.refl_max = max(self.refl_max, self.refl)
        self.refl_interval = self.refl_max - self.refl_min

    def calculate_offset(self):
        """Calculate offset value to edge of tape.

        Description:
            The reflection has a min and max value. The value
            in between (pivot) min and max is considered the
            edge of the tape. The offset is set to 1 if
            reflection is at max, 0 if in the middle, -1 if
            at min, and any value between those (continous).
        """
        self.offset_prev = self.offset
        pivot = (self.refl_max - self.refl_min) / 2 + self.refl_min
        if self.refl_interval != 0:
            self.offset = (self.refl-pivot) / (self.refl_interval/2)
        else:
            self.offset = 0
        self.offset_hist.append(self.offset)
        self.offset_hist.pop(0)

    def adjust_speed(self, unit):
        """Control speed of unit.

        Description:
            Increases speed if reflection has low variation.
            Decreases speed if reflection has high variation.
        """
        if abs(self.refl - self.refl_prev) < 2:
            unit.set_speed(unit.speed+1)
        else:
            unit.set_speed(unit.speed-1)
            if unit.speed < self.min_speed:
                unit.set_speed(self.min_speed)

    def adjust_turn(self, unit):
        """Control turn value for unit with PD controller."""
        proportional_coeff = 1
        derivative_coeff = 0.75

        self.turn = proportional_coeff * self.offset \
                  + derivative_coeff * (self.offset - self.offset_prev)

        self.turn /= float(proportional_coeff + derivative_coeff*2)
        self.turn *= 2 # max turn value is 2 instead of 1

    def run(self, unit):
        """Run an iteration of the follow tape mode.

        Description:
            Should be run from a loop. Executes all
            methods needed to follow the tape. Variables
            accross iterations are stored in the object.
        """
        self.update_reflection(unit)
        if self.refl_interval > 10:
            self.calculate_offset()
            self.adjust_speed(unit)
            self.adjust_direction()
            self.adjust_turn(unit)

        unit.turn(self.turn)

        return self


class ThreatMode():
    """Make unit react to a threat.

    Public methods:
        run -- Run an iteration of the mode.
    """

    def __init__(self, unit, speed=40):
        self.speed = speed
        self.distance = 50

    def detect_threat(self, unit):
        """
        detect moving object that can be classed as a threat
        """
        if unit.prox() <= self.distance:
            unit.stop()
            sleep(0.2)
            if unit.check_movement(2, 2) and unit.prox() <= self.distance:
                unit.speak('get out')
                sleep(1)
                for seconds in ['five','four','three','two','one']:
                    if unit.prox() <= self.distance:
                        unit.speak(seconds)
                        sleep(1)
                    else:
                        unit.stop()
                        return False
                return True
            else:
                unit.change_direction(self.speed)
                return Patrol(unit, patrol.Patrol.GUARD)

    def shoot(self, unit):
        """
        Rotate and fire a shot
        """
        unit.rotate(100,150)
        sleep(0.8)
        unit.speak('Say hello to my little friend')
        sleep(3.3)
        unit.shoot(1)
        sleep(1)
        unit.rotate(100,180)
        sleep(2)

    def run(self, unit):
        """
        run iteration of threat
        """
        prox = unit.ir_sensor.get_prox()
        if self.detect_threat(unit):
            self.shoot(unit)
            if unit.prox() <= self.distance:
                return Surrender(unit)
        else:
            return Patrol(unit, Patrol.GUARD)
        return self


class Surrender(FollowTape):
    """Surrender to a threat and find the closest corner.

    Public methods:
        run -- Run an iteration of the mode.
    """
    def __init__(self, unit):
        super().__init__(unit)

    def __init__(self, unit):
        super().__init__(unit)
        unit.speak('I surrender')
        sleep(2)
        unit.rotate(100,180)
        sleep(2.3)
        unit.forward(50)

    def in_corner(self, unit):
        """
        checks if robot is in corner
        
        description:
            There is a red tape on the outside of every corner which the color
            sensor picks up on and registers as a corner
        """
        return (20 <= self.refl <= 39 or self.refl >=45) and unit.color() == 'red'

    def outside_corner(self, unit):
        """
        checks for rare occasion where robot doesnt register corner but movement
        pattern indicates that a corner is closeby
        """
        if (-0.8 < self.offset_hist[0] < 0 < self.offset_hist[1] < 0.8) \
        or (-0.8 < self.offset_hist[1] < 0 < self.offset_hist[0] < 0.8):
            if abs(self.offset_hist[-1]) >= 0.85:
                for offset in self.offset_hist[1:-1]:
                    if abs(offset) >= 0.8:
                        pass
                    else:
                        return False
                return True
        return False

    def run(self, unit):
        """runs an iteration of surrender"""
        super().run(unit)
        if self.in_corner(unit) or self.outside_corner(unit):
            return IdleMode(unit)
        return self


class FollowRemote(FollowTape):
    """Make unit go to the remote.

    Public methods:
        run -- Run an iteration of the mode.
    """

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


class LiveMode():
    """Control unit with keyboard.

    Public methods:
        run -- Run an iteration of the mode.
    """
    
    def __init__(self, unit):
        self.unit = unit

        self.initiate_keys()

        self.speed = 100
        self.shoot_flag = False
        unit.stop()

        system('xset r off') # repeat keys mess up key states

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
        """Set key state to pressed."""
        key = event.keysym
        self.dir_key_states[key] = True

    def dir_key_released(self, event):
        """Set key state to released."""
        key = event.keysym
        self.dir_key_states[key] = False

    def shoot(self, event):
        """Make unit shoot next run iteration."""
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
        """run an iteration of Live Mode"""
        direction, speed = self.calculate_movement()

        self.unit.set_speed(self.speed*speed)
        self.unit.turn(direction)

        if self.shoot_flag:
            self.unit.shoot()
            self.shoot_flag = False
        
        return self
