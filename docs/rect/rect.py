import pygame
from pygame.locals import *
from random import randint

width = 500
height = 200

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

dir = {K_LEFT: (-5, 0), K_RIGHT: (5, 0), K_UP: (0, -5), K_DOWN: (0, 5)}
rect = Rect(50, 60, 200, 80)

def draw_text(text, pos):
    img = font.render(text, True, BLACK)
    screen.blit(img, pos)

def random_point():
    x = randint(0, width)
    y = randint(0, height)
    return (x, y)

def random_points(n):
    points = []
    for i in range(n):
        p = random_point()
        points.append(p)
    return points

def random_rects(n):
    rects = []
    for i in range(n):
        r = Rect(random_point(), (20, 20))
        rects.append(r)
    return rects

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
running = True