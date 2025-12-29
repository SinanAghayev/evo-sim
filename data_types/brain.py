import random, math, sys
import data_types.constants as constants

from data_types.neuron_role import NeuronRole
from data_types.neuron import Neuron
from data_types.connection import Connection


class Brain(object):

    connections: list[Connection]
    all_neurons: dict[NeuronRole, Neuron]

    def __init__(self, creature):
        self.creature = creature

        self.connections = []
        self.all_neurons = {}

    def generate_brain(self):
        self.connections = []
        for _ in range(constants.BRAIN_COMPLEXITY):
            self.create_new_connection()

    def create_new_connection(self):
        # Create or get source neuron
        neuron_role = random.choice(
            [n for n in NeuronRole if n.is_input or n.is_internal]
        )
        if neuron_role in self.all_neurons:
            source_neuron = self.all_neurons.get(neuron_role)
        else:
            source_neuron = Neuron(neuron_role, self.creature)
            self.all_neurons[neuron_role] = source_neuron

        # Create or get target neuron
        neuron_role = random.choice(
            [n for n in NeuronRole if n.is_output or n.is_internal]
        )
        if neuron_role in self.all_neurons:
            target_neuron = self.all_neurons.get(neuron_role)
        else:
            target_neuron = Neuron(neuron_role, self.creature)
            self.all_neurons[neuron_role] = target_neuron

        weight = (random.random() - 0.5) * 8

        # Create connection
        connection = Connection(source_neuron, target_neuron, weight, self.creature)

        self.connections.append(connection)

    # This function is for "reproduction" purposes.
    def add_existing_connections(self, connections: list[Connection]):
        self.connections = []

        for connection in connections:
            source_role = connection.get_source().get_role()
            if source_role not in self.all_neurons:
                self.all_neurons[source_role] = Neuron(source_role, self.creature)

            target_role = connection.get_target().get_role()
            if target_role not in self.all_neurons:
                self.all_neurons[target_role] = Neuron(target_role, self.creature)

            new_connection = Connection(
                self.all_neurons[source_role],
                self.all_neurons[target_role],
                connection.weight,
                self.creature,
            )
            self.connections.append(new_connection)

        if random.random() < 0.001:
            print("Mutating while creating brain")
            self.mutate()

    """
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
    """

    def evaluate_connections(self):
        # Evaluate input neurons
        for connection in self.connections:
            if not connection.get_source().get_role().is_input:
                continue

            target_previous_value = connection.get_target().get_temp_value()
            evaluated_value = (
                connection.get_source().get_value() * connection.get_weight()
            )

            connection.get_target().set_temp_value(
                target_previous_value + evaluated_value
            )

        # Evaluate internal neurons
        for connection in self.connections:
            if not connection.get_source().get_role().is_internal:
                continue

            internal_input = connection.source.get_temp_value()
            connection.get_source().set_temp_value(activation(internal_input))

            target_previous_value = connection.get_target().get_temp_value()
            evaluated_value = (
                connection.get_source().get_temp_value() * connection.get_weight()
            )

            connection.get_target().set_temp_value(
                target_previous_value + evaluated_value
            )

        # Reset temp_values of all neurons for future use.
        for neuron in self.all_neurons.values():
            neuron.set_value(activation(neuron.get_temp_value()))
            neuron.set_temp_value(0)

        self.activate_neurons()

    def activate_neurons(self):
        max_value = -1
        max_neuron = None
        for neuron in self.all_neurons.values():
            if neuron.get_role().is_output and neuron.get_value() > max_value:
                max_value = neuron.get_value()
                max_neuron = neuron

        if max_value < 0:
            return

        max_neuron.activate()

    def mutate(self):
        if random.random() < 0.7:
            self.mutate_partially()
            return

        print("Mutating whole connection")
        rnd = random.randint(0, len(self.connections) - 1)
        self.connections.remove(self.connections[rnd])
        self.create_new_connection()

    def mutate_partially(self):
        connection_count = len(self.connections)
        if connection_count == 0:
            return
        elif connection_count == 1:
            rnd = 0
        else:
            rnd = random.randint(0, len(self.connections) - 1)
        self.connections[rnd].mutate()

    def get_random_half(self):
        n = len(self.connections)
        indices = random.sample(range(0, n), n // 2)
        return [self.connections[i] for i in indices]

    def __str__(self):
        temp = ""
        for c in self.connections:
            temp += f"{c.get_source().get_role()}, {c.get_weight()}, {c.get_target().get_role()}\n"
        return temp


def activation(x):
    return math.tanh(x)
    return max(0, x)
    return 1 / (1 + math.exp(-x))
