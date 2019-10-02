import pygame

pygame.init()
screen = pygame.display.set_mode((640, 240))

while True:
    for event in pygame.event.get():
        print(event)