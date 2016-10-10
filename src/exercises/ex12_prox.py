from api.ev3 import Ev3

test_unit = Ev3('192.168.0.111')
ir_sensor = test_unit.add_sensor(3, 'IR')

motor_left = test_unit.add_motor('C')
motor_right = test_unit.add_motor('B')

def forward(vel):
    motor_left.run_forever(vel)
    motor_right.run_forever(vel)
    test_unit.start_motors(['B', 'C'])

def run_sim(m1, m2, v1, v2):
    m1.run_forever(v1, run=False)
    m2.run_forever(v2, run=False)
    test_unit.start_motors(['C', 'B'])

def backward(vel):
    motor_left.run_forever(-vel)
    motor_right.run_forever(-vel)
    test_unit.start_motors(['B', 'C'])

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
    test_unit.start_motors(['C', 'B'])

def turn_left(vel):
    motor_right.run_forever(vel, run=False)
    motor_left.run_forever(-vel, run=False)
    test_unit.start_motors(['C', 'B'])

channel = 1
error_margin = 10
velocity = 25
distance = 55

while True:
    prox = ir_sensor.get_prox()
    print(prox)
    if prox < distance: backward(velocity)
    elif prox > distance+error_margin: forward(velocity)
    else: stop()

