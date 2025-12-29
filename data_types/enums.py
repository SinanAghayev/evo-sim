import random
from enum import IntEnum, Enum


class Direction(IntEnum):
    WEST: 0
    NORTH: 1
    EAST: 2
    SOUTH: 3

    def turn_left(self):
        return Direction((self - 1) % 4)

    def turn_right(self):
        return Direction((self + 1) % 4)

    def turn_backward(self):
        return Direction((self + 2) % 4)

    @staticmethod
    def random():
        return Direction(random.randint(0, 3))

    def delta(self):
        return {
            Direction.WEST: (-1, 0),
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
        }[self]


class Turn(Enum):
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    BACKWARD = "backward"
    RANDOM = "random"
