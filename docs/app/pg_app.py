import pygame
from pygame.locals import *
import os
import sys
import inspect
import numpy as numpy


class Scene:
    """Create a new scene and initialize the node options."""
    id = 0
    options = {'bg': Color('gray')}

    node_options = {'pos': (20, 20),
                    'size': (100, 40),
                    'dir': (0, 1),
                    'gap': (10, 10),
                    'color': Color('red'),
                    'd': 1,
                    'id': 0,
                    'selected': False,
                    'visible': True}

    def __init__(self, *args, **options):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        Node.options = Scene.node_options.copy()

        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []

        Scene.options.update(options)
        self.bg = Scene.options['bg']

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

    def do_event(self, event):
        """Handle the events of the scene."""
        if event.type == MOUSEBUTTONDOWN:
            for node in self.nodes:
                node.selected = False
                if node.rect.collidepoint(event.pos):
                    node.selected = True

    def __str__(self):
        return 'Scene {}'.format(self.id)


class Node:
    """Create a node."""
    options = {}

    def __init__(self, **options):
        Node.options.update(options)

        # create node attributes from class options
        self.__dict__ = Node.options.copy()
        
        # update the position
        if self.id > 0 : 
            x = self.pos[0] + self.dir[0] * (self.size[0] + self.gap[0])
            y = self.pos[1] + self.dir[1] * (self.size[1] + self.gap[1])
            self.pos = x, y
            Node.options['pos'] = x, y
        
        Node.options['id'] += 1

        self.rect = Rect(*self.pos, *self.size)

        # Append the node to the current window
        App.scene.nodes.append(self)

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, self.d)
        if self.selected:
            pygame.draw.rect(App.screen, Color('blue'), self.rect, 3)

    def __str__(self):
        return self.__class__.__name__ + str(self.id)
            

class Text(Node):
    """Create a text object which knows how to draw itself."""

    def __init__(self, text, **options):
        """Instantiate and render the text object."""
        super().__init__(**options)

        self.str = text
        self.fontsize = 72
        self.fontcolor = Color('black')
        self.render()

        # Append the node to the current window
        App.scene.nodes.append(self)

    def render(self):
        """Render the string and create a surface object."""
        self.font = pygame.font.Font(None, self.fontsize)
        self.text = self.font.render(self.str, True, self.fontcolor)
        self.rect = self.text.get_rect()
        self.rect.topleft = self.pos
        self.size = self.rect.size
        Node.options['size'] = self.size

    def draw(self):
        """Draw the text surface on the screen."""
        App.screen.blit(self.text, self.pos)
        Node.draw(self)


class Rectangle(Node):
    """Draw a rectangle on the screen."""

    def __init__(self, **options):
        super().__init__(**options)

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, self.d)
        Node.draw(self)


class Ellipse(Node):
    """Draw an ellipse on the screen."""

    def __init__(self, **options):
        super().__init__(**options)

    def draw(self):
        pygame.draw.ellipse(App.screen, self.color, self.rect, self.d)
        Node.draw(self)


class Button:
    pass


class App:
    """Create a single-window app with multiple scenes."""
    scenes = []
    scene = None

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((640, 240), flags)

        self.shortcuts = {K_ESCAPE: 'App.running=False',
                          K_p: 'self.capture()',
                          K_w: 'self.where()',
                          K_s: 'self.next_scene()',
                          }

        App.running = True

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

                if event.type == KEYDOWN:
                    self.do_shortcut(event)

                # Send the event to the scene
                App.scene.do_event(event)

            self.draw()

        pygame.quit()

    def draw(self):
        """Draw the objects of the current scene to the screen."""
        App.scene.draw()

    def next_scene(self):
        """Switch to the next scene."""
        i = App.scenes.index(App.scene)
        n = len(App.scenes)
        i = (i+1) % n
        App.scene = App.scenes[i]

    def do_shortcut(self, event):
        """Check if the key/mod combination is part of the shortcuts
        dictionary and execute it. More shortcuts can be added 
        to the ``self.shortcuts`` dictionary by the program."""
        k = event.key
        m = event.mod

        if k in self.shortcuts and m == 0:
            exec(self.shortcuts[k])
        elif (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])

    def capture(self):
        """Save a screen capture to the directory of the 
        calling class, under the class name in PNG format."""
        name = type(self).__name__
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
        name, ext = os.path.splitext(name)
        filename = path + '/' + name + '.png'
        pygame.image.save(App.screen, filename)


if __name__ == '__main__':
    app = App()
    s0 = Scene()
    App.scenes.append(s0)
    App.scene = s0
    app.run()
