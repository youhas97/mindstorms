from src.api.ev3 import Ev3
from time import sleep
from random import randint
test_unit = Ev3('192.168.0.111')
mot_b = test_unit.add_motor('B')
mot_c = test_unit.add_motor('C')
touch_sensor = test_unit.add_sensor(1, 'touch')
color_sensor = test_unit.add_sensor(2, 'color')

def turn_degree_one_track(degree, left, right):
    conversion = 11
    if degree < 0:
        right.run_position_limited(100, -degree*conversion, brake='hold')
    else:
        left.run_position_limited(100, degree*conversion, brake='hold')

def turn_degree_two_track(degree, left, right):
    conversion = 5
    right.run_position_limited(100, -degree*conversion, brake='hold', run=False)
    left.run_position_limited(100, degree*conversion, brake='hold', run=False)
    test_unit.start_motors(['B','C'])

#turn_degree_two_track(360, mot_c, mot_b)
#test_unit.start_motors(['B','C'])
#sleep(2)
#turn_degree_two_track(360, mot_c, mot_b)
#sleep(1)
#test_unit.stop_motors(['B','C'])
#sleep(2)

motors = ['B', 'C']
mot_b.run_forever(100, run=False)
mot_c.run_forever(100, run=False)
#test_unit.start_motors(motors)

color_prev = 0
while True:
    colors = ['no color', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown']
    color = (color_sensor.get_color())
    (colors[color])
    if color != color_prev and color:
        test_unit.speak(colors[color])
        color_prev = color
        sleep(2)
    if touch_sensor.is_pressed():
        test_unit.stop_motors(motors)
        sleep(0.1)
        test_unit.speak('ouch')
        sleep(1)
        mot_b.run_time_limited(-100, 2000, run=False)
        mot_c.run_time_limited(-100, 2000, run=False)
        test_unit.start_motors(motors)
        sleep(2)
        turn_degree_two_track(randint(90,270), mot_c, mot_b)
        sleep(3)
        motors = ['B', 'C']
        mot_b.run_forever(100, run=False)
        mot_c.run_forever(100, run=False)
        test_unit.start_motors(motors)
    sleep(0.1)
