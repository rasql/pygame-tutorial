"""
This is a game with a space theme.
It uses object-oriented programming.

Creative Commons Attribution license
Icons: https://www.flaticon.com/authors/freepik
Music: https://patrickdearteaga.com/arcade-music/
"""

import pygame
import sys
import random
import math
from pygame.locals import *

class Player:
    """The player can move."""
    
    def __init__(self):
        print('create player')
                
        self.img0 = pygame.image.load('images/spaceship.png')
        self.img = self.img0.copy()
        self.rect = self.img.get_rect()
        
        self.pos = 100, 100
        self.speed = 0
        self.angle = 0
        self.v = 0, 0
        self.rect.center = self.pos

    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.speed += 1
                
            elif event.key == K_DOWN:
                self.speed += -1
                
            elif event.key == K_LEFT:
                self.angle += math.pi/20
                
            elif event.key == K_RIGHT:
                self.angle += - math.pi/20
                
            elif event.key == K_SPACE:
                self.speed = 0
            
            center = self.rect.center
            self.img = pygame.transform.rotate(self.img0, math.degrees(self.angle))
            self.rect = self.img.get_rect()
            self.rect.center = center
            
            self.v = [-self.speed * math.sin(self.angle), -self.speed * math.cos(self.angle)]
    
    def update(self):
        self.rect.move_ip(self.v)
        self.rect.centerx = self.rect.centerx % App.size[0]
        self.rect.centery = self.rect.centery % App.size[1]
        
    
    def draw(self):
        App.screen.blit(self.img, self.rect)    
    
class Enemy:
    """The player must avoid the enemies."""
    
    def __init__(self, img):
        self.img = img
        self.rect = img.get_rect()
        x = random.randint(0, App.size[0])
        y = random.randint(0, App.size[1])
        self.rect.center = x, y
        self.v = (random.randint(-1, 1), random.randint(-1, 1))
            
    def update(self):
        self.rect.move_ip(self.v)
        self.rect.centerx = self.rect.centerx % (App.size[0]+self.rect.width)
        self.rect.centery = self.rect.centery % (App.size[1]+self.rect.height)
        
    
    def draw(self):
        App.screen.blit(self.img, self.rect)

class Text:
    """Create a text object."""
    
    def __init__(self, text, pos):
        self.font = pygame.font.Font(None, 36)
        self.rect = Rect(pos, (0, 0))
        self.set(text)
        
    def set(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, Color('white'))
        self.rect.size = self.img.get_size()
        
    def draw(self):
        App.screen.blit(self.img, self.rect)
        
        

class App:
    size = None
    screen = None  # this allows to use the class variable App.screen from everywhere
    caption = 'Space Game'
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(App.caption)
        self.img = pygame.image.load('images/space.jpg')
        App.size = self.img.get_size()
        App.screen = pygame.display.set_mode(App.size)
        
        self.snd = pygame.mixer.Sound('sounds/Intergalactic Odyssey.ogg')
        self.snd.play(-1)

        self.player = Player()
        self.score = 0
        self.text = Text(f'Score: {self.score}', (20, 20))
  
        self.enemies = []
        img = pygame.image.load('images/ufo.png')
        for i in range(10):
            self.enemies.append(Enemy(img))
  
        self.running = True
        
    def run(self):
        print('run app')
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)

            self.update()
            self.draw()
            
        pygame.quit()
        sys.exit()
            
            
    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
            
        self.player.do_event(event)
            
    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            
    def draw(self):
        App.screen.blit(self.img, (0, 0))

        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()
        
        self.score += 1
        self.text.set(f'Score: {self.score}')
        self.text.draw()

        pygame.display.update()
         
if __name__ == '__main__':
    app = App()
    app.run()