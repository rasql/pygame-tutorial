"""Place lines on the screen"""

import pygame
from pygame.locals import *
from pygamelib import *

class Line:
    """Draw a rectangle on the screen."""
    def __init__(self, rect, d):
        self.rect = rect
        self.col = RED
        self.d = d

    def draw(self):
        pygame.draw.line(Game.screen, self.col, self.rect.topleft, self.rect.bottomright, self.d)

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        Game.screen = pygame.display.set_mode((640, 240))
        self.bg = YELLOW
        self.str = 'mouseclick to place rect, backspace to remove'
        self.font = pygame.font.Font(None, 24)
        self.objects = []
        self.key = None
        self.d = 1

    def run(self):
        """Run the main event loop."""
        d = {K_UP:(0, -10), K_DOWN:(0, 10), K_LEFT:(-10, 0), K_RIGHT:(10, 0)}
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if len(self.objects) > 0:
                            self.objects.pop()
                    elif event.key == K_d:
                        self.d += 1
                        self.d %= 5
                        self.objects[-1].d = self.d
                    else:
                        self.key = event.key

                elif event.type == MOUSEBUTTONDOWN:
                    rect = Rect(event.pos, (10, 10))
                    self.objects.append(Line(rect, self.d))

                elif event.type == MOUSEBUTTONUP:
                    pass
                elif event.type == MOUSEMOTION:
                    if event.buttons[0]==1:
                        x1, y1 = event.pos
                        self.objects[-1].rect.w = x1-self.objects[-1].rect.x
                        self.objects[-1].rect.h = y1-self.objects[-1].rect.y

            self.draw()

    def draw(self):
        self.screen.fill(self.bg)
        self.text = self.font.render(self.str, True, BLACK)
        self.screen.blit(self.text, (10, 10))

        for object in self.objects:
            object.draw()
        pygame.display.flip()

if __name__ == '__main__':
  Game().run()