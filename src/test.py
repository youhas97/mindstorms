#!/bin/env python3

from unit import Unit
from mockbot import MockedEv3

def main():
    unit = Unit('192.168.43.11')

    while True:
        mode = patrol(unit)

def patrol(unit):
    print(unit.prox())
    return patrol


def follow_tape(unit):
    return follow_tape


if __name__ == '__main__':
    main()
