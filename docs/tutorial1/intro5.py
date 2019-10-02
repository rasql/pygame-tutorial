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

key_dict = {K_k:BLACK, K_r:RED, K_g:GREEN, K_b:BLUE, 
    K_y:YELLOW, K_c:CYAN, K_m:MAGENTA, K_w:WHITE}

print(key_dict)

pygame.init()
screen = pygame.display.set_mode((640, 240))

running = True
background = GRAY
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in key_dict:
                background = key_dict[event.key]
                
                caption = 'background color = ' + str(background)
                pygame.display.set_caption(caption)

    screen.fill(background)
    pygame.display.update()

pygame.quit()