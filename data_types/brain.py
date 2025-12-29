import random, math, sys
from data_types.neuron import Neuron
from data_types.connection import Connection
from data_types.constants import *


class Brain(object):

    def __init__(self, creature):
        self.creature = creature

        self.connections = []
        self.allNeurons = {}

    def generateBrain(self):
        self.connections = []
        for _ in range(brainComplexity):
            self.createNewConnection()

    def createNewConnection(self):
        nType = random.sample(Neuron.from_neurons, 1)[0]
        if nType in self.allNeurons:
            fromNeuron = self.allNeurons.get(nType)
        else:
            fromNeuron = Neuron(False, nType, self.creature)

        nType = random.sample(Neuron.to_neurons, 1)[0]
        if nType in self.allNeurons:
            toNeuron = self.allNeurons.get(nType)
        else:
            toNeuron = Neuron(True, nType, self.creature)

        connection = Connection(
            fromNeuron, toNeuron, (random.random() - 0.5) * 8, self.creature
        )

        self.connections.append(connection)

    # This function is for "reproduction" purposes.
    def addExistingConnections(self, connections):
        self.connections = []

        for c in connections:
            fromType = c.get_from_n().get_neuron_type()
            if fromType not in self.allNeurons:
                self.allNeurons[fromType] = Neuron(False, fromType, self.creature)

            toType = c.get_to_n().get_neuron_type()
            if toType not in self.allNeurons:
                self.allNeurons[toType] = Neuron(True, toType, self.creature)

            connection = Connection(
                self.allNeurons[fromType],
                self.allNeurons[toType],
                c.weight,
                self.creature,
            )
            self.connections.append(connection)
        if random.random() < 0.001:
            print("Mutating while creating brain")
            self.mutate()

    def addExistingConnectionsFromFile(self, connections):
        # TODO - Not corrected, need to have a look if this will be used
        self.connections = []

        for c in connections:
            fromType = c.get_from_n()
            if not self.allNeurons.__contains__(fromType):
                self.allNeurons[fromType] = Neuron(False, fromType, self.creature)

            toType = c.get_to_n()
            if not self.allNeurons.__contains__(toType):
                self.allNeurons[toType] = Neuron(True, toType, self.creature)

            connection = Connection(
                self.allNeurons[fromType],
                self.allNeurons[toType],
                c.weight,
                self.creature,
            )
            self.connections.append(connection)

    def evaluateConnections(self):
        for c in self.connections:
            if c.from_n.neuronType in Neuron.input_neurons:
                c.get_to_n().set_temp_value(
                    c.get_to_n().get_temp_value()
                    + c.get_from_n().getValue() * c.get_weight()
                )

        for c in self.connections:
            if c.from_n.neuronType in Neuron.internal_neurons:
                c.from_n.set_temp_value(activation(c.from_n.get_temp_value()))
                c.get_to_n().set_temp_value(
                    c.get_to_n().get_temp_value()
                    + c.get_from_n().get_temp_value() * c.get_weight()
                )

        for neuron in Neuron.all_neuron_types:
            if neuron not in self.allNeurons:
                continue
            self.allNeurons[neuron].set_value(
                activation(self.allNeurons[neuron].get_temp_value())
            )
            self.allNeurons[neuron].set_temp_value(0)

        self.activateNeurons()

    def activateNeurons(self):
        curr_max = -1
        max_neuron = None
        for n in self.allNeurons.values():
            if n.neuronType in Neuron.output_neurons and n.value > curr_max:
                curr_max = n.value
                max_neuron = n

        if curr_max < 0:
            return

        max_neuron.activate()

    def mutate(self):
        if random.random() < 0.7:
            self.mutate_partially()
            return
        print("Mutating whole connection")
        rnd = random.randint(0, len(self.connections) - 1)
        self.connections.remove(self.connections[rnd])
        self.createNewConnection()

    def mutate_partially(self):
        rnd = random.randint(0, len(self.connections) - 1)
        self.connections[rnd].mutate()

    def get_random_half(self):
        n = len(self.connections)
        indices = random.sample(range(0, n), n // 2)
        return [self.connections[i] for i in indices]

    def __str__(self):
        temp = ""
        for c in self.connections:
            temp += f"{c.get_from_n().get_neuron_type()}, {c.get_weight()}, {c.get_to_n().get_neuron_type()}\n"
        return temp


def activation(x):
    # Define your sigmoid function implementation here
    # For example, you can use the math module:
    return math.tanh(x)
    return max(0, x)
    return 1 / (1 + math.exp(-x))
