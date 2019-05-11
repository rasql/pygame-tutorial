"""Create a checkerboard pattern."""

import pygame
from pygame.locals import *
from pygamelib import *
import numpy as np

class BoardDemo(Game):
    """Draw cells in random colors."""
    def __init__(self):
        super(BoardDemo, self).__init__()
        Text('Checker', size=48)
        Text('Create a pattern', size=24)

        n, m = 10, 16
        b = Board(n, m, pos=(200, 10))
        b.color_list = [None, RED]
        b.colors = np.fromfunction(lambda x, y: (x + y) % 2, (n, m), dtype=int)
        b.T = b.colors

if __name__ == '__main__':
    BoardDemo().run()