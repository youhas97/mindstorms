from api.ev3 import Ev3

test_unit = Ev3('192.168.43.11')
ir_sensor = test_unit.add_sensor(2,'IR')

motor_left = test_unit.add_motor('D')
motor_right = test_unit.add_motor('A')

def forward():
    motor_left.run_forever(100)
    motor_right.run_forever(100)
    test_unit.start_motors(['B', 'C'])

def run_sim(m1, m2, v1, v2):
    m1.run_forever(v1, run=False)
    m2.run_forever(v2, run=False)
    test_unit.start_motors(['C', 'B'])

def backward(motor):
    motor.run_forever(-100)
    
def stop():
    test_unit.stop_motors(['B', 'C'])

def turn_degree_two_track(degree, left, right):
    conversion = 5
    right.run_position_limited(100, -degree*conversion, brake='hold', run=False)
    left.run_position_limited(100, degree*conversion, brake='hold', run=False)
    test_unit.start_motors(['B','C'])

def turn_right(vel):
    motor_right.run_forever(-vel, run=False)
    motor_left.run_forever(vel, run=False)
    test_unit.start_motors(['D', 'A'])

def turn_left(vel):
    motor_right.run_forever(vel, run=False)
    motor_left.run_forever(-vel, run=False)
    test_unit.start_motors(['C', 'B'])

channel = 1
error_margin = 5
velocity = 25

"""
while True:
    angle, distance = ir_sensor.get_seek()[channel-1]
    if angle > error_margin: turn_right(velocity)
    elif angle < -error_margin: turn_left(velocity)
    else: forward()
    print(angle, distance)
"""

velocity = 1

while True:
    angle, distance = ir_sensor.get_seek()[channel-1]
    turn_right(-min(int(velocity*angle), 100))
