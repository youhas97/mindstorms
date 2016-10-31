from unit import Unit
from time import sleep

channel = 1
error_margin = 10
velocity = 25
distance = 50
def threat():
    unit = Unit('192.168.0.111')
	
    while True:
        """checks if encountered object is an intruder and attacks"""
        prox = unit.ir_sensor.get_prox()
        print(prox)
        if prox <= distance:
            if unit.check_movement(2,5) and prox <= distance:
                unit.speak('get out')
                sleep(1)
                for seconds in ['five','four','three','two','one']:
                    if unit.prox()<= distance:
                        unit.speak(seconds)
                    else:
                        break 
                    sleep(1)    
                if seconds == 'one':
                    unit.rotate(100,140)
                    sleep(0.8)
                    unit.speak('Say hello to my little friend')
                    sleep(2.6)
                    unit.start_gun(100)
                    sleep(4)
                    unit.stop_gun()
                       
threat()
		   
		