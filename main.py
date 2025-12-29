import sys, pygame

import data_types.constants as constants
from data_types.simulation import Simulation
from data_types.neuron import Neuron
from data_types.connection import Connection

from utils.ui_utils import draw_to_screen

import networkx as nx
import matplotlib.pyplot as plt

from utils.graph import plot_graph


def show_connection():
    # Create a graph
    G = nx.MultiDiGraph()

    e = []
    for c in creatures[0].brain.connections:
        e.append((c.from_n.neuronType, c.to_n.neuronType, "{:.2f}".format(c.weight)))

    G.add_weighted_edges_from(e)

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


font = pygame.font.Font(pygame.font.get_default_font(), 24)

# Screen
screen.fill(black)

px = pygame.PixelArray(screen)
px[2 : width + 2, 2 : height + 2] = white
px[h_start - 2 : h_end + 2, v_start - 2 : v_end + 2] = black
px[h_start:h_end, v_start:v_end] = white
px[h_end + 2 : height, (limit) * c_size + h_start - 2] = (127, 127, 127)
del px

# Survivors from previous generation
survivors = []

# Initialize creatures
create()

mouse_position = (0, 0)
drawing = False

t, gen = 0, 1
past_survivors = 0
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button down.
                last = (event.pos[0] - event.rel[0], event.pos[1] - event.rel[1])
                # pygame.draw.line(screen, black, last, event.pos, c_size)
                x_pos = (last[0] - h_start) // c_size
                y_pos = (last[1] - v_start) // c_size
                if 0 < x_pos < pg_size and 0 < y_pos < pg_size:
                    draw_to_screen(x_pos, y_pos, black)
                    playground[x_pos][y_pos] = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                get_connection = not get_connection
                print(f"{get_connection=}")
            if event.key == pygame.K_m:
                mutate = not mutate
                print(f"{mutate=}")
            if event.key == pygame.K_s:
                show = not show
                print(f"{show=}")
            if event.key == pygame.K_l:
                slow = not slow
                print(f"{slow=}")

    # Prepare the text lines
    text_lines = [
        f"Gen: {gen}",
        f"Population: {len(creatures)}",
        f"Survivors: {past_survivors}",
        f"T (days lapsed): {t}",
    ]
    # Start drawing the text at position (800, 50)
    text_position = (800, 50)
    pygame.draw.rect(screen, white, (800, 50, 240, len(text_lines) * 40))
    # Draw each line of text
    for line in text_lines:
        text_surface = font.render(line, True, black)
        screen.blit(text_surface, text_position)

        # Move the position down for the next line
        text_position = (800, text_position[1] + 40)  # Adjust the 40 for line spacing

    if not t % 100:
        print(f"move {t}")

    # 300 movements every gen
    if t == MAX_MOVES:
        if get_connection:
            print(f"{len(Neuron.all_neuron_counts)=}")
            print(f"{Neuron.all_neuron_counts=}")

            plot_graph(
                Neuron.all_neuron_counts.keys(),
                Neuron.all_neuron_counts.values(),
                "title",
                "x_label",
                "y_label",
            )
            plot_graph(
                Neuron.activated_neurons.keys(),
                Neuron.activated_neurons.values(),
                "activated",
                "x_label",
                "y_label",
            )
            show_connection()

        Neuron.all_neuron_counts = {i: 0 for i in Neuron.all_neuron_types}
        Neuron.activated_neurons = {i: 0 for i in Neuron.to_neurons}

        survivors = erase()
        past_survivors = len(survivors)
        create()
        survivors = []
        t = 0
        gen += 1

    # Movement of creatures depending their "DNA"
    for c in creatures:
        c.get_brain().evaluateConnections()
        if c.get_will_move():
            move(c)
            c.set_will_move(False)
        c.age += 1

    """
    ####### For debugging playground
    for i in range(pg_size):
        for j in range(pg_size):
            if playground[i][j]:
                draw_to_screen(pg_size + j + 1, i, black)
            else:
                draw_to_screen(pg_size + j + 1, i, white)
    """

    if mutate:
        mutation()
    # erase_one(t)

    t += 1
    if slow:
        pygame.time.wait(100)

    if show:
        pygame.display.flip()
