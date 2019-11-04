"""Create a 4x4 puzzle."""

import pygame
import numpy as np
from pygame.locals import *
from pygamelib import *

class Puzzle(Board):
    """Create a 4x4 number puzzle."""
    def __init__(self, n, m, **kwargs):
        super(Puzzle, self).__init__(n, m, **kwargs)
        a = np.arange(n * m)
        a.resize(n, m)
        self.T = a

    def on_key(self, event):
        d = {K_LEFT:0, K_RIGHT:0, K_UP:0, K_DOWN:0}
        if event.key in d:
            i, j = self.find(0)
            if event.key == K_LEFT:
                pass
            print(index)

    def find(self, n):
        """Return first index of n."""
        for i in range(self.n):
            for j in range(self.m):
                if self.T[i, j] == n:
                    return (i, j)

class BoardDemo(App):
    """Draw a 4x4 number puzzle."""
    def __init__(self):
        super(BoardDemo, self).__init__()
        Text('Number puzzle')

        Puzzle(4, 5, pos=(300, 20))

if __name__ == '__main__':
    BoardDemo().run()