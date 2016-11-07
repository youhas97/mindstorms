import matplotlib.pyplot as plt

from unit import Unit

unit = Unit('192.168.0.112')
data_function = unit.reflect()

try:
    i = 0
    while True:
        value = data_function()
        plt.scatter(i, value)
        plt.pause(0.01)
        i += 1
except KeyboardInterrupt:
    pass
