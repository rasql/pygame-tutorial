"""Place two 4x4 boards on the screen."""

import pygame
from pygame.locals import *
from pygamelib import *

class BoardDemo2(Game):
    """Draw two 4x4 boards and select cells with mouse click."""
    def __init__(self):
        super(BoardDemo2, self).__init__()
        
        Text('Board', size=48)
        Text('click to select', size=24)
        Text('cmd+click multiple')
        Text('arrow to move')
        Board(pos=(200, 20))
        Board(pos=(420, 20)).wrap = True

if __name__ == '__main__':
    BoardDemo2().run()