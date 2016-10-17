from unit import Unit

def main():
    unit = Unit('192.168.0.111')
    unit.forward(20)
    channel = 1
    FOV = 90
    RANGE = 20
    while True:
        angle, distance = unit.seek(channel)
        if abs(angle) < FOV/2 and distance < RANGE:
            mode = guard()


if __name__ == '__main__':
    main()
