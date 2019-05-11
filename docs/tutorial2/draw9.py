"""Draw circles of different size and color."""

import pygame
from random import randint
from pygamelib import *

colors = (RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN, GRAY)

class MovingShapeDemo(Game):
    """Draw ellipses in different sizes and colors."""
    def __init__(self):
        super(MovingShapeDemo, self).__init__()
        Text('Random positions', size=48)
        for i in range(20):
            w = randint(10, 50)
            h = randint(10, 50)
            x = randint(0, Game.screen.get_width()-w)
            y = randint(0, Game.screen.get_height()-h)
            d = randint(0, 1)
            vx = randint(-2, 2)
            vy = randint(-2, 2)
            c = colors[randint(0, 6)]
            Rectangle(pos=(x, y), size=(w, h), color=c, v=(vx, vy), d=d)
        
if __name__ == '__main__':
    MovingShapeDemo().run()