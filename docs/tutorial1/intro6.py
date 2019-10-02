import pygame
from pygame.locals import *

width = 640
height = 320
speed = [2, 2]
GREEN = (150, 255, 150)
running = True

pygame.init()
screen = pygame.display.set_mode((width, height))
ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

while running:
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(GREEN)
    screen.blit(ball, ballrect)
    pygame.display.flip()

pygame.quit()