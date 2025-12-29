import sys, pygame

import data_types.constants as constants
import data_types.config as config
from data_types.simulator import Simulator
from data_types.neuron import Neuron
from data_types.connection import Connection

from utils.ui_utils import draw_to_screen, screen
from utils.graph import plot_graph


font = pygame.font.Font(pygame.font.get_default_font(), 24)

# Screen
screen.fill(constants.COLOR_BLACK)

# TODO: Lots of magic numbers here, fix them
px = pygame.PixelArray(screen)
px[2 : constants.SCREEN_WIDTH + 2, 2 : constants.SCREEN_HEIGHT + 2] = (
    constants.COLOR_WHITE
)
px[
    constants.HORIZONTAL_START - 2 : constants.HORIZONTAL_END + 2,
    constants.VERTICAL_START - 2 : constants.VERTICAL_END + 2,
] = constants.COLOR_BLACK

px[
    constants.HORIZONTAL_START : constants.HORIZONTAL_END,
    constants.VERTICAL_START : constants.VERTICAL_END,
] = constants.COLOR_WHITE

px[
    constants.HORIZONTAL_END + 2 : constants.SCREEN_HEIGHT,
    (constants.LIMIT) * constants.CREATURE_SIZE + constants.HORIZONTAL_START - 2,
] = constants.COLOR_GRAY
del px

# Initialize simulator
simulator = Simulator()
# Initialize creatures
simulator.create()

mouse_position = (0, 0)
drawing = False

pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button down.
                last = (event.pos[0] - event.rel[0], event.pos[1] - event.rel[1])
                # pygame.draw.line(screen, black, last, event.pos, c_size)
                x_pos = (
                    last[0] - constants.HORIZONTAL_START
                ) // constants.CREATURE_SIZE
                y_pos = (last[1] - constants.VERTICAL_START) // constants.CREATURE_SIZE
                if 0 < x_pos < constants.GRID_SIZE and 0 < y_pos < constants.GRID_SIZE:
                    draw_to_screen(x_pos, y_pos, constants.COLOR_BLACK)
                    simulator[y_pos][x_pos] = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                config.SHOW_CONNECTION_GRAPHS = not config.SHOW_CONNECTION_GRAPHS
                print(f"{config.SHOW_CONNECTION_GRAPHS=}")
            if event.key == pygame.K_m:
                config.ENABLE_MUTATION = not config.ENABLE_MUTATION
                print(f"{config.ENABLE_MUTATION=}")
            if event.key == pygame.K_s:
                config.SHOW_VISUALS = not config.SHOW_VISUALS
                print(f"{config.SHOW_VISUALS=}")
            if event.key == pygame.K_l:
                config.SLOW_MODE = not config.SLOW_MODE
                print(f"{config.SLOW_MODE=}")

    # Prepare the text lines
    text_lines = [
        f"Gen: {simulator.gen}",
        f"Population: {len(simulator.creatures)}",
        f"Survivors: {simulator.previous_survivor_count}",
        f"T (days lapsed): {simulator.t}",
    ]
    # Start drawing the text at position (800, 50)
    text_position = (800, 50)
    pygame.draw.rect(
        screen, constants.COLOR_WHITE, (800, 50, 240, len(text_lines) * 40)
    )
    # Draw each line of text
    for line in text_lines:
        text_surface = font.render(line, True, constants.COLOR_BLACK)
        screen.blit(text_surface, text_position)

        # Move the position down for the next line
        text_position = (800, text_position[1] + 40)  # Adjust the 40 for line spacing

    if not simulator.t % 100:
        print(f"move {simulator.t}")

    # 300 movements every gen
    if simulator.t >= constants.MAX_MOVES:
        if config.SHOW_CONNECTION_GRAPHS:
            """
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
            )"""
            simulator.show_connection_graph()

        simulator.prepare_new_generation()

    # Movement of creatures depending their "DNA"
    simulator.step()

    if config.SLOW_MODE:
        pygame.time.wait(100)

    if config.SHOW_VISUALS:
        pygame.display.flip()
