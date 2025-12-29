from data_types.neuron_role import NeuronRole


class Neuron(object):
    # Types:
    # 0=age, 1=x_coord, 2=y_coord,
    # 3=dist_to_west, 4=dist_to_east, 5=dist_to_north, 6=dist_to_south
    # 7,8,9= internal neuron
    # 10=moveWest, 11=moveNorth, 12=moveEast, 13=moveSouth
    # 14=moveLeft, 15=moveForward, 16=moveRight, 17=moveBackward
    # 18=moveRandom, 19=nothing
    # 20=turnLeft, 21=turnRight
    # (not active) 22=kill

    def __init__(self, role: NeuronRole, creature):
        self.role = role
        self.creature = creature

        self.temp_value = 0
        self.value = 0

    def get_value(self) -> float:
        self.value = self.role.read_value(self.creature)
        return self.value

    def activate(self):
        self.role.activate(self.creature)

    # Getter and setter for role
    def get_role(self) -> NeuronRole:
        return self.role

    def set_role(self, value: NeuronRole):
        self.role = value

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
