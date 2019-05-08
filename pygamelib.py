"""This pygame library provides useful classes for making games quickly."""

import os, sys, inspect
import pygame
from pygame.locals import *

SHIFT = KMOD_LSHIFT + KMOD_RSHIFT
CTRL = KMOD_LCTRL + KMOD_RCTRL

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTGRAY = (240, 240, 240)


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
    """Base class for geometric shapes. They have 
    * size, color and thickness.
    * position, speed, friction and gravity."""
    
    size = [50, 20]  # default size
    color = BLUE     # default color
    d = 0            # default thickness
    v = [0, 0]       # default speed
    selection_color = RED
    selection_d = 3

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
        self.selected = False
        self.cmd = ''
        Game.objects.append(self)

    def draw(self):
        pass

    def select(self):
        color = Shape.selection_color
        d = Shape.selection_d
        pygame.draw.rect(Game.screen, color, self.rect, d)

    def update(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if not 0 < self.pos[0] < Game.w-self.size[0]:
            self.v[0] *= -1
        if not 0 < self.pos[1] < Game.h-self.size[1]:
            self.v[1] *= -1
        self.rect.topleft = self.pos

class Rectangle(Shape):
    """Draw a rectangle on the screen."""
    def __init__(self, **kwargs):
        super(Rectangle, self).__init__(**kwargs)

    def draw(self):
        pygame.draw.rect(Game.screen, self.color, self.rect, self.d)
        if self.selected:
            self.select()

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
    v = [0, 0]

    def __init__(self, str, pos=None, size=None, color=None, font=None, v=None):

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
        
        if v != None:
            Text.v = list(v)
        self.v = Text.v

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
        self.rect = self.text.get_rect()

    def update(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if not 0 < self.pos[0] < Game.w-self.rect.w:
            self.v[0] *= -1
        if not 0 < self.pos[1] < Game.h-self.rect.h:
            self.v[1] *= -1
        self.rect.topleft = self.pos

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


class Button(Shape):
    """Draw Button on the screen.""" 
    size = [120, 40]
    color = WHITE
    d = 3
     
    def __init__(self, msg, cmd, size=None, color=None, d=None, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.msg = msg
        self.cmd = cmd

        if color != None:
            Button.color = color
        self.color = Button.color

        if size != None:
            Button.size = list(size)
        self.size = Button.size
        self.rect.size = self.size
        Game.pos[1] += Button.size[1]

        if d != None:
            Button.d = d
        self.d = Button.d
        
        self.font = pygame.font.Font(None, self.size[1])
        self.text = self.font.render(self.msg, True, BLACK)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self):
        pygame.draw.rect(Game.screen, self.color, self.rect, 0)
        pygame.draw.rect(Game.screen, BLACK, self.rect, self.d)
        Game.screen.blit(self.text, self.text_rect)

    def update(self):
        pass

class Game():
    """Define the main game object and its attributes."""
    
    pos = [10, 10]   # current position for object placement
    objects = []   # objects to display
    selection = [] # current selection

    def __init__(self):
        """Initialize pygame and set up the display screen."""
        pygame.init()
        flags = RESIZABLE
        Game.screen = pygame.display.set_mode((640, 240), flags)
        Game.w = Game.screen.get_width()
        Game.h = Game.screen.get_height()
        self.bg_color = LIGHTGRAY
        self.key = None
        self.mod = None
        self.shortcuts = {  K_ESCAPE:'self.running=False', 
                            K_p:'self.capture()',
                            K_w:'self.who_where()',
        }
        self.running = True
    
    def run(self):
        """Run the main event loop.
        Handle the QUIT event and call ``on_event``. """
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    self.do_shortcuts(event)
                    self.key = event.key
                    self.mod = event.mod
                elif event.type == MOUSEBUTTONDOWN:
                    for obj in Game.objects:
                        if obj.rect.collidepoint(event.pos):
                            exec(obj.cmd)
                elif event.type == VIDEORESIZE:
                    print(event)
                self.on_event(event)
            self.update()
            self.draw()

        pygame.quit()
        
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
    
    def capture(self):
        """Save a screen capture to the directory of the 
        calling class, under the class name in PNG format."""
        name = type(self).__name__
        module = sys.modules['__main__']
        path = os.path.dirname(module.__file__)
        filename = path + '/' + name + '.png'
        pygame.image.save(Game.screen, filename)

    def find_objects(self, pos):
        """Return the objects at position."""
        return [obj for obj in Game.objects if obj.rect.collidepoint(pos)]

    def do_shortcuts(self, event):
        """Check if the key/mod combination is part of the shortcuts
        dictionary and execute it. More shortcuts can be added 
        by the program to the ``self.shortcuts`` dictionary."""
        k = event.key
        m = event.mod

        if m & KMOD_ALT:
            m |= KMOD_ALT
        if m & KMOD_CTRL:
            m |= KMOD_CTRL
        if m & KMOD_SHIFT: 
            m |= KMOD_SHIFT

        if k in self.shortcuts and m == 0 :
            exec(self.shortcuts[k])
        elif (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])

    def who_where(self):
        """Print info to the current caller."""
        print('\nwho_where')
        print('__name__  =', __name__)
        print('__class__ =', __class__)
        print('self', self)
        print(type(self).__name__)
        module = sys.modules['__main__']
        print(module.__name__)
        print(module.__file__)
        print(os.path.dirname(module.__file__))
        
if __name__ == '__main__':
    Game().run()