import random
from enum import IntEnum, Enum

import data_types.constants as constants
from data_types.brain import Brain


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


class Turn(Enum):
    LEFT = "left"
    RIGHT = "right"
    BACKWARD = "backward"
    RANDOM = "random"


class Creature(object):

    def __init__(
        self,
        color: tuple[int, int, int] = (0, 0, 0),
        x: int = 0,
        y: int = 0,
        ID: int = 0,
        create_new_brain: bool = True,
    ):
        """initialize color and x and y coordinates"""
        self.color = color
        self.ID = ID

        self.age = 0
        self.x = x
        self.y = y

        # 0=west, 1=north, 2=east, 3=south
        self.facing_direction: Direction = random.choice(list(Direction))
        self.will_move = False

        self.brain = Brain(self)
        if create_new_brain:
            self.brain.generate_brain()

        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def distance_to_direction(self, direction):
        if direction == Direction.WEST:
            return self.x
        if direction == Direction.NORTH:
            return self.y
        if direction == Direction.EAST:
            return constants.pg_size - self.x
        if direction == Direction.SOUTH:
            return constants.pg_size - self.y

    def choose_move_direction(self, command):
        if command in list(Direction):
            self.facing_direction = command

        elif command == Turn.LEFT:
            self.facing_direction = self.facing_direction.turn_left()
        elif command == Turn.RIGHT:
            self.facing_direction = self.facing_direction.turn_right()
        elif command == Turn.BACKWARD:
            self.facing_direction = self.facing_direction.turn_backward()
        elif command == Turn.RANDOM:
            self.facing_direction = Direction.random()

    def move(self, direction):
        self.choose_move_direction(direction)
        self.will_move = True

    # Getter and setter for x
    def get_x(self):
        return self.x

    def set_x(self, value):
        self.x = value

    # Getter and setter for y
    def get_y(self):
        return self.y

    def set_y(self, value):
        self.y = value

    # Getter for brain
    def get_brain(self):
        return self.brain

    def set_brain(self, value):
        self.brain = value

    # Getter for age
    def get_age(self):
        return self.age

    def set_age(self, value):
        self.age = value

    def get_facing_direction(self):
        return self.facing_direction

    def set_facing_direction(self, value):
        self.facing_direction = value

    def get_will_move(self):
        return self.will_move

    def set_will_move(self, value):
        self.will_move = value
