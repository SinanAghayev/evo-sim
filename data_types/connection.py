import random
from data_types.neuron import Neuron
from data_types.neuron_role import NeuronRole


class Connection(object):

    def __init__(self, source: Neuron, target: Neuron, weight: float, creature):
        self.source = source
        self.target = target
        self.weight = weight
        self.creature = creature

    def mutate(self):
        rnd = random.randint(0, 10)
        if rnd == 0:
            print("Mutating source neuron")
            self.source.set_role(random.choice(list(NeuronRole)))
        elif rnd == 1:
            print("Mutating target neuron")
            self.target.set_role(random.choice(list(NeuronRole)))
        elif rnd == 2:
            print("Mutating weight")
            self.weight = (random.random() - 0.5) * 8
        else:
            print("Mutating weight slightly")
            self.weight += (random.random() - 0.5) / 5
        self.weight = max(-4, min(4, self.weight))

    def __str__(self):
        return f"{self.source.role} -> {self.weight} -> {self.target.role}"

    # Getter and setter for from_n
    def get_source(self):
        return self.source

    def set_source(self, value):
        self.source = value

    # Getter and setter for to_n
    def get_target(self):
        return self.target

    def set_target(self, value):
        self.target = value

    # Getter and setter for weight
    def get_weight(self):
        return self.weight

    def set_weight(self, value):
        self.weight = value

    # Getter and setter for creature
    def get_creature(self):
        return self.creature

    def set_creature(self, value):
        self.creature = value
