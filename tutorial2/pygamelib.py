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

class Shape:
    """Base class for geometric shapes having size, color and thickness."""
    size = [50, 20]  # default size
    color = BLUE     # default color
    d = 0            # default thickness
    v = [0, 0]       # default speed

    def __init__(self, pos=None, size=None, color=None, d=None, v=None):
        """Define the object attributes from the arguments and class defaults."""
        if pos != None:
            Game.pos = list(pos)
        self.pos = Game.pos[:]

        if size != None:
            Shape.size = list(size)
        self.size = Shape.size[:]
        Game.pos[1] += Shape.size[1] 
        
        if color != None:
            Shape.color = color
        self.color = Shape.color

        if d != None:
            Shape.d = d
        self.d = Shape.d

        if v != None:
            Shape.v = list(v)
        self.v = Shape.v

        self.rect = Rect(self.pos, self.size)
        Game.objects.append(self)

    def draw():
        pass

    def update(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if not 0 < self.pos[0] < Game.screen.get_width()-self.size[0]:
            self.v[0] *= -1
        if not 0 < self.pos[1] < Game.screen.get_height()-self.size[1]:
            self.v[1] *= -1
        self.rect.topleft = self.pos

class Rectangle(Shape):
    """Draw a rectangle on the screen."""
    def __init__(self, **kwargs):
        super(Rectangle, self).__init__(**kwargs)

    def draw(self):
        pygame.draw.rect(Game.screen, self.color, self.rect, self.d)


class Ellipse(Shape):
    """Draw an ellipse on the screen."""  
    def __init__(self, **kwargs):
        super(Ellipse, self).__init__(**kwargs)

    def draw(self):
        pygame.draw.ellipse(Game.screen, self.color, self.rect, self.d)


class Polygon(Shape):
    """Draw a polygon on the screen."""  
    def __init__(self, points, **kwargs):
        super(Polygon, self).__init__(**kwargs)
        self.points = points

    def draw(self):
        pygame.draw.polygon(Game.screen, self.color, self.points, self.d)


class Arc(Shape):
    """Draw an arc on the screen."""  
    def __init__(self, start, stop, **kwargs):
        super(Arc, self).__init__(**kwargs)
        self.start = start
        self.stop = stop

    def draw(self):
        pygame.draw.arc(Game.screen, self.color, self.rect, self.start, self.stop, self.d)

class Line(Shape):
    """Draw a line on the screen."""  
    def __init__(self, start, stop, **kwargs):
        super(Line, self).__init__(**kwargs)
        self.start = start
        self.stop = stop

    def draw(self):
        pygame.draw.line(Game.screen, self.color, self.start, self.stop, self.d)



class Text:
    """Draw a line of text on the screen."""
    
    color = BLACK
    size = 24
    font = None

    def __init__(self, str, pos=None, size=None, color=None, font=None):

        if size != None:
            Text.size = size
        self.size = Text.size

        if pos != None:
            Game.pos = list(pos)
        self.pos = Game.pos[:]
        Game.pos[1] += Text.size * 3 // 4

        if color != None:
            Text.color = color
        self.color = Text.color
        
        self.font = font
        self.set(str)
        Game.objects.append(self)

    def set(self, str, size=None, color=None):
        self.str = str
        if size != None:
            self.size = size
        if color != None:
            self.color = color
        self.font = pygame.font.Font(None, self.size)
        self.text = self.font.render(self.str, True, self.color)

    def update(self):
        pass

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


class Game():
    """Define the main game object and its attributes."""
    
    pos = [0, 0]
    objects = []

    def __init__(self):
        """Initialize pygame and set up the display screen."""
        pygame.init()
        Game.screen = pygame.display.set_mode((640, 240))
        self.bg_color = WHITE
    
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
            self.update()
            self.draw()
        
    def on_event(self, event):
        """Implement an event handler."""
        pass

    def update(self):
        """Update the screen objects (sprites)."""
        for object in Game.objects:
            object.update()

    def draw(self):
        """Draw the game objects to the screen."""
        self.screen.fill(self.bg_color)
        for object in Game.objects:
            object.draw()
        pygame.display.flip()

if __name__ == '__main__':
    Game().run()