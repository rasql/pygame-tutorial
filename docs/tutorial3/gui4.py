"""Editing graphical shapes. placing rectangles"""

import pygame
from random import randint
from pygame.locals import *
from pygamelib import *

class GuiDemo(App):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(GuiDemo, self).__init__()
        self.shortcuts[K_BACKSPACE] = 'App.objects.pop()'
        Text('Placing rectangles', size=50)
        Text('Press A to add, BACK to remove', size=24)
        self.editing = False

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.key == K_a:
                Rectangle(pos=event.pos, size=(0, 0))
                self.editing = True
            else:
                sel = self.find_objects(event.pos)
                for obj in sel:
                    obj.selected = True

        elif event.type == MOUSEMOTION:
            if self.editing:
                App.objects[-1].rect.inflate_ip(event.rel)

        elif event.type == MOUSEBUTTONUP:
            self.editing = False

if __name__ == '__main__':
    GuiDemo().run()