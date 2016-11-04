from unit import Unit
from time import sleep
from random import randint, choice

channel = 1
error_margin = 10
velocity = 25
distance = 40
unit = Unit('192.168.0.111')

class Patrol():
    
    def patrol():
        direction = choice([-1,1])
    	print(direction)
    	prox = unit.ir_sensor.get_prox()
    	reflection = unit.color_sensor.get_reflect()
    	print(prox)
    	if prox >= distance or reflection > 7:
    		unit.forward(100)
    	elif prox <= distance+error_margin:
    		unit.stop()
    		unit.speak('u what mate')
    		sleep(1)
    		unit.rotate(100,direction*randint(90,180))
    		sleep(2)
        elif reflection <=7:
            unit.stop()
            unit.rotate(100,direction*randint(90,180))
            sleep(2)
		
patrol = Patrol.patrol()
        
            
