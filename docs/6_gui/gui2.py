"""Place clickable buttons on the screen."""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

words = ['beauty', 'strength', 'love', 'dream', 'silence']
cmd = {
    K_BACKSPACE:'App.objects.pop()',
    K_t:'print("test")',}

class ButtonDemo(App):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(ButtonDemo, self).__init__()
        self.shortcuts.update(cmd)
        Text('Button Demo')
        Text('Press A to add, BACK to remove', size=24)
        
        Button('Start 1', 'print("start 1")', pos=(10, 100))
        Button('Start 2', 'print("start 2")')
        Button('Stop', 'sys.exit()', pos=(200, 100), color=YELLOW)

if __name__ == '__main__':
    ButtonDemo().run()