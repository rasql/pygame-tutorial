"""
Create the application class
----------------------------
"""

import pygame
from pygame.locals import *
import os
import sys
import inspect
import numpy as numpy


class Scene:
    """Create a new scene and initialize the node options."""
    id = 0
    options = {'bg': Color('gray'),
               'caption': 'Scene',
               'size': (800, 600),
               'flags': 0, }

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
        self.size = Scene.options['size']
        self.caption = Scene.options['caption']
        self.set_scene()

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

    def set_scene(self):
        pygame.display.set_caption(self.caption)
        pygame.display.set_mode(self.size)


class Node:
    """Create a node."""
    default = {'pos': (20, 20),
               'size': (100, 40),
               'dir': (0, 1),
               'gap': (10, 10),
               'color': Color('red'),
               'd': 1,
               'id': 0,
               'selected': False,
               'visible': True}

    options = {}

    def __init__(self, **options):
        Node.options.update(options)

        # create node attributes from class options
        self.__dict__ = Node.options.copy()

        # update the position
        if self.id > 0:
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

    def reset_options(self):
        Node.__dict__.update(Node.default)


class App:
    """Create a single-window app with multiple scenes."""
    size = (640, 240)
    caption = 'Pygame'
    flags = RESIZABLE

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
                          K_i: 'self.info()'
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

                # if there is no scene, then create a dummy one
                if App.scene == None:
                    Scene()

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
        App.scene.set_scene()

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

    def info(self):
        """Print display info."""
        print('info', '-'*40)
        # d = pygame.display.get_wm_info() # empty
        info = pygame.display.Info()
        # for k, y in d.items():
        #     print(k, v, sep='\t')
        print(info)


if __name__ == '__main__':
    App().run()
