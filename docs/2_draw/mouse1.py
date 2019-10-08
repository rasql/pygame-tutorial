"""Print mouse event to the console."""

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((640, 240))

running = True
background = GRAY
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            print(event)
        elif event.type == MOUSEBUTTONUP:
            print(event)
        elif event.type == MOUSEMOTION:
            print(event)

    screen.fill(background)
    pygame.display.update()

pygame.quit()