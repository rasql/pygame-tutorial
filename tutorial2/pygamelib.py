"""This is the pygame library with utility functions and definitions."""
import pygame
from pygame.locals import *


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


colors = {
    'black':BLACK, 
    'red':RED, 
    'green':GREEN, 
    'blue':BLUE, 
    'yellow':YELLOW,
    'cyan':CYAN,
    'magenta':MAGENTA,
    'white':WHITE,
}


class Text:
    """Draw a line of text on the screen."""
    def __init__(self, str, pos=(0, 0), size=24, color=BLACK, font=None):
        self.pos = pos
        self.size = size
        self.color = color
        self.font = font
        self.set(str)

    def set(self, str, size=None, color=None):
        self.str = str
        if size != None:
            self.size = size
        if color != None:
            self.color = color
        self.font = pygame.font.Font(None, self.size)
        self.text = self.font.render(self.str, True, self.color)

    def draw(self):
        """Draw the text on the screen."""
        Game.screen.blit(self.text, self.pos)


class ListLabel(Text):
    """Draw a label with an item chosen from a list.
    Display 'Label = item'. """
    def __init__(self, label, items, index=0, **kwargs):
        if isinstance(items, dict):
            self.keys = list(items.keys())
            self.values = list(items.values())
        else:
            self.keys = items
            self.values = items
        self.index = index
        self.value = self.values[index]
        self.key = self.keys[index]
        self.label = label
        super(ListLabel, self).__init__(label + self.key, **kwargs)
    
    def next(self):
        """Increment cyclically to the next item."""
        self.index += 1
        self.index %= len(self.values)
        self.value = self.values[self.index]
        self.key = self.keys[self.index]
        self.str = self.label + self.key
        return self.value


class Line:
    """Draw a line on the screen."""
    def __init__(self, rect, d, col):
        self.rect = rect
        self.col = col
        self.d = d

    def draw(self):
        pygame.draw.line(Game.screen, self.col, self.rect.topleft, self.rect.bottomright, self.d)


class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        Game.screen = pygame.display.set_mode((640, 240))
        self.bg_color = WHITE
        self.objects = []
    
    def run(self):
        """Run the main event loop.
        Handle the QUIT event and call ``on_event``. """
        running = True
        while running:
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False
                else:
                    self.on_event(event)
            self.draw()
        
    def on_event(self, event):
        """Implement an event handler."""
        pass

    def draw(self):
        """Draw the game objects to the screen."""
        self.screen.fill(self.bg_color)
        for object in self.objects:
            object.draw()
        pygame.display.flip()


if __name__ == '__main__':
    Game().run()