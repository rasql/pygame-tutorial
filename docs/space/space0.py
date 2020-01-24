import pygame
import sys
from pygame.locals import *

class Player:
    """The player can move."""
    
    def __init__(self):
        print('create player')
        
    def do_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        pass
    
    
class Enemy:
    """The player must avoid the enemies."""
    
    def __init__(self):
        print('create enemy')
        
    def update(self):
        pass
    
    def draw(self):
        pass
    
class App:
    width = 600
    size = 400
    caption = 'Space Game'
    
    def __init__(self):
        print('initalize app')
        pygame.init()
        pygame.display.set_mode((App.width, App.size))
        pygame.display.set_caption(App.caption)

        self.screen = pygame.display.get_surface()
        self.player = Player()
        self.enemy = Enemy()
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
        self.enemy.update()
            
    def draw(self):
        self.screen.fill(Color('black'))
        self.player.draw()
        self.enemy.draw()
        pygame.display.update()
         
        
if __name__ == '__main__':
    app = App()
    app.run()