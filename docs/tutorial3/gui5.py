"""Selecting and editing objects."""

import pygame
from pygame.locals import *
from pygamelib import *

class GuiDemo5(Game):
    """Make a subclass of the Game class."""
    def __init__(self):
        super(GuiDemo5, self).__init__()
        Text('Selecting objects')
        Text('Click to select', size=24)
        Text('Ctrl-drag to move')
        Text('Type to edit text')
        Text('Cmd-V to animate')

        self.shortcuts[(K_v, KMOD_LMETA)] = 'self.current_obj.v=[1, 1]'
        
        Rectangle(color=GREEN)
        Ellipse(size=(200, 50), color=YELLOW)
        Text('ABC')

if __name__ == '__main__':
    GuiDemo5().run()