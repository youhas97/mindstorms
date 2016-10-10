from api.ev3 import Ev3

test_unit = Ev3('192.168.0.111')
ir_sensor = test_unit.add_sensor(3, 'IR')

motor_left = test_unit.add_motor('C')
motor_right = test_unit.add_motor('B')

def forward(motor):
    motor.run_forever(100)

def run_sim(m1, m2, v1, v2):
    m1.run_forever(v1, run=False)
    m2.run_forever(v2, run=False)
    test_unit.start_motors(['C', 'B'])

def backward(motor):
    motor.run_forever(-100)
    
def stop(motor):
    motor.stop()

channel = 1

buttons_prev = [False, False, False, False]

while True:
    remote = ir_sensor.get_remote()
    button = remote[channel-1]
    buttons = [False, False, False, False]

    if button == 0:
        pass
    elif button == 1:
        buttons[0] = True
    elif button == 2:
        buttons[1] = True
    elif button == 3:
        buttons[3] = True
    elif button == 4:
        buttons[4] = True
    elif button == 5:
        buttons[0] = True
        buttons[2] = True
    elif button == 6:
        buttons[0] = True
        buttons[3] = True
    elif button == 7:
        buttons[1] = True
        buttons[2] = True
    elif button = 8:
        buttons[1] = True
        buttons[4] = True


    #print(ir_sensor.get_seek())
    #print(ir_sensor.get_prox())
