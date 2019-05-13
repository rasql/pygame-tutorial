"""Display example text on the screen.
Vary color, size and position.
Add new text objects with a mouse click.
Type to add text."""

import pygame
from pygame.locals import *
from pygamelib import *

class TextDemo(App):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(TextDemo, self).__init__()
        self.objects.append(Text('red', color=RED))
        self.objects.append(Text('green', color=GREEN, pos=(30, 30)))
        self.objects.append(Text('size=48', pos=(100, 100), size=48))
        self.objects.append(Text('size=72', color=BLUE, pos=(100, 160), size=72))
    
    def on_event(self, event):
        """React to mouseclicks and keydown events."""
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.objects.pop()
            else:
                s = self.objects[-1].str + event.unicode
                self.objects[-1].render()

        elif event.type == MOUSEBUTTONDOWN:
            rect = Rect(event.pos, (10, 10))
            self.objects.append(Text('', pos=event.pos))

if __name__ == '__main__':
    TextDemo().run()
