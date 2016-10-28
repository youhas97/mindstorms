from api.ev3 import Ev3

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

    def forward(self, velocity):
        self.left.run_forever(-velocity, run=False)
        self.right.run_forever(-velocity, run=False)
        self.start_motors(self.wheels)

    def stop(self):
        self.stop_motors(self.wheels)

    def rotate(self, velocity, degrees):
        conversion = 5.3
        rotation = int(conversion*degrees)
        self.right.run_position_limited(velocity, rotation, run=False)
        self.left.run_position_limited(velocity, -rotation, run=False)
        self.start_motors(self.wheels)

    def seek(self, channel):
        return self.ir_sensor.get_seek()[channel-1]

    def prox(self):
        return self.ir_sensor.get_prox()

    def shoot(self):
        self.gun.run_forever(10)

def main():
    unit = Unit(
            ip = '192.168.0.111', 
            wheels = ['B', 'C'],
            gun = 'A')

if __name__ == '__main__':
    main()
