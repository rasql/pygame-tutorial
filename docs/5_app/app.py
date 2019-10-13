import pygame
from pygame.locals import *
import os
import sys
import inspect
import numpy as np

class App:
    """Create a single-window app with multiple scenes hierarchial objects."""
    scenes = []
    scene = None
    screen = None
    running = True

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        self.flags = 0
        self.rect = Rect(0, 0, 640, 240)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)

        self.shortcuts = {(K_ESCAPE, KMOD_NONE): 'App.running=False',
                          (K_q, KMOD_LMETA): 'App.running=False',
                          (K_f, KMOD_LMETA): 'self.toggle_fullscreen()',
                          (K_r, KMOD_LMETA): 'self.toggle_resizable()',
                          (K_g, KMOD_LMETA): 'self.toggle_frame()',
                          
                          (K_h, KMOD_LMETA): 'pygame.display.iconify()',
                          (K_p, KMOD_LMETA): 'self.capture()',
                          (K_s, KMOD_LMETA): 'self.next_scene()',

                          (K_e, KMOD_NONE): 'Ellipse(Color("green"), pos=pygame.mouse.get_pos())',
                          (K_n, KMOD_NONE): 'Node(pos=pygame.mouse.get_pos())',
                          (K_r, KMOD_NONE): 'Rectangle(Color("white"), pos=pygame.mouse.get_pos())',
                          (K_t, KMOD_NONE): 'Text("Text", pos=pygame.mouse.get_pos())',
                          (K_o, KMOD_NONE): 'self.scene.print_nodes()',

                          (K_x, KMOD_LMETA): 'print("cmd+X")',
                          (K_x, KMOD_LALT): 'print("alt+X")',
                          (K_x, KMOD_LCTRL): 'print("ctrl+X")',
                          (K_x, KMOD_LMETA + KMOD_LSHIFT): 'print("cmd+shift+X")',
                          (K_x, KMOD_LMETA + KMOD_LALT): 'print("cmd+alt+X")',
                          (K_x, KMOD_LMETA + KMOD_LALT + KMOD_LSHIFT): 'print("cmd+alt+shift+X")',
                          }

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

                elif event.type == KEYDOWN:
                    self.do_shortcut(event)

                # Send the event to the scene
                App.scene.do_event(event)
                App.scene.update()

            App.scene.draw()

        pygame.quit()

    def next_scene(self):
        """Switch to the next scene."""
        i = App.scenes.index(App.scene)
        n = len(App.scenes)
        i = (i+1) % n
        App.scene = App.scenes[i]
        App.scene.enter()

    def do_shortcut(self, event):
        """Find the key/mod combination in the dictionary and execute the cmd."""
        k = event.key
        m = event.mod
        if (k, m) in self.shortcuts:
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

    def toggle_fullscreen(self):
        """Toggle between full screen and windowed screen."""
        self.flags ^= FULLSCREEN
        pygame.display.set_mode((0, 0), self.flags)

    def toggle_resizable(self):
        """Toggle between resizable and fixed-size window."""
        self.flags ^= RESIZABLE
        pygame.display.set_mode(self.rect.size, self.flags)

    def toggle_frame(self):
        """Toggle between frame and noframe window."""
        self.flags ^= NOFRAME
        pygame.display.set_mode(self.rect.size, self.flags)


class Scene:
    """Create a new scene and initialize the node options."""
    id = 0
    options = { 'bg': Color('gray'), 
                'caption': 'Pygame',
                'file': ''}

    def __init__(self, *args, **options):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self

        # Reset Node options to default
        Node.options = Node.options0.copy()

        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.selection = []

        # Update class options from current **options argument
        Scene.options.update(options)

        # Add/update instance options from class options
        self.__dict__.update(Scene.options)

        self.rect = App.screen.get_rect()
        if self.file != '':
            self.img = pygame.image.load(self.file)    
            self.img = pygame.transform.smoothscale(self.img, self.rect.size)
        else:
            self.img = pygame.Surface(self.rect.size)
            self.img.fill(self.bg)

        self.enter()

    def enter(self):
        """Enter a scene."""
        pygame.display.set_caption(self.caption)
    
    def update(self):
        """Update the nodes in a scene."""
        pass

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.blit(self.img, self.rect)

        for node in self.nodes:
            node.draw()
        pygame.display.flip()

    def do_event(self, event):
        """Handle the events of the scene."""
        mods = pygame.key.get_mods()
        if mods & KMOD_CTRL:
            print(event)

        if event.type == KEYDOWN:
            if event.key == K_TAB:
                self.select_next()
        
        if event.type == MOUSEBUTTONDOWN:
            if not mods & KMOD_SHIFT:  
                self.selection = []
            for node in self.nodes:
                node.selected = False
                if node.rect.collidepoint(event.pos):
                    self.selection.append(node)
            for node in self.selection:
                node.selected = True

        elif event.type == MOUSEMOTION:
            pass

        elif event.type == MOUSEBUTTONUP:
            pass
        
        for node in self.selection:
            node.do_event(event)
        
    def print_nodes(self):
        for node in self.nodes:
            print(node)

    def select_next(self, d=1):
        """Move to the next object in the node list."""
        if len(self.selection) > 0:
            node = self.selection[0]
            i = self.nodes.index(node)
            n = len(self.nodes)
            i = (i+d) % n
            print(i, n)
            self.selection = [self.nodes[i]]
            for node in self.nodes:
                node.selected = False
            self.nodes[i].selected = True

    def __str__(self):
        return 'Scene {}'.format(self.id)


class Node:
    """Create a node for embedded objects."""
   # initial options for nodes in a new scene
    options0 = {'pos': (20, 20),
                'size': (100, 40),
                'dir': (0, 1),
                'gap': (10, 10),
                'color': Color('red'),
                'd': 1,
                'id': 0,
                'selected': False,
                'visible': True}
    options = {}

    # key direction vectors
    dirs = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1)}
    
    # selection color and line thickness
    sel_color = Color('blue')
    sel_thick = 1

    def __init__(self, **options):
        Node.options.update(options)

        # create node attributes from class options
        self.__dict__ = Node.options.copy()
        self.parent = App.scene
        self.time = pygame.time.get_ticks()
        
        # update the position
        if self.id > 0 and 'pos' not in options: 
            x = self.pos[0] + self.dir[0] * (self.size[0] + self.gap[0])
            y = self.pos[1] + self.dir[1] * (self.size[1] + self.gap[1])
            self.pos = x, y
            Node.options['pos'] = x, y
        
        Node.options['id'] += 1

        self.rect = Rect(*self.pos, *self.size)

        font = pygame.font.Font(None, 14)
        self.label_img = font.render(str(self), True, self.color)

        # Append the node to the current window
        App.scene.nodes.append(self)

    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            # detect double click
            t = pygame.time.get_ticks()
            if t - self.time < 200:
                self.double_click()
            self.time = t

        if event.type == MOUSEMOTION: 
            # move the node if selected + cmd key
            if self.selected:
                if pygame.key.get_mods() & KMOD_META:
                    screen_rect =  App.screen.get_rect()
                    if screen_rect.contains(self.rect.move(event.rel)):
                        self.rect.move_ip(event.rel)
        
        elif event.type == KEYDOWN:
            if event.key in Node.dirs:
                v = Node.dirs[event.key]
                self.rect.move_ip(v)

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, self.d)
        if self.selected:
            pygame.draw.rect(App.screen, Node.sel_color, self.rect, Node.sel_thick)

            r0 = Rect(self.rect.topleft, (5, 5))
            pygame.draw.rect(App.screen, Node.sel_color, r0)

            r0 = Rect(self.rect.topright, (5, 5))
            pygame.draw.rect(App.screen, Node.sel_color, r0)

        App.screen.blit(self.label_img, self.rect)
    
    def double_click(self):
        print('double-click in', self)

    def __str__(self):
        return self.__class__.__name__ + str(self.id)
            

class Text(Node):
    """Create a text object which knows how to draw itself."""

    fontname = None
    fontsize = 36
    fontcolor = Color('black')
    background = None
    italic = False
    bold = False
    underline = False

    def __init__(self, text, cmd='', **options):
        """Instantiate and render the text object."""
        super().__init__(**options)
        self.__dict__.update(Text.options)
        
        self.text = text
        self.cmd = cmd
    
        self.set_font()
        self.render()
        Node.options['size'] = self.rect.size

    def set_font(self):
        """Set the font and its properties."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor, self.background)
        self.rect.size = self.img.get_size()

    def do_event(self, event):
        super().do_event(event)
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.selected = False
                exec(self.cmd)
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.render()

    def draw(self):
        """Draw the text surface on the screen."""
        App.screen.blit(self.img, self.rect)
        Node.draw(self)

class TextList(Node):
  
    def __init__(self, items, **options):
        super().__init__(**options)

        self.font = pygame.font.Font(None, 24)
        w, h = self.font.size('abc')
        n = len(items)
        self.img = pygame.Surface((100, n * h))
        self.rect.size = self.img.get_size()
        
        self.img.fill(Color('white'))
        for i in range(n):
            text = self.font.render(items[i], True, Color('black'))
            w, h = text.get_size()
            self.img.blit(text, ((100-w)/2, i*h))
            print(i)

    def draw(self):
        App.screen.blit(self.img, self.rect)


class Rectangle(Node):
    """Draw a rectangle on the screen."""

    def __init__(self, color, color2=(0, 0, 0), thick=0, **options):
        super().__init__(**options)
        self.color = color
        self.color2 = color2
        self.thick = thick

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, 0)
        pygame.draw.rect(App.screen, self.color2, self.rect, self.thick)
        Node.draw(self)

class Ellipse(Node):
    """Draw an ellipse on the screen."""

    def __init__(self, color, color2=(0, 0, 0), thick=1, **options):
        super().__init__(**options)
        self.color = color
        self.color2 = color2
        self.thick = thick

    def draw(self):
        pygame.draw.ellipse(App.screen, self.color, self.rect, 0)
        pygame.draw.ellipse(App.screen, self.color2, self.rect, self.thick)
        Node.draw(self)

class Button(Text):
    """Create a button object with command.""" 
    button_color = Color('blue')
    size = (160, 40)
    border = 2
    border_color = Color('magenta')

    def __init__(self, text, cmd='',  **options):
        super().__init__(text, **options)
        self.__dict__.update(Button.options)

        self.cmd = cmd
        self.rect.size = 160, 40
        self.button_color = Color('green')

        self.text_rect = self.img.get_rect()
        self.text_rect.center = self.rect.center

    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            exec(self.cmd)

    def draw(self):
        pygame.draw.rect(App.screen, self.button_color, self.rect)
        pygame.draw.rect(App.screen, self.border_color, self.rect, self.border)
        
        App.screen.blit(self.img, self.text_rect)
        Node.draw(self)


if __name__ == '__main__':
    app = App()
    Scene(caption='Scene 0')
    Text('Scene 0')
    Ellipse(Color('pink'), Color('magenta'), 10)
    Rectangle(Color('red'), Color('blue'), 10)

    Scene(bg=Color('cyan'))
    Text('Scene 1')
    Button('Scene', cmd='print(App.scene)')
    Button('Button 1', cmd='print(123)')
    TextList(['Amsterdam', 'Berlin', 'Calcutta'])
    TextList(['Charlie', 'Daniel', 'Tim', 'Jack'], pos=(200, 20))
    
    app.run()