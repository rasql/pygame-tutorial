"""Place lines on the screen. 
* Text
* TextLabel to present a list menu
"""

import pygame
from pygame.locals import *
from pygamelib import *

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
    def __init__(self, str, pos=(0, 0), size=24, color=BLACK):
        self.str = str
        self.pos = pos
        self.size = size
        self.color = color
        self.font = pygame.font.Font(None, self.size)

    def draw(self):
        """Draw the text on the screen."""
        self.text = self.font.render(self.str, True, self.color)
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
    """Draw a rectangle on the screen."""
    def __init__(self, rect, d, col):
        self.rect = rect
        self.col = col
        self.d = d

    def draw(self):
        pygame.draw.line(Game.screen, self.col, self.rect.topleft, self.rect.bottomright, self.d)

class Color:
    """Select and return a specific color."""
    str = ['black', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']
    colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]

    def __init__(self, index=0):
        self.index = index
        self.color = Color.colors[index]

    def __str__(self):
        return Color.str[self.index]
    
    def next(self):
        self.index += 1
        self.index %= len(Color.str)
        self.color = Color.colors[self.index]

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        Game.screen = pygame.display.set_mode((640, 240))
        self.objects = [Text('Mouse-drag to place a line')]

        self.bg = ListLabel('Backeground = ', colors, index=1, pos=(0, 20))
        self.objects.append(self.bg)
        
        self.color = ListLabel('Color = ', colors, pos=(0, 40))
        self.objects.append(self.color)
        
        self.day = ListLabel('Day = ', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], pos=(0, 60))
        self.objects.append(self.day)
        
        self.thickness = ListLabel('Thickness = ', ['1', '2', '5', '10'], pos=(0, 80))
        self.objects.append(self.thickness)

    def run(self):
        """Run the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if len(self.objects) > 0:
                            self.objects.pop()
                    elif event.key == K_t:
                        self.thickness.next()
                        self.objects[-1].d = int(self.thickness.value)
                    elif event.key == K_b:
                        self.bg.next()
                    elif event.key == K_c:
                        self.color.next()
                        self.objects[-1].col = self.color.value
                    elif event.key == K_d:
                        self.day.next()

                elif event.type == MOUSEBUTTONDOWN:
                    rect = Rect(event.pos, (10, 10))
                    d = int(self.thickness.value)
                    self.objects.append(Line(rect, d, self.color.value))

                elif event.type == MOUSEBUTTONUP:
                    pass
                elif event.type == MOUSEMOTION:
                    if event.buttons[0]==1:
                        x1, y1 = event.pos
                        self.objects[-1].rect.w = x1-self.objects[-1].rect.x
                        self.objects[-1].rect.h = y1-self.objects[-1].rect.y

            self.draw()

    def draw(self):
        self.screen.fill(self.bg.value)
        for object in self.objects:
            object.draw()
        pygame.display.flip()

if __name__ == '__main__':
  Game().run()