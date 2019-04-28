"""Place a rectangle by clicking and dragging with the mouse."""

import pygame
from pygame.locals import *
from pygamelib import *

class Rectangle:
    """Draw a rectangle on the screen."""
    def __init__(self, rect):
        self.rect = rect
        self.col = RED

    def draw(self):
        pygame.draw.rect(Game.screen, self.col, self.rect)
    
class Ellipse:
    """Draw an ellipse on the screen."""
    def __init__(self, rect):
        self.rect = rect
        self.col = BLUE

    def draw(self):
        pygame.draw.ellipse(Game.screen, self.col, self.rect)


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
                    else:
                        self.key = event.key

                elif event.type == MOUSEBUTTONDOWN:
                    rect = Rect(event.pos, (10, 10))
                    if self.key == K_e:
                        self.objects.append(Ellipse(rect))
                    else:
                        self.objects.append(Rectangle(rect))
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