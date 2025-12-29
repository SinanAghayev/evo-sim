import pygame
from data_types.constants import *


pygame.init()
screen = pygame.display.set_mode(size)


def draw_to_screen(x, y, color):
    px = pygame.PixelArray(screen)  # Create px only when needed
    tempx = h_start + x * c_size
    tempy = v_start + y * c_size
    px[tempx : tempx + c_size, tempy : tempy + c_size] = color
    del px  # Unlock screen after modifying pixels
