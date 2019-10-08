"""
Draw Text with attributes
-------------------------

Text is placed on the screen as a **Text()** object.
They are automatically positioned vertically. 
Text can have the attributes:

* color
* size
* position
* font

The next text object inherits the previous attributes.
"""

import pygame
from pygame.locals import *
from pygamelib import *

class TextDemo(App):
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