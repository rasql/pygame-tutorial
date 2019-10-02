import pygame
from pygame.locals import *

RED = (255, 0, 0)
GRAY = (127, 127, 127)

pygame.init()
screen = pygame.display.set_mode((640, 240))

start = (0, 0)
end = (0, 0)
drawing = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            start = event.pos
            end = event.pos
            drawing = True
            
        elif event.type == MOUSEBUTTONUP:
            end = event.pos
            drawing = False

        elif event.type == MOUSEMOTION:
            if drawing:
                end = event.pos

    screen.fill(GRAY)
    size = end[0] - start[0], end[1] - start[1]
    pygame.draw.rect(screen, RED, (start, size), 2)
    pygame.display.update()

pygame.quit()