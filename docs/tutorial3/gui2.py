"""Menu elements
* Button
* ListMenu
* Var
"""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

words = ['beauty', 'strength', 'love', 'dream', 'silence']
cmd = {
    K_BACKSPACE:'Game.objects.pop()',
    K_p:'Game.capture(self)',
    K_t:'print("test")',}

class ButtonDemo(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(ButtonDemo, self).__init__()
        self.shortcuts.update(cmd)
        Text('Button Demo', size=48)
        Text('Press A to add, BACK to remove', size=24)
        
        Button('Start 1', 'print("start 1")')
        Button('Start 2', 'print("start 2")')
        Button('Stop', 'self.running=False', pos=(200, 100), color=YELLOW)
        Button('Quit', 'sys.exit()')

if __name__ == '__main__':
    ButtonDemo().run()