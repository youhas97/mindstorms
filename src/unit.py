from api.ev3 import Ev3
from time import sleep, time

class Unit(Ev3):
    def __init__(self, ip):
        super().__init__(ip)
        
        # ports
        left_motor = 'D'
        right_motor = 'A'
        gun = 'B'
        ir_sensor = 2
        color_sensor = 3

        self.wheels = [left_motor, right_motor]
        self.left = self.add_motor(self.wheels[0])
        self.right = self.add_motor(self.wheels[1])
        self.gun = self.add_motor(gun)
        self.ir_sensor = self.add_sensor(ir_sensor, 'IR')
        self.color_sensor = self.add_sensor(color_sensor, 'color')

        self.speed = 0

    def forward(self, speed):
        """Make the unit go forward."""
        self.speed = speed
        self.left.run_forever(-self.speed, run=False)
        self.right.run_forever(-self.speed, run=False)
        self.start_motors(self.wheels)

    def turn(self, direction):
        """Turn unit while moving.
        
        Params:
            direction -- float between -1 and 1 indicating
                         turn radius and direction
        Examples:
            self.speed = 40, direction = 1:
            left_vel = 80, right_vel = 0 (unit turns right)

            self.speed = 60, direction = -0.5:
            left_vel = 40, right_vel = 80 (unit turns left)

            self.speed = 90, direction = 0.75:
            left_vel = 100, right_vel = 25

        Derivation:
            vel_quotient/direction decides the ratio of speed
            between the two wheels, therefore deciding the 
            turn radius:
                min_vel / max_vel = vel_quotient
                    --> min_vel = max_vel * vel_quotient

            In order to not slow down the unit during turning, 
            the average speed of the wheels should be the 
            current speed of the unit (as long as it doesnt
            exceed motors' the speed limit):
                ( max_vel + min_vel ) / 2 = self.speed
                    --> max_vel = 2 * vel_quotient / self.speed
        """
        assert -1 <= direction <= 1
        vel_quotient = 1 - abs(direction)
        
        max_vel = 2 / (vel_quotient + 1) * self.speed
        if max_vel > 100: max_vel = 100
        min_vel = max_vel * vel_quotient
        if direction > 0: left_vel, right_vel = max_vel, min_vel
        else:             left_vel, right_vel = min_vel, max_vel

        self.left.run_forever(-round(left_vel))
        self.right.run_forever(-round(right_vel))

    def stop(self):
        """Stop the unit."""
        self.speed = 0
        self.stop_motors(self.wheels)

    def rotate(self, speed, degrees):
        """Rotate the unit."""
        self.speed = 0
        conversion = 5.3
        rotation = int(conversion*degrees)
        self.right.run_position_limited(speed, rotation, run=False)
        self.left.run_position_limited(speed, -rotation, run=False)
        self.start_motors(self.wheels)
    
    def start_gun(self, speed):
        """Fire the unit's gun."""
        self.gun.run_forever(speed)
		
    def stop_gun(self):
        """Stop the unit's gun."""
        self.gun.stop()

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
