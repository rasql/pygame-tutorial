"""Place a polygone line with the clicks of the mouse."""

import pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((640, 240))

drawing = False
points = []
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if len(points) > 0:
                    points.pop()

        elif event.type == MOUSEBUTTONDOWN:
            points.append(event.pos)
            drawing = True

        elif event.type == MOUSEBUTTONUP:
            drawing = False

        elif event.type == MOUSEMOTION and drawing:
            points[-1] = event.pos
    
    screen.fill(GRAY)
    if len(points)>1:
        rect = pygame.draw.lines(screen, RED, True, points, 3)
        pygame.draw.rect(screen, GREEN, rect, 1)
    pygame.display.update()

pygame.quit()