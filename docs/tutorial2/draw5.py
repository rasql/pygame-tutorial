import pygame
from pygame.locals import *
from pygamelib import *

class LineDemo(App):
    """Drawing lines with the mouse."""
    def __init__(self):
        super(LineDemo, self).__init__()

        self.bg = ListLabel('Background = ', colors, index=1, pos=(0, 20))
        self.color = ListLabel('Color = ', colors, pos=(0, 40))       
        self.thick = ListLabel('Thickness = ', ['1', '2', '5', '10'], pos=(0, 60))

    def on_event(self, event):
        """React to mouseclicks and keydown events."""
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.objects.pop()
            elif event.key == K_t:
                self.thick.next()
                self.objects[-1].d = int(self.thick.value)
            elif event.key == K_b:
                self.bg.next()
            elif event.key == K_c:
                self.color.next()
                self.objects[-1].col = self.color.value

        elif event.type == MOUSEBUTTONDOWN:
            d = int(self.thick.value)
            App.objects.append(Line(event.pos, event.pos, d=d, color=self.color.value))

        elif event.type == MOUSEMOTION:
            if event.buttons[0]==1:
                self.objects[-1].stop = event.pos

            self.draw()

if __name__ == '__main__':
    LineDemo().run()