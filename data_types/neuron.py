import random

import data_types.constants as constants


class Neuron(object):
    # fromTo : 0 if from, 1 if to

    # Types:
    # 0=age, 1=x_coord, 2=y_coord,
    # 3=dist_to_west, 4=dist_to_east, 5=dist_to_north, 6=dist_to_south
    # 7,8,9= internal neuron
    # 10=moveWest, 11=moveNorth, 12=moveEast, 13=moveSouth
    # 14=moveLeft, 15=moveForward, 16=moveRight, 17=moveBackward
    # 18=moveRandom, 19=nothing
    # 20=turnLeft, 21=turnRight
    # (not active) 22=kill

    input_neurons = [
        "age",
        "x_coord",
        "y_coord",
        "dist_to_west",
        "dist_to_east",
        "dist_to_north",
        "dist_to_south",
    ]
    output_neurons = [
        "moveWest",
        "moveNorth",
        "moveEast",
        "moveSouth",
        "moveLeft",
        "moveForward",
        "moveRight",
        "moveBackward",
        "moveRandom",
        "nothing",
        "turnLeft",
        "turnRight",
    ]
    internal_neurons = ["internal" + str(i) for i in range(3)]
    all_neuron_types = input_neurons + output_neurons + internal_neurons
    from_neurons = input_neurons + internal_neurons
    to_neurons = output_neurons + internal_neurons
    all_neuron_counts = {i: 0 for i in all_neuron_types}
    activated_neurons = {i: 0 for i in to_neurons}

    def __init__(self, fromTo, neuronType, creature):
        self.fromTo = fromTo
        self.neuronType = neuronType
        self.creature = creature

        self.temp_value = 0
        self.value = 0

        self.creature.brain.allNeurons[neuronType] = self

    def getValue(self):
        if self.neuronType == "age":
            self.value = self.creature.get_age() / constants.MAX_MOVES
        elif self.neuronType == "x_coord":
            self.value = self.creature.x / constants.pg_size
        elif self.neuronType == "y_coord":
            self.value = self.creature.y / constants.pg_size
        elif self.neuronType == "dist_to_west":
            self.value = self.creature.dist("west") / constants.pg_size
        elif self.neuronType == "dist_to_east":
            self.value = self.creature.dist("east") / constants.pg_size
        elif self.neuronType == "dist_to_north":
            self.value = self.creature.dist("north") / constants.pg_size
        elif self.neuronType == "dist_to_south":
            self.value = self.creature.dist("south") / constants.pg_size
        return self.value

    def activate(self):
        self.activated_neurons[self.neuronType] += 1
        # print(f"type {self.neuronType} neuron activated! creature {self.creature.ID}")
        if self.neuronType == "moveWest":
            self.creature.move("west")
        elif self.neuronType == "moveNorth":
            self.creature.move("north")
        elif self.neuronType == "moveEast":
            self.creature.move("east")
        elif self.neuronType == "moveSouth":
            self.creature.move("south")
        elif self.neuronType == "moveLeft":
            self.creature.move("left")
        elif self.neuronType == "moveForward":
            self.creature.move("forward")
        elif self.neuronType == "moveRight":
            self.creature.move("right")
        elif self.neuronType == "moveBackward":
            self.creature.move("backward")
        elif self.neuronType == "moveRandom":
            self.creature.move("random")
        elif self.neuronType == "turnLeft":
            self.creature.choose_move_direction("left")
        elif self.neuronType == "turnRight":
            self.creature.choose_move_direction("right")

    # Getter and setter for fromTo
    def get_from_to(self):
        return self.from_to

    def set_from_to(self, value):
        self.from_to = value

    # Getter and setter for neuronType
    def get_neuron_type(self):
        return self.neuronType

    def set_neuron_type(self, value):
        self.neuronType = value

    # Getter and setter for creature
    def get_creature(self):
        return self.creature

    def set_creature(self, value):
        self.creature = value

        # Getter and setter for temp_value

    def get_temp_value(self):
        return self.temp_value

    def set_temp_value(self, value):
        self.temp_value = value

    # Getter and setter for value
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
