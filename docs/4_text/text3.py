"""Display unicode (Japanese and pictograms)."""
import pygame

from pygame.locals import *
import time
 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((640, 240))

s = 'Unicodeカタ日本♚♛'
font0 = pygame.font.Font(None, 48)
font1 = pygame.font.SysFont('arialunicode.ttf', 64)

img0 = font0.render(s, True, RED)
img1 = font1.render(s, True, RED)

running = True
background = GRAY

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.fill(background)
    screen.blit(img0, (20, 20))
    screen.blit(img1, (20, 50))
    pygame.display.update()

pygame.quit()