import pygame
import random
from pygame.locals import *

class Player:
    """The player can move."""
    
    def __init__(self):
        print('create player')
        self.x = 100
        self.y = 100
        self.w = 50
        self.h = 50
        self.dx = 0
        self.dy = 0
        self.color = Color('red')
        
    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.dx += 1
            elif event.key == K_LEFT:
                self.dx -= 1
            elif event.key == K_DOWN:
                self.dy += 1
            elif event.key == K_UP:
                self.dy -= 1
            elif event.key == K_SPACE:
                self.dx = 0
                self.dy = 0
    
    def update(self):
        self.x += self.dx
        self.x = self.x % App.width
        self.y += self.dy
        self.y = self.y % App.height
    
    def draw(self):
        pygame.draw.rect(App.screen, self.color, Rect(self.x, self.y, self.w, self.h))
    
    
class Enemy:
    """The player must avoid the enemies."""
    
    def __init__(self):
        print('create enemy')
        self.x = random.randint(0, App.width)
        self.y = random.randint(0, App.height)
        self.w = 30
        self.h = 30
        self.color = Color('blue')
        
    def update(self):
        pass
    
    def draw(self):
        pygame.draw.rect(App.screen, self.color, Rect(self.x, self.y, self.w, self.h))
    
class App:
    width = 600
    height = 400
    caption = 'Space Game'
    screen = None  # this allows to use the class variable App.screen from everywhere
    
    def __init__(self):
        print('initalize app')
        pygame.init()
        App.screen = pygame.display.set_mode((App.width, App.height))
        pygame.display.set_caption(App.caption)

        self.player = Player()
  
        self.enemies = []
        for i in range(10):
            self.enemies.append(Enemy())
  
        self.running = True
        
    def run(self):
        print('run app')
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)

            self.update()
            self.draw()
            
        pygame.quit()
            
    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
            
        self.player.do_event(event)
            
    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            
    def draw(self):
        App.screen.fill(Color('black'))

        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()

        pygame.display.update()
        
        
if __name__ == '__main__':
    app = App()
    app.run()