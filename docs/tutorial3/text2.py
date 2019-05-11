"""
Floating text
-------------

In this exemple words from a list float over the screen, 
with random speed vx and vy in the range (-3, ... +3), 
and starting at random positions.
"""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

words = ['beauty', 'strength', 'love', 'dream', 'silence']

class TextDemo2(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(TextDemo2, self).__init__()
        self.shortcuts[K_a] = 'self.new_text()'
        self.shortcuts[(K_BACKSPACE, KMOD_LMETA)] = 'Game.objects.pop()'
        
        Text('Floating text', size=50)
        Text('Press A to add, cmd+BACK to remove', size=24)
        for i in range(10):
            self.new_text()

    def new_text(self):
        i = randint(0, 4)
        word = words[i]
        vx = randint(-3, 3)
        vy = randint(-3, 3)
        size = randint(20, 40)
        x = randint(0, Game.w)
        y = randint(0, Game.h)
        Text(word, pos=(x, y), size=size, v=(vx, vy))

if __name__ == '__main__':
    TextDemo2().run()