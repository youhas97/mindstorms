from api.ev3 import Ev3

from time import sleep

class Unit(Ev3):
    def __init__(self, ip):
        super().__init__(ip)
        self.wheels = ['D', 'A']
        self.left = self.add_motor(self.wheels[0])
        self.right = self.add_motor(self.wheels[1])
        self.gun = self.add_motor('B')
        self.ir_sensor = self.add_sensor(2, 'IR')
        self.color_sensor = self.add_sensor(3, 'color')

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

    def shoot(self):
        self.gun.run_forever(10)

def main():
    unit = Unit(
            ip = '192.168.0.111', 
            wheels = ['B', 'C'],
            gun = 'A')

if __name__ == '__main__':
    main()
