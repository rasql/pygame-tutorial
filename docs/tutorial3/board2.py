"""Place two 4x4 boards on the screen. Mouse-click can select and activate a cell.
Arrow keys can move the active cell. The most recently clicked Board is the active one."""

import pygame
import numpy as np
from pygame.locals import *
from pygamelib import *

class BoardDemo2(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(BoardDemo2, self).__init__()
        
        Text('Board', size=48)
        Text('click to select', size=24)
        Text('cmd+click multiple')
        Text('arrow to move')
        Board(4, 4, pos=(200, 10),dx=50, dy=50)
        Board(8, 4, pos=(500, 10)).wrap = True

if __name__ == '__main__':
    BoardDemo2().run()