"""Draw shapes of different size and color."""

import pygame
from pygamelib import *

class ShapeDemo(Game):
    """Draw ellipses in different sizes and colors."""
    def __init__(self):
        super(ShapeDemo, self).__init__()
        Text('Polygons', size=48)
        Polygon([(100, 40), (10, 100), (200, 100)])
        Polygon([(100, 200), (10, 100), (200, 100)], color=RED, d=3)

        Text('Arcs', size=48, pos=(250, 0))
        Rectangle(size=(100, 50))
        Arc(0, 1, d=1)
        Arc(0, 3, d=3, color=GREEN)
        Arc(0, 6, d=5)
    
        Text('Lines', size=48, pos=(500, 0))
        Line((500, 40), (600, 200), color=MAGENTA)
        
if __name__ == '__main__':
    ShapeDemo().run()