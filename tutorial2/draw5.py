import pygame
from pygame.locals import *
from pygamelib import *

class LineDemo(Game):
    """Drawing lines with the mouse."""
    def __init__(self):
        super(LineDemo, self).__init__()

        self.bg = ListLabel('Backeground = ', colors, index=1, pos=(0, 20))
        self.objects.append(self.bg)
        
        self.color = ListLabel('Color = ', colors, pos=(0, 40))
        self.objects.append(self.color)
                
        self.thickness = ListLabel('Thickness = ', ['1', '2', '5', '10'], pos=(0, 60))
        self.objects.append(self.thickness)

    def on_event(self, event):
        """React to mouseclicks and keydown events."""
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.objects.pop()
            elif event.key == K_t:
                self.thickness.next()
                self.objects[-1].d = int(self.thickness.value)
            elif event.key == K_b:
                self.bg.next()
            elif event.key == K_c:
                self.color.next()
                self.objects[-1].col = self.color.value

        elif event.type == MOUSEBUTTONDOWN:
            rect = Rect(event.pos, (10, 10))
            d = int(self.thickness.value)
            self.objects.append(Line(rect, d, self.color.value))

        elif event.type == MOUSEMOTION:
            if event.buttons[0]==1:
                x1, y1 = event.pos
                self.objects[-1].rect.w = x1-self.objects[-1].rect.x
                self.objects[-1].rect.h = y1-self.objects[-1].rect.y

            self.draw()

if __name__ == '__main__':
    LineDemo().run()