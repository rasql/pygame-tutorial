"""Place a rectangle or ellipse by clicking and dragging with the mouse.
Press E to draw an ellipse and R to draw a rectangle."""

import pygame
from pygame.locals import *
from pygamelib import *

class Rectangle:
    """Draw a rectangle on the screen."""
    def __init__(self, rect):
        self.rect = rect
        self.col = RED

    def draw(self):
        pygame.draw.rect(App.screen, self.col, self.rect)
    
class Ellipse:
    """Draw an ellipse on the screen."""
    def __init__(self, rect):
        self.rect = rect
        self.col = BLUE

    def draw(self):
        pygame.draw.ellipse(App.screen, self.col, self.rect)

class Text:
    """Draw a line of text on the screen."""
    def __init__(self, str, pos=(0, 0), size=24, color=BLACK):
        self.str = str
        self.pos = pos
        self.size = size
        self.color = color
        self.font = pygame.font.Font(None, self.size)

    def draw(self):
        """Draw the text on the screen."""
        self.text = self.font.render(self.str, True, self.color)
        App.screen.blit(self.text, self.pos)

class App():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        App.screen = pygame.display.set_mode((640, 240))
        self.bg = YELLOW
        self.objects = []
        self.objects.append(Text('mouse-click to place rect, back-space to remove rect'))
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

        for object in self.objects:
            object.draw()
        pygame.display.flip()

if __name__ == '__main__':
  App().run()