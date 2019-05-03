"""Floating text."""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

words = ['beauty', 'strength', 'love', 'dream', 'silence']
cmd = {
    K_a:'self.new_text()', 
    K_BACKSPACE:'Game.objects.pop()',
    K_p:'Game.capture(self)',}

class TextDemo(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(TextDemo, self).__init__()
        Text('Floating text', size=50)
        Text('Press A to add, BACK to remove', size=24)

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

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key in cmd:
                eval(cmd[event.key])
            # if event.key == K_a:
            #     self.new_text()
            # if event.key == K_BACKSPACE:
            #     Game.objects.pop()

if __name__ == '__main__':
    TextDemo().run()