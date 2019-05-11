"""Draw a 4x4 board."""

import pygame
import numpy as np
from pygame.locals import *
from pygamelib import *

class BoardDemo(Game):
    """Draw a playing board."""
    def __init__(self):
        super(BoardDemo, self).__init__()
        Text('Board')
        Board(pos=(200, 20))

if __name__ == '__main__':
    BoardDemo().run()