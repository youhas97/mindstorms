from api.ev3 import Ev3
from time import sleep, time

class Unit(Ev3):
    """Handle unit."""

    def __init__(self, ip):
        super().__init__(ip)
        
        # ports
        left_motor = 'D'
        right_motor = 'A'
        gun = 'B'
        ir_sensor = 2
        color_sensor = 4

        self.wheels = [left_motor, right_motor]
        self.left = self.add_motor(self.wheels[0])
        self.right = self.add_motor(self.wheels[1])
        self.gun = self.add_motor(gun)
        self.ir_sensor = self.add_sensor(ir_sensor, 'IR')
        self.color_sensor = self.add_sensor(color_sensor, 'color')

        self.speed = 0

    def set_speed(self, speed):
        """Set speed of unit"""
        self.speed = min(max(speed, -100), 100)
        return self.speed

    def forward(self, speed):
        """Make the unit go forward."""
        self.set_speed(speed)
        self.left.run_forever(-self.speed, run=False)
        self.right.run_forever(-self.speed, run=False)
        self.start_motors(self.wheels)
    
    def rotate_forever(self, speed):
        """Make the unit rotate."""
        self.set_speed(speed)
        self.left.run_forever(-self.speed, run=False)
        self.right.run_forever(self.speed, run=False)
        self.start_motors(self.wheels)

    def turn(self, direction):
        """Turn unit while moving.
        
        Params:
            direction -- float between -2 and 2 indicating
                         turn radius and direction

        Exceptions:
            ValueError -- if direction is not within [-2,2] range.

        Examples:
            self.speed = 40, direction = 1:
            left_speed = 80, right_speed = 0 (unit turns right)

            self.speed = 60, direction = -0.5:
            left_speed = 40, right_speed = 80 (unit turns left)

            self.speed = 90, direction = 0.75:
            left_speed = 100, right_speed = 25

        Derivation:
            speed_ratio/direction decides the ratio of speed
            between the two wheels, therefore deciding the 
            turn radius:
                min_speed / max_speed = speed_ratio
                    --> min_speed = max_speed * speed_ratio

            In order to not slow down the unit during turning, 
            the average speed of the wheels should be the 
            current speed of the unit (as long as it doesnt
            exceed motors' the speed limit):
                ( max_speed + min_speed ) / 2 = self.speed
                    --> max_speed = 2 * speed_ratio / self.speed
        """

        if -1 <= direction <= 1:
            # TODO does not work if speed is negative, fix
            speed_ratio = 1 - abs(direction)
            max_speed = 2 / (speed_ratio + 1) * self.speed
            if max_speed > 100: max_speed = 100
            min_speed = max_speed * speed_ratio
        elif -2 <= direction <= 2:
            max_speed = self.speed
            min_speed = max_speed - abs(direction) * self.speed
        else:
            raise ValueError('input outside range [-2,2] -- {}'.format(direction))

        if direction > 0: left_speed, right_speed = max_speed, min_speed
        else:             left_speed, right_speed = min_speed, max_speed
       
        self.left.run_forever(-round(left_speed))
        self.right.run_forever(-round(right_speed))

    def stop(self):
        """Stop the unit."""
        self.speed = 0
        self.stop_motors(self.wheels)

    def rotate(self, speed, degrees):
        """Rotate the unit."""
        self.speed = 0
        ANGLE_DEGREE = 5.3
        rotation = int(ANGLE_DEGREE*degrees)
        self.right.run_position_limited(speed, rotation, run=False)
        self.left.run_position_limited(speed, -rotation, run=False)
        self.start_motors(self.wheels)

    def shoot(self, shots=1):
        """Fires amount of shots you want"""
        ANGLE_BULLET = 1190
        self.gun.run_time_limited(100, ANGLE_BULLET*shots)

    def seek(self, channel):
        """Parse seek values from IR sensor """
        return self.ir_sensor.get_seek()[channel-1]

    def prox(self):
        """Parse proximity value from IR sensor."""
        return self.ir_sensor.get_prox()

    def color(self):
        """Parse color from color sensor and return corresponding string."""
        color_number = self.color_sensor.get_color()
        color_tuple = ('none', 'black', 'blue', 'green',
                        'yellow', 'red', 'white', 'brown')
        return color_tuple[color_number]

    def reflect(self):
        """Parse reflection value from color sensor"""
        return self.color_sensor.get_reflect()

    def actual_speed(self):
        left = self.left.get_attribute('speed')
        right = self.right.get_attribute('speed')
        return -(left+right)/2

    def check_movement(self, time_interval, distance_margin):
        """Check for movement with proximity sensors.

        Params:
            time_interval -- the maximum time to wait for 
                             movement
            distance_margin -- the variation in distance
                               which counts as movement

        Return:
            True, if movement has been detected, otherwise False.
        """
        time_start = time()
        distance_min = distance_max = self.prox()
        while time()-time_start < time_interval:
            distance = self.prox()
            distance_min = min(distance, distance_min)
            distance_max = max(distance, distance_max)
            if distance_max-distance_min > distance_margin: return True

if __name__ == '__main__':
    unit = Unit('192.168.0.112')
    unit.forward(10)
    unit.turn(2)
    while True:
        pass
