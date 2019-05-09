import pygame
import numpy as np
from pygame.locals import *
from pygamelib import *

class BoardDemo(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(BoardDemo, self).__init__()
        Text('Board')
        self.board = Board(10, 16, pos=(100, 10))

    def on_event(self, event): 
        """React to mouseclicks and keydown events."""
        d = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1), }
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.board.T = np.random.randint(0, 3, (self.board.n, self.board.m))
            if event.key in d:
                self.board.j += d[event.key][0]
                self.board.i += d[event.key][1]
                self.board.j = self.board.j % self.board.m
                self.board.i = self.board.i % self.board.n   

if __name__ == '__main__':
    BoardDemo().run()