import random
import data_types.constants as constants

from data_types.brain import Brain


class Creature(object):

    def __init__(self, color=(0, 0, 0), x=0, y=0, ID=0, newBrain=True):
        """initialize color and x and y coordinates"""
        self.color = color
        self.ID = ID

        self.age = 0
        self.x = x
        self.y = y

        # 0=west, 1=north, 2=east, 3=south
        self.facing = random.randint(0, 3)  # east
        self.will_move = False

        self.brain = Brain(self)
        if newBrain:
            self.brain.generateBrain()

        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def dist(self, direction):
        if direction == "west":
            return self.x
        if direction == "north":
            return self.y
        if direction == "east":
            return constants.pg_size - self.x
        if direction == "south":
            return constants.pg_size - self.y

    def choose_move_direction(self, direction):
        if direction == "west":
            self.facing = 0
        elif direction == "north":
            self.facing = 1
        elif direction == "east":
            self.facing = 2
        elif direction == "south":
            self.facing = 3
        elif direction == "left":
            self.facing = (self.facing - 1) % 4
        elif direction == "right":
            self.facing = (self.facing + 1) % 4
        elif direction == "backward":
            self.facing = (self.facing + 2) % 4
        elif direction == "random":
            self.facing = random.randint(0, 3)

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

    def get_facing(self):
        return self.facing

    def set_facing(self, value):
        self.facing = value

    def get_will_move(self):
        return self.will_move

    def set_will_move(self, value):
        self.will_move = value
