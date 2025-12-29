import random
from data_types.neuron import Neuron


class Connection(object):

    def __init__(self, from_n, to_n, weight, creature):
        self.from_n = from_n
        self.to_n = to_n
        self.weight = weight
        self.creature = creature

        Neuron.all_neuron_counts[from_n.get_neuron_type()] += 1
        Neuron.all_neuron_counts[to_n.get_neuron_type()] += 1

    def mutate(self):
        rnd = random.randint(0, 10)
        if rnd == 0:
            print("Mutating from_n")
            self.from_n.set_neuron_type(random.sample(Neuron.all_neuron_types, 1)[0])
        elif rnd == 1:
            print("Mutating to_n")
            self.to_n.set_neuron_type(random.sample(Neuron.all_neuron_types, 1)[0])
        elif rnd == 2:
            print("Mutating weight")
            self.weight = (random.random() - 0.5) * 8
        else:
            print("Mutating weight slightly")
            self.weight += (random.random() - 0.5) / 5
        self.weight = max(-4, min(4, self.weight))

    def __str__(self):
        return f"{self.from_n.neuronType} -> {self.weight} -> {self.to_n.neuronType}"

    # Getter and setter for from_n
    def get_from_n(self):
        return self.from_n

    def set_from_n(self, value):
        self.from_n = value

    # Getter and setter for to_n
    def get_to_n(self):
        return self.to_n

    def set_to_n(self, value):
        self.to_n = value

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
