import pygame
from pygame.locals import *
import os

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

DARKRED = (127, 0, 0)
DARKBLUE = (0, 0, 127)
DARKGREEN = (0, 127,0)

text = '''This is a
multi-line
text file.
'''

class App:
    """Create the application."""
    screen = None
    selected = None

    def __init__(self):
        pygame.init()
        self.rect = Rect(0, 0, 800, 600)
        self.background_color = GRAY
        self.title = 'Hacker Desktop Environment'
        self.children = []
        App.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(self.title)

        x, y = 20, 20
        dy = 120
        Icon(self, 'icons/address-book.png', pos=(x, y)); y += dy
        Icon(self, 'icons/device-camera.png', pos=(x, y)); y += dy
        Icon(self, 'icons/device-computer.png', pos=(x, y)); y += dy
        Icon(self, 'icons/device-drive.png', pos=(x, y)); y += dy
        Icon(self, 'icons/device-laptop.png', pos=(x, y))

        folder = Window(self, 'Target user', Rect(150, 50, 400, 300))
        Icon(folder, 'icons/user-male.png', pos=(20, 60))
        Icon(folder, 'icons/user-female.png', pos=(150, 60))

        Image(self, 'images/hacker.jpg', pos=(120, 260))
        Text(self, 'Hacker Environment', pos=(300, 10))
        TextFile(self, 'Text.txt', text, Rect(400, 100, 500, 200))

        Terminal(self, 'Terminal', '> mkdir hacking_files', Rect(400,350, 500, 200))
        
        
    def run(self):
        """Run the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    App.selected = None
                for child in self.children:
                    child.do_event(event)

            self.draw()

        pygame.quit()

    def draw(self, pos=(0, 0)):
        """Draw the objects of the main screen."""
        self.screen.fill(self.background_color)
        for child in self.children:
            child.draw(pos)
        pygame.display.flip()


class Node:
    sel_color = DARKRED
    """Create a node class for embedded objects."""
    def __init__(self, parent, rect=Rect(20, 20, 200, 100), **options):

        self.parent = parent
        self.parent.children.append(self)
        self.children = []
        self.rect = rect
        self.abs_rect = rect
        self.visible = True
        self.outlined = True
        self.editable = False
        self.movable = True
        self.selectable = True
        self.color = DARKBLUE
        self.time = 0
        self.__dict__.update(options)

    def draw(self, pos):
        """Draw the node and its children."""
        if self.visible:
            if self.outlined:
                pygame.draw.rect(App.screen, self.color, self.rect.move(*pos), 1)
            for child in self.children:
                child.draw(self.rect.topleft)
        if self is App.selected:
            pygame.draw.rect(App.screen, Node.sel_color, self.rect.move(*pos), 3)

    def do_event(self, event):
        """Handle mouse clicks and key press events."""

        if event.type == MOUSEBUTTONDOWN:
            self.abs_rect = self.rect.move(self.parent.rect.topleft)

            if self.abs_rect.collidepoint(event.pos) and self.selectable:
                
                # place the selected object on the top
                self.parent.children.remove(self)
                self.parent.children.append(self)

                App.selected = self
                self.click_pos = event.pos

                # detect double click
                t = pygame.time.get_ticks()
                if t - self.time < 200:
                    self.double_click()
                self.time = t

                print('clicked in', self)

        for child in self.children:
            child.do_event(event)

        if self is App.selected:
            if event.type == MOUSEMOTION and event.buttons[0] == 1 and self.movable:
                self.rect.move_ip(event.rel)

    def double_click(self):
        print('double-click in', self)

    def __str__(self):
        """Return a string to name the object."""
        return '{} at ({}, {})'.format(self.__class__.__name__, *self.rect.topleft)

    def __repr__(self):
        """Return a representation of the object."""
        return '{}()'.format(self.__class__.__name__)


class Text(Node):
    """Create an editable text object."""
    def __init__(self, parent, text, pos=(0, 0), fontcolor=BLACK, **options):
        super().__init__(parent, pos)
        self.text = text
        self.pos = pos
        self.fontcolor = fontcolor
        self.fontsize = 36
        self.editable = True
        self.render()
        self.__dict__.update(options)

    def render(self):
        """Create a surface image of the text."""
        self.font = pygame.font.Font(None, self.fontsize)
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, pos):
        """Draw the text object."""
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos))

    def do_event(self, event):
        super().do_event(event)
        if self is App.selected and event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == K_RETURN:
                print('Return')
            elif event.key == K_TAB:
                print('Tab')
            else:
                self.text += event.unicode
            self.render()


class Icon(Node):
    def __init__(self, parent, file, pos=(100, 100)):
        super().__init__(parent, pos)

        self.file = file
        self.img = pygame.image.load(file)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.outlined = False

    def draw(self, pos=(0, 0)):
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos))


class Window(Node):
    """Create a window object."""
    def __init__(self, parent, title, rect=Rect(100, 100, 300, 200)):
        super().__init__(parent, rect)

        self.title = title
        self.rect = rect
        self.border_color = BLACK
        self.border_width = 3
        self.background_color = WHITE
        self.titlebar_color = DARKBLUE
        self.outlined = False
        
        Text(self, title, fontcolor=WHITE, pos=(10, 10), movable=False, selectable=False, outlined=False)

    def draw(self, pos=(0, 0)):
        """Draw window with title bar."""
        super().draw(pos)
        pygame.draw.rect(App.screen, self.background_color, self.rect, 0)
        pygame.draw.rect(App.screen, self.titlebar_color, (*self.rect.topleft, self.rect.width, 40))
        pygame.draw.rect(App.screen, self.border_color, self.rect, self.border_width)
        for child in self.children:
            child.draw(self.rect.topleft)

class Image(Window):
    """Display an image in a window."""
    def __init__(self, parent, file, pos=(100, 100)):
        super().__init__(parent, file, pos)

        self.title = file
        self.titlebar_color = DARKRED
        self.img = pygame.image.load(file)
        # self.img = pygame.transform.scale(self.img, (80, 80))
        self.rect = self.img.get_rect()
        self.rect.topleft = pos

    def draw(self, pos=(0, 0)):
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos).move(0, 40))
        
class TextFile(Window):
    """Create a folder object."""
    def __init__(self, parent, name, lines, rect):
        super().__init__(parent, name, rect)

        x, y = 10, 50
        for line in lines.splitlines():
            Text(self, line, pos=(x, y), movable=False, outlined=False)
            y += 30

class Terminal(Window):
    """Create a terminal object."""
    def __init__(self, parent, name, lines, rect):
        super().__init__(parent, name, rect)
        self.background_color = BLACK
        self.titlebar_color = DARKGREEN

        x, y = 10, 50
        for line in lines.splitlines():
            Text(self, line, pos=(x, y), movable=False, outlined=False, fontcolor=WHITE)
            y += 30

if __name__ == '__main__':
    App().run()