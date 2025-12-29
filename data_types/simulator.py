import random
import networkx as nx
import matplotlib.pyplot as plt


import data_types.constants as constants
import data_types.config as config
from utils.ui_utils import draw_to_screen

from data_types.creature import Creature
from data_types.enums import Direction


class Simulator:

    def __init__(self):
        self.grid = [
            [0 for i in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)
        ]
        self.creatures: list[Creature] = []
        self.survivors = []
        self.empty_squares = [
            (i, j)
            for i in range(constants.GRID_SIZE)
            for j in range(constants.GRID_SIZE)
        ]
        self.previous_survivor_count = 0
        self.t = 0
        self.gen = 1

    def prepare_new_generation(self):
        self.erase()
        self.create()

        self.t = 0
        self.gen += 1

    def step(self):
        for creature in self.creatures:
            creature.get_brain().evaluate_connections()
            if creature.get_will_move():
                self.move(creature)
                creature.set_will_move(False)
            creature.age += 1

        if config.ENABLE_MUTATION:
            self.mutation()

        if config.ENABLE_RADIATION:
            self.radiation(self.t)

        self.t += 1

    def get_random_coord(self):
        rnd = random.randint(0, len(self.empty_squares) - 1)
        x, y = self.empty_squares[rnd]
        self.empty_squares.pop(rnd)
        return x, y

    def create(self):
        self.creatures = []
        ID = 0

        if len(self.survivors) != 0:
            for survivor in self.survivors:
                past_x, past_y = survivor.x, survivor.y
                survivor.x, survivor.y = self.get_random_coord()
                self.change_position(
                    past_x, past_y, survivor.x, survivor.y, survivor.color
                )
                self.creatures.append(survivor)

            for creature_index in range(constants.CREATURE_COUNT):
                if len(self.creatures) >= constants.CREATURE_COUNT:
                    break
                if len(self.survivors) < 2:
                    break

                x, y = self.get_random_coord()
                creature = Creature(x=x, y=y, ID=ID, create_new_brain=False)
                ID += 1

                creature_1 = self.survivors[random.randint(0, len(self.survivors) - 1)]
                creature_2 = self.survivors[random.randint(0, len(self.survivors) - 1)]
                connections = []

                if creature_index < len(self.survivors):
                    connections = self.survivors[creature_index].get_brain().connections
                else:
                    connections = (
                        creature_1.get_brain().get_random_half()
                        + creature_2.get_brain().get_random_half()
                    )

                creature.get_brain().add_existing_connections(connections)
                self.create_creature(creature)

        if len(self.creatures) < constants.CREATURE_COUNT:
            for _ in range(constants.CREATURE_COUNT - len(self.creatures)):
                x, y = self.get_random_coord()
                creature = Creature(x=x, y=y, ID=ID)
                self.create_creature(creature)
                ID += 1

        print(f"c count: {len(self.creatures)}")
        self.survivors = []

    def erase(self):
        self.survivors = []
        for creature in self.creatures.copy():
            self.delete_creature(creature)
            if self.surviving_rule(creature):
                self.survivors.append(creature)

        self.empty_squares = [
            (i, j)
            for i in range(constants.GRID_SIZE)
            for j in range(constants.GRID_SIZE)
        ]
        print(f"survivors: {len(self.survivors)}")
        self.previous_survivor_count = len(self.survivors)
        return self.survivors

    def surviving_rule(self, creature: Creature) -> bool:
        # Take creature, and return true if it survives, otherwise false.
        return 100 <= creature.x <= 150

    # For radiation
    def radiation(self, t):
        for creature in self.creatures.copy():
            i = random.randint(1, 1000)
            if i != 1:
                continue
            if self.radiation_rule(creature, t):
                self.delete_creature(creature)

    # Radiation
    def radiation_rule(self, creature, t) -> bool:
        # Take creature, and return true if it experiences radiation, otherwise false.
        return (creature.x < 125 and t < constants.MAX_MOVES / 2) or (
            creature.x > 125 and t > constants.MAX_MOVES / 2
        )

    # Mutation
    def mutation(self):
        for creature in self.creatures:
            mutation_rate = random.randint(1, 100_000)
            if mutation_rate == 1:
                creature.get_brain().mutate()

    def create_barrier(self):
        # TODO: No idea what LIMIT is, investigate
        for i in range(10, constants.GRID_SIZE - 10):
            self.grid[i][constants.LIMIT + 5] = 1
            draw_to_screen(i, constants.LIMIT + 5, constants.COLOR_BLACK)

    ############ Moving creature functions
    def move(self, creature: Creature):
        direction = creature.get_facing_direction()
        self.move_creature_in_direction(creature, direction)

    def move_creature_in_direction(self, creature: Creature, direction: Direction):
        dx, dy = direction.delta()
        new_x = creature.x + dx
        new_y = creature.y + dy

        if not self.check_bounds(new_x, new_y):
            return

        if not self.is_position_empty(new_x, new_y):
            return

        self.change_position(creature.x, creature.y, new_x, new_y, creature.color)

        creature.x = new_x
        creature.y = new_y

    ############

    ############ Move creature visually
    def change_position(self, x1, y1, x2, y2, color):
        self.grid[y1][x1] = 0
        self.grid[y2][x2] = 1

        draw_to_screen(x1, y1, constants.COLOR_BACKGROUND)
        draw_to_screen(x2, y2, color)

    ############

    ############ Creature create/delete
    def create_creature(self, creature):
        self.grid[creature.y][creature.x] = 1
        self.creatures.append(creature)

        if (creature.x, creature.y) in self.empty_squares:
            self.empty_squares.remove((creature.x, creature.y))

        draw_to_screen(creature.x, creature.y, creature.color)

    def delete_creature(self, creature):
        self.grid[creature.y][creature.x] = 0
        self.creatures.remove(creature)

        draw_to_screen(creature.x, creature.y, constants.COLOR_BACKGROUND)

    ############

    ############ Grid content functions
    def check_bounds(self, x, y):
        return 0 <= x < constants.GRID_SIZE and 0 <= y < constants.GRID_SIZE

    def is_position_empty(self, x, y):
        return self.grid[y][x] == 0

    ############

    def show_connection_graph(self, creature_index=0):
        # Create a graph
        G = nx.MultiDiGraph()

        edges = []
        for connection in self.creatures[creature_index].brain.connections:
            edges.append(
                (
                    connection.get_source().get_role().name,
                    connection.get_target().get_role().name,
                    "{:.2f}".format(connection.weight),
                )
            )

        G.add_weighted_edges_from(edges)

        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight="bold", arrows=True)
        # Draw the graph
        # nx.draw(G, with_labels=True, font_weight='bold', arrows=True)
        edge_labels = {}
        for u, v, key, data in G.edges(data=True, keys=True):
            edge_labels[(u, v, key)] = data["weight"]

        nx.draw_networkx_edge_labels(
            G, pos, edge_labels={(u, v): w for (u, v, _), w in edge_labels.items()}
        )

        plt.show()
