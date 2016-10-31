from unit import Unit
from time import sleep

channel = 1
error_margin = 10
velocity = 25
distance = 55

def threat():
    unit = Unit('192.168.0.111')
while True:
    prox = unit.ir_sensor.get_prox()
    print(prox)
    if prox <= distance+error_margin:
	    unit.speak('Get out')
	    sleep(2)
		if prox <= distance+error_margin:
		   unit.speak('say hello to my little friend')
		   unit.rotate(100,170)
		   unit.start_gun()
		   sleep(2)
		   unit.stop_gun()
		   
		