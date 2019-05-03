"""The game of PONG."""

import pygame
from pygame.locals import *
from pygamelib import *

class PongDemo(Game):
    """Play the game of Pong."""
    def __init__(self):
        super(PongDemo, self).__init__()
        Text('Pong', size=48)

        self.pad = Rectangle(size=(20, 100))
        self.ball = Rectangle(size=(20, 20), color=RED, v=(2, 2))

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.pad.v[1] = -1
            if event.key == K_DOWN:
                self.pad.v[1] = 1
                
if __name__ == '__main__':
    PongDemo().run()