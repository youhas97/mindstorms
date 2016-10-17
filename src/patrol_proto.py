from unit import Unit
from time import sleep
from random import randint, choice

channel = 1
error_margin = 10
velocity = 25
distance = 40

def patrol():
    print('hej')
    unit = Unit('192.168.0.111')
    
    while True:
	    direction = choice([-1,1])
	    print(direction)
	    prox = unit.ir_sensor.get_prox()
	    print(prox)
	    if prox >= distance:
		    unit.forward(100)
	    elif prox <= distance+error_margin:
		    unit.stop()
		    unit.speak('u what mate')
		    sleep(1)
		    unit.rotate(100,direction*randint(90,180))
		    sleep(2)
patrol()
        
            
