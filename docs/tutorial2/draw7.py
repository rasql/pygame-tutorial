"""Draw shapes (rectangles,) of different size and color."""

import pygame
from pygamelib import *

class RectangleDemo(Game):
    """Draw rectangles in different sizes and colors."""
    def __init__(self):
        super(RectangleDemo, self).__init__()
        Text('Rectangles', size=48)
        Rectangle()
        Rectangle(color=RED)
        Rectangle(d=1)
        Rectangle(color=GREEN, d=4)

        Ellipse(pos=(200,50), d=0)
        Ellipse(color=YELLOW, size=(200, 50))
        Ellipse(d=1, color=BLACK)
        Ellipse(color=GREEN, d=10)

if __name__ == '__main__':
    RectangleDemo().run()