from unit import Unit
from time import sleep

channel = 1
error_margin = 10
velocity = 25
distance = 55

def threat():
    unit = Unit('192.168.0.111')
	
    while True:
        """checks if encountered object is an intruder and attacks"""
        prox = unit.ir_sensor.get_prox()
        print(prox)
        if prox <= distance+error_margin:
            if 
            if prox <= distance+error_margin:
                unit.rotate(100,135)
                sleep(0.8)
                unit.speak('Say hello to my little friend')
                sleep(2.6)
                unit.start_gun(100)
                sleep(4)
                unit.stop_gun()
threat()
		   
		