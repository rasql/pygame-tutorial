# https://opensource.com/article/17/12/game-python-add-a-player

import pygame
import sys
import os


class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        # img = pygame.image.load(os.path.join('images', 'player1.png')).convert()
        img = pygame.image.load('images/player1.png')
        
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()


w, h = 640, 480

fps   = 40  # frame rate
ani   = 4   # animation cycles

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((w, h))
backdrop = pygame.image.load(os.path.join('images', 'fall.jpg')).convert()
backdrop = pygame.image.load('images/fall.jpg')
backdrop.convert()

backdropbox = screen.get_rect()


player = Player()   # spawn player
player.rect.x = 0   # go to x
player.rect.y = 0   # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
running = True

'''
Main loop
'''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False

    screen.fill((255, 0, 0))
    screen.blit(backdrop, backdropbox)
    player_list.draw(screen)  # draw player
    pygame.display.flip()

pygame.quit()
