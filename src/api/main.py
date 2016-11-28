#Requires a motor on port B and C
from ev3 import Ev3
import time
#Replace with your ip
test_unit=Ev3("169.254.72.80")
left=test_unit.add_motor("B")
right=test_unit.add_motor("C")

left.run_position_limited(100,720,"brake",False)
right.run_position_limited(100,720,"brake",False)
test_unit.start_motors(["B","C"])
time.sleep(3)

left.run_position_limited(100,720,"brake",False)
right.run_position_limited(-100,720,"brake",False)
test_unit.start_motors(["B","C"])
time.sleep(3)

left.run_position_limited(100,720,"brake",False)
right.run_position_limited(100,720,"brake",False)
test_unit.start_motors(["B","C"])
time.sleep(3)

left.run_position_limited(-100,720,"brake",False)
right.run_position_limited(100,720,"brake",False)
test_unit.start_motors(["B","C"])
time.sleep(3)

test_unit.play_wav("t2_learning_computer_x")