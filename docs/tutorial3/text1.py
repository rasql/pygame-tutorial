"""Draw Text with inherited attributes.
* Text is automatically added to objects.
* Text has the attributes pos, size, color, font."""

import pygame
from pygame.locals import *
from pygamelib import *


class TextDemo(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(TextDemo, self).__init__()
        Text('Hello world', size=100)
        Text('text', color=RED)

        Text('text', size=36, pos=(400, 0))
        Text('text', color=GREEN)
        Text('text')
        ListLabel('menu:', ['a', 'b', 'c'])
        Rectangle(color=RED)
        Ellipse(color=BLUE)
        
if __name__ == '__main__':
    TextDemo().run()