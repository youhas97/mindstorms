from unit import Unit

def patrol():
    print('hej')
    unit = Unit('192.168.0.111')

    if unit.ir_sensor.get_prox() >= 50:
        
        unit.forward(10)
        
    else:
        unit.stop
        Ev3.speak('u what mate')
        rotate.random.randint()
        unit.forward(20)

patrol()
        
            
