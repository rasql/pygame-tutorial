"""This pygame library provides useful classes for making games quickly."""

import os, sys, inspect
import pygame
from pygame.locals import *
import numpy as np


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
    """Base class for geometric shapes objects to place in the game.
    Shapes have the following attributes: 

    * size
    * color
    * thickness
    * position, speed, 
    * friction, gravity
    """
    pos = [10, 10]   # default position
    size = [100, 40] # default size
    gap = 2          # defalut gap
    color = GREEN    # default color
    d = 0            # default thickness
    v = [0, 0]       # default speed
    selection_color = BLUE
    selection_d = 2

    def __init__(self, pos=None, size=None, color=None, d=None, v=None):
        """Define the object attributes from the arguments and class defaults."""
        
        if pos != None:
            Shape.pos = list(pos)
        self.pos = Shape.pos[:]

        if size != None:
            Shape.size = list(size)
        self.size = Shape.size[:]
        Shape.pos[1] += Shape.size[1] + Shape.gap
        
        if color != None:
            Shape.color = color
        self.color = Shape.color

        if d != None:
            Shape.d = d
        self.d = Shape.d

        if v != None:
            Shape.v = list(v)
        self.v = Shape.v[:]

        self.rect = Rect(self.pos, self.size)
        self.is_active = False
        self.cmd = ''
        Game.objects.append(self)

    def draw(self):
        """Draw the object to the screen."""
        if self.is_active:
            self.select()

    def on_click(self, event):
        """Handle a mouse click."""
        pass

    def on_key(self, event):
        """Handle a key press event."""
        if self.is_active:
            if pygame.key.get_mods() & KMOD_META:
                d = {K_UP:(0, -1), K_DOWN:(0, 1), K_LEFT:(-1, 1), K_RIGHT:(1, 0)}
                if event.key in d:
                    dv = d[event.key]
                    self.v[0] += dv[0]
                    self.v[1] += dv[1]
                if event.key == K_s:
                    self.v = [0, 0]

    def select(self):
        """Surround the object with a frame."""
        color = Shape.selection_color
        d = Shape.selection_d
        pygame.draw.rect(Game.screen, color, self.rect, d)

    def update(self):
        """Update the position of the object."""
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if not 0 < self.pos[0] < Game.w-self.rect.w:
            self.v[0] *= -1
        if not 0 < self.pos[1] < Game.h-self.rect.h:
            self.v[1] *= -1
        self.rect.topleft = self.pos

class Rectangle(Shape):
    """Draw a rectangle on the screen."""
    def __init__(self, **kwargs):
        super(Rectangle, self).__init__(**kwargs)

    def draw(self):
        pygame.draw.rect(Game.screen, self.color, self.rect, self.d)
        Shape.draw(self)
 

class Ellipse(Shape):
    """Draw an ellipse on the screen."""  
    def __init__(self, **kwargs):
        super(Ellipse, self).__init__(**kwargs)

    def draw(self):
        pygame.draw.ellipse(Game.screen, self.color, self.rect, self.d)
        Shape.draw(self)


class Polygon(Shape):
    """Draw a polygon on the screen."""  
    def __init__(self, points=[], **kwargs):
        super(Polygon, self).__init__(**kwargs)
        self.points = points

    def draw(self):
        pygame.draw.polygon(Game.screen, self.color, self.points, self.d)
        Shape.draw(self)


class Arc(Shape):
    """Draw an arc on the screen."""  
    def __init__(self, start, stop, **kwargs):
        super(Arc, self).__init__(**kwargs)
        self.start = start
        self.stop = stop

    def draw(self):
        pygame.draw.arc(Game.screen, self.color, self.rect, self.start, self.stop, self.d)
        Shape.draw(self)


class Line(Shape):
    """Draw a line on the screen."""  
    def __init__(self, start, stop, **kwargs):
        super(Line, self).__init__(**kwargs)
        self.start = start
        self.stop = stop

    def draw(self):
        pygame.draw.line(Game.screen, self.color, self.start, self.stop, self.d)
        Shape.draw(self)


class Text(Shape):
    """Draw a line of text on the screen."""
    fontcolor = BLACK
    fontsize = 24
    fontname = None
    bgcolor = None

    def __init__(self, str='', size=None, color=None, bgcolor=None, font=None, **kwargs):
        if size != None:
            Text.fontsize = size
        self.fontsize = Text.fontsize

        if font != None:
            Text.fontname = font
        self.fontname = Text.fontname

        if color != None:
            Text.fontcolor = color
        self.fontcolor = Text.fontcolor

        if bgcolor != None:
            Text.bgcolor = bgcolor
        self.bgcolor = Text.bgcolor
        
        self.str = str
        self.render()     

        super(Text, self).__init__(size=self.rect.size, **kwargs)

    def render(self):
        """Render the string and create an Surface object."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.text = self.font.render(self.str, True, self.fontcolor, self.bgcolor)
        self.rect = self.text.get_rect()

    def draw(self):
        """Draw the text on the screen."""
        Game.screen.blit(self.text, self.pos)
        Shape.draw(self)

    def on_key(self, event):
        """Edit the text. Backspace to delete."""
        Shape.on_key(self, event)
        if not pygame.key.get_mods() & (KMOD_CTRL | KMOD_META):
            if event.key == K_BACKSPACE:
                self.str = self.str[:-1]
            else:
                self.str = self.str + event.unicode
            self.render()


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
        self.render()
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

    def on_click(self, event):
        eval(self.cmd)


class Board(Shape):
    """Represents a nxm board with n rows and m columns.
    n, m    number of cells (row, column)
    i, j    index of cell (row, column)
    dx, dy  size of cell
    x0, y0  origin of first cell
    """
    
    def __init__(self, n=8, m=8, dx=20, dy=20, pos=None, **kwargs):
        self.size = (m * dx, n * dy)
        super(Board, self).__init__(pos=pos, size=self.size, **kwargs)
        self.n = n
        self.m = m
        self.i = 0
        self.j = 0
        self.col = RED
        self.dx = dx
        self.dy = dy
        self.x0, self.y0 = self.pos
        self.sel = set()    # set of selected cells
        self.rect = Rect(self.pos, self.size)
        self.is_active = False
        self.wrap = False
        self.T = np.zeros((n, m), int)
        
    def draw(self):
        x0, y0 = self.pos
        x1, y1 = self.get_pos((self.n, self.m))
        for i in range(self.n+1):
            y = y0 + i * self.dy
            pygame.draw.line(Game.screen, BLACK, (x0, y), (x1, y))
        for j in range(self.m+1):
            x = x0 + j * self.dx
            pygame.draw.line(Game.screen, BLACK, (x, y0), (x, y1))

        for i in range(self.n):
            font = pygame.font.Font(None, 24)
            for j in range(self.m):
                x, y = self.get_pos((i, j))
                text = font.render(str(self.T[i, j]), True, BLACK)
                rect = text.get_rect()
                rect.center = x + self.dx//2, y + self.dy//2
                Game.screen.blit(text, rect)
        
        for s in self.sel:
            rect = pygame.Rect(self.get_pos(s), (self.dx, self.dy))
            pygame.draw.rect(Game.screen, RED, rect, 3)
        Shape.draw(self)
    
    def get_index(self, pos):
        j = (pos[0] - self.pos[0]) // self.dx
        i = (pos[1] - self.pos[1]) // self.dy
        return i, j

    def get_pos(self, index):
        x = self.pos[0] + index[1] * self.dx
        y = self.pos[1] + index[0] * self.dy
        return x, y

    def on_click(self, event):
        """Add clicked cell to selection."""
        if pygame.key.get_mods() & KMOD_META:
            self.sel.add(self.get_index(event.pos))
        else:
            self.sel = set([self.get_index(event.pos)])

    def on_key(self, event):
        """Move the current cell if there is only one."""
        if len(self.sel) == 1:
             d = {K_LEFT:(0, -1), K_RIGHT:(0, 1), K_UP:(-1, 0), K_DOWN:(1, 0), }
             if event.key in d:
                i, j = list(self.sel)[0]
                di, dj = d[event.key]
                i += di
                j += dj
                if self.wrap:
                    i %= self.n
                    j %= self.m
                else:
                    i = 0 if i < 0 else self.n-1 if i >= self.n else i
                    j = 0 if j < 0 else self.m-1 if j >= self.m else j
                self.sel = {(i, j)}


class Game():
    """Define the main game object and its attributes."""

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
        self.current_obj = None
        self.shortcuts = {  K_ESCAPE:'Game.running=False', 
                            K_p:'self.capture()',
        }
        Game.running = True
    
    def run(self):
        """Run the main event loop.
        Handle the QUIT event and call ``on_event``. """
        while Game.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Game.running = False

                elif event.type == KEYDOWN:
                    self.do_shortcuts(event)
                    self.key = event.key
                    self.mod = event.mod
                    if self.current_obj:
                        self.current_obj.on_key(event)

                elif event.type == MOUSEBUTTONDOWN:
                    for obj in Game.objects:
                        if obj.rect.collidepoint(event.pos):
                            if self.current_obj:
                                self.current_obj.is_active = False
                            self.current_obj = obj
                            obj.is_active = True
                            obj.on_click(event)

                elif event.type == MOUSEMOTION:
                    if self.current_obj:
                        if pygame.key.get_mods() & KMOD_META:
                            self.current_obj.pos = list(event.pos)

                elif event.type == VIDEORESIZE:
                    print(event)
                self.on_event(event)
            self.update()
            self.draw()

        pygame.quit()
        
    def on_event(self, event):
        """Implement a general-purpose event handler."""
        pass

    def update(self):
        """Update the screen objects."""
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
        to the ``self.shortcuts`` dictionary by the program."""
        k = event.key
        m = event.mod

        if k in self.shortcuts and m == 0 :
            exec(self.shortcuts[k])
        elif (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])
        
if __name__ == '__main__':
    Game().run()