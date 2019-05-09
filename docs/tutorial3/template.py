"""Template for making games."""

import pygame
from pygame.locals import *
from pygamelib import *

class GameDemo(Game):
    """Make a subclass of the Game class."""
    def __init__(self):
        super(GameDemo, self).__init__()
        Text('GameDemo Template', size=48, bgcolor=CYAN)
        Text('Start your game with this template', size=24)
        
        Rectangle(size=(100,30))
        Rectangle(d=3)
        Ellipse()

if __name__ == '__main__':
    GameDemo().run()