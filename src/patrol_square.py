from patrol_proto import Patrol
from unit import Unit
def patrol_blacksquare():
    unit = Unit('192.168.0.112')
    patrol_mode = Patrol(speed=100)
    while True:
        patrol_mode.run(unit)
patrol_blacksquare()