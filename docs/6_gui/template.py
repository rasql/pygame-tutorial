"""Template for making games."""

import pygame
from pygame.locals import *
from pygamelib import *

class AppDemo(App):
    """Make a subclass of the App class."""
    def __init__(self):
        super(AppDemo, self).__init__()
        Text('AppDemo Template', size=48, bgcolor=CYAN)
        Text('Start your app with this template', size=24)
        
        Rectangle(size=(100,30))
        Rectangle(d=3)
        Ellipse()

if __name__ == '__main__':
    AppDemo().run()