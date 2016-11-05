from unit import Unit
from time import sleep
from patrol_proto import Patrol

channel = 1
error_margin = 10
velocity = 25
distance = 50
def threat():
    unit = Unit('192.168.0.112')
    patrol_mode = Patrol(speed=100)
    while True:
        """checks if encountered object is an intruder and attacks"""
        prox = unit.ir_sensor.get_prox()
        print(prox)
        if prox <= distance:
            unit.stop()
            #checks if object is an intruder and if it moves.
            if unit.check_movement(2,5) and prox <= distance:
                unit.speak('get out')
                sleep(1)
                for seconds in ['five','four','three','two','one']:
                #if the object is still there it counts down, otherwise breaks.
                    if unit.prox()<= distance:
                        unit.speak(seconds)
                    else:
                        break 
                    sleep(1)    
                #if the object is still there after 5 seconds it attacks
                if seconds == 'one':
                    unit.rotate(100,180)
                    sleep(0.8)
                    unit.speak('Say hello to my little friend')
                    sleep(2.6)
                    unit.start_gun(100)
                    sleep(4)
                    unit.stop_gun()
                    sleep(0.5)
                    unit.rotate(100,180)
                    sleep(1.7)
                    #if the object is still there after the atttack it surrenders
                    if unit.prox()<=distance:
                        sleep(0.8)
                        unit.speak('I surrender')
                        sleep(0.5)
                        unit.rotate(100,180)
                        sleep(1.7)
                        unit.forward(100)
                        
                        
        else:
            patrol_mode.run(unit)
threat()
		   
		