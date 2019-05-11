"""GUI elements - display variables."""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

class GuiDemo(Game):
    """Display variables."""
    def __init__(self):
        super(GuiDemo, self).__init__()
        self.shortcuts[K_UP] = 'self.var1 += 1; print(self.var1)'
        self.shortcuts[K_DOWN] = 'self.var1 -= 1; print(self.var1)'
        self.shortcuts[(K_UP, KMOD_LSHIFT)] = 'self.var1 += 10; print(self.var1)'
        self.shortcuts[(K_DOWN, KMOD_LSHIFT)] = 'self.var1 -= 10; print(self.var1)'
        self.var1 = 12
        self.var2 = 'hello'
        self.var3 = True

        Text('Display variables')
        Text('Press Up/Down to inc by 1', size=24)
        Text('Press shift+Up/Down to inc by 10')
        Text('var1 = ' + str(self.var1))
        Text('var2 = ' + self.var2)
        Text('var3 = ' + str(self.var3))

if __name__ == '__main__':
    GuiDemo().run()