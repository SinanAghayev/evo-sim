import pygame
import data_types.constants as constants


pygame.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE)


def draw_to_screen(x, y, color):
    px = pygame.PixelArray(screen)  # Create px only when needed
    tempx = constants.HORIZONTAL_START + x * constants.CREATURE_SIZE
    tempy = constants.VERTICAL_START + y * constants.CREATURE_SIZE
    px[
        tempx : tempx + constants.CREATURE_SIZE, tempy : tempy + constants.CREATURE_SIZE
    ] = color
    del px  # Unlock screen after modifying pixels
