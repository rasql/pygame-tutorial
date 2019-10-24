"""
App
- there is only one App object
- an App has multiple scenes (App.scenes)
- there one current scene (App.scene)

Scene
- a scene has multiple objects (Scene.nodes)
- objects are ordered (the last displayed last)
- the object which is clicked becomes active
- the active object becomes the top object
- the active oject has focus (Scene.focus)
- TAB and shift-TAB select the next object

Node objects
- objects have default position and size (pos, size)
- objects are automatically placed at creation (dir, gap)
- objects inherit options (color, size, ...) from the previous object
- ARROW keys move the active object

A Node object has the following properties
- clickable: mouse-click has effect
- editable: text can be edited
- movable: can be moved (mouse, arrow-keys)
- visible: is drawn
- outlined: an outline is drawn
- acitve: 
"""

import pygame
from pygame.locals import *
import copy
import os
import sys
import inspect
import numpy as np

DBG_EVENTS = 1
DBG_LABELS = 2
DBG_OUTLINE = 4

class App:
    """Create a single-window app with multiple scenes having multiple objects."""
    scenes = []     # scene list
    scene = None    # current scene
    screen = None   # main display window
    running = True  # the app is running
    selection = None # list of selected objects (cut/copy/paste)
    debug = DBG_LABELS + DBG_OUTLINE

    def __init__(self, size=(640, 240), shortcuts={}):
        """Initialize pygame and the application."""
        pygame.init()
        self.flags = 0  # RESIZABLE, FULLSCREEN, NOFRAME
        self.rect = Rect(0, 0, *size)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.root = self

        self.shortcuts = {(K_ESCAPE, KMOD_NONE): 'App.running=False',
                          (K_q, KMOD_LMETA): 'App.running=False',
                          (K_f, KMOD_LMETA): 'self.toggle_fullscreen()',
                          (K_r, KMOD_LMETA): 'self.toggle_resizable()',
                          (K_g, KMOD_LMETA): 'self.toggle_frame()',
                          
                          (K_h, KMOD_LMETA): 'pygame.display.iconify()',
                          (K_p, KMOD_LMETA): 'self.capture()',
                          (K_s, KMOD_LMETA): 'self.next_scene()',

                          (K_e, KMOD_LCTRL): 'Ellipse(Color("green"), pos=pygame.mouse.get_pos())',
                          (K_n, KMOD_LCTRL): 'Node(pos=pygame.mouse.get_pos())',
                          (K_r, KMOD_LCTRL): 'Rectangle(Color("white"), pos=pygame.mouse.get_pos())',
                          (K_t, KMOD_LCTRL): 'Text(pos=pygame.mouse.get_pos())',

                          (K_x, KMOD_LMETA): 'print("cmd+X")',
                          (K_x, KMOD_LALT): 'print("alt+X")',
                          (K_x, KMOD_LCTRL): 'print("ctrl+X")',
                          (K_x, KMOD_LMETA + KMOD_LSHIFT): 'print("cmd+shift+X")',
                          (K_x, KMOD_LMETA + KMOD_LALT): 'print("cmd+alt+X")',
                          (K_x, KMOD_LMETA + KMOD_LALT + KMOD_LSHIFT): 'print("cmd+alt+shift+X")',
                         
                          (K_x, KMOD_LMETA): 'App.scene.cut()',
                          (K_c, KMOD_LMETA): 'App.scene.copy()',
                          (K_v, KMOD_LMETA): 'App.scene.paste()',

                          (K_e, KMOD_LMETA): 'App.debug ^= DBG_EVENTS',
                          (K_l, KMOD_LMETA): 'App.debug ^= DBG_LABELS',
                          (K_o, KMOD_LMETA): 'App.debug ^= DBG_OUTLINE',

                          (K_d, KMOD_LMETA): 'App.scene.focus.debug()',
                          
                          }
        self.shortcuts.update(shortcuts)

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

    def __str__(self):
        return self.__class__.__name__

class Scene:
    """Create a new scene and initialize the node options."""
    options = { 'id': 0,
                'bg': Color('gray'), 
                'caption': 'Pygame',
                'file': '',
                'focus': None,
                }

    def __init__(self, **options):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        self.nodes = []

        # Reset Node options to default
        Node.options = Node.options0.copy()

        # Set the instance id and increment the class id
        self.selection = []

        # Update class options from current **options argument
        Scene.options.update(options)

        # Add/update instance options from class options
        self.__dict__.update(Scene.options)
        Scene.options['id'] += 1

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
        if App.debug & 1:
            print(event)

        if event.type == KEYDOWN:
            if event.key == K_TAB:
                self.next_focus()
        
        if event.type == MOUSEBUTTONDOWN:
            self.focus = None
            for node in self.nodes:
                node.selected = False
                if node.rect.collidepoint(event.pos):
                    self.focus = node

                    # place node on top
                    self.nodes.remove(node)
                    self.nodes.append(node)

        elif event.type == MOUSEMOTION:
            pass

        elif event.type == MOUSEBUTTONUP:
            pass
        
        if self.focus != None:
            self.focus.do_event(event)

    def next_focus(self, d=1):
        """Advance focus to next node."""
        if self.focus == None:
            self.focus = self.nodes[0]
        else:
            i = self.nodes.index(self.focus)
            n = len(self.nodes)
            i = (i+d) % n
            self.focus = self.nodes[i]

    def cut(self):
        """Cuts the selected objects and places them in App.selection."""
        print('cut')
        App.selection = self.selection
        for obj in self.selection:
            print('remove', obj)
            self.children.remove(obj)
        self.selection = []

    def copy(self):
        """Copies the selected objects and places them in App.selection."""
        print('copy')
        App.selection = self.selection

    def paste(self):
        """Pastes the objects from App.selection."""
        print('paste')
        for obj in App.selection:
            obj2 = eval(type(obj).__name__+'()')
            obj2.rect = obj.rect.copy()
            obj2.rect.topleft = pygame.mouse.get_pos()
            obj2.__dict__.update(obj.__dict__)
            self.children.append(obj)

    def __str__(self):
        return 'Scene{}'.format(self.id)


class Node:
    """Create a node for embedded objects."""
   # initial options for nodes in a new scene
    options0 = {'pos': (20, 20),
                'size': (100, 40),
                'dir': (0, 1),
                'gap': (10, 10),

                'id': 0,
                'file': '',
                'bg': None,
                'border_thick': 0,
                'border_col': None,
                'img': None,
                'time': 0,  # for double-click

                'visible': True,
                'movable': True,
                'resizable': True,
                }

    # current options dictionary for each node
    options = {}
    resize = False

    # color and size/thickness
    label = Color('red'), 14
    outline = Color('red'), 1
    focus = Color('blue'), 1
    selection = Color('magenta'), 1
    dbl_click_time = 200

    # key direction vectors
    dirs = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1)}

    def __init__(self, **options):
        # update current class options
        Node.options.update(options)

        # create instance attributes from current class options
        self.__dict__ = Node.options.copy()
        
        # update the position
        if self.id > 0 and 'pos' not in options: 
            x = self.pos[0] + self.dir[0] * (self.size[0] + self.gap[0])
            y = self.pos[1] + self.dir[1] * (self.size[1] + self.gap[1])
            self.pos = x, y
            Node.options['pos'] = x, y
        
        Node.options['id'] += 1

        self.rect = Rect(*self.pos, *self.size)
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
        App.scene.nodes.append(self)

        # create node label
        font = pygame.font.Font(None, Node.label[1])
        self.label_img = font.render(str(self), True, Node.label[0])

        if self.file != '':
            self.img0 = pygame.image.load(self.file)    
            self.img = pygame.transform.smoothscale(self.img0, self.rect.size)
        else:
            self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
            if self.bg == None:
                self.img.fill((0, 0, 0, 0))
            else:
                self.img.fill(self.bg)
            if self.border_thick > 0:
                pygame.draw.rect(self.img, self.border_col, Rect((0, 0), self.rect.size), self.border_thick)

    def do_event(self, event):
        mods = pygame.key.get_mods()

        if event.type == MOUSEBUTTONDOWN:
            # detect double click
            t = pygame.time.get_ticks()
            if t - self.time < Node.dbl_click_time:
                self.double_click()
            self.time = t

            # click in resize button
            r = Rect(0, 0, 7, 7)
            r.bottomright = self.rect.bottomright
            if r.collidepoint(event.pos) and self.resizable:
                Node.resize = True

        elif event.type == MOUSEMOTION: 
            # resize the node
            if Node.resize:
                dx, dy = event.rel
                if mods & KMOD_LALT:
                    self.rect.inflate_ip(2*dx, 2*dy)
                else:
                    self.rect.width += dx
                    self.rect.height += dy
                if self.file != '':
                    self.img = pygame.transform.smoothscale(self.img0, self.rect.size)
                
            if self == App.scene.focus and self.movable:
                if mods & KMOD_META:
                    screen_rect =  App.screen.get_rect()
                    if screen_rect.contains(self.rect.move(event.rel)):
                        self.rect.move_ip(event.rel)

        elif event.type == MOUSEBUTTONUP:
            Node.resize = False
        
        elif event.type == KEYDOWN:
            if event.key in Node.dirs:
                dx, dy = Node.dirs[event.key]
                if mods & KMOD_ALT:
                    self.rect.move_ip(10*dx, 10*dy)
                else:
                    self.rect.move_ip(dx, dy)

    def update(self):
        pass

    def draw(self):
        """Draw the node and its children."""
        if self.visible:
            App.screen.blit(self.img, self.rect)
        
        if App.debug & DBG_OUTLINE:
            pygame.draw.rect(App.screen, Node.outline[0], self.rect, Node.outline[1])

        if App.debug & DBG_LABELS:
            App.screen.blit(self.label_img, self.rect)

        if self == App.scene.focus:
            pygame.draw.rect(App.screen, Node.focus[0], self.rect, Node.focus[1])
            if self.resizable:
                r = Rect(0, 0, 7, 7)
                r.bottomright = self.rect.bottomright
                pygame.draw.rect(App.screen, Node.focus[0], r, Node.focus[1])
    
    def double_click(self):
        print('double-click in', self)

    def debug(self):
        """Print all node options."""
        print('-'*30)
        print(self)
        for k, v in self.__dict__.items():
            print(k, '=', v)

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

    def __init__(self, text='Text', cmd='', **options):
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

    def draw(self):
        """Draw the text surface on the screen."""
        App.screen.blit(self.img, self.rect)
        Node.draw(self)

class TextEdit(Text):
    """Text with movable cursor to edit the text."""
    def __init__(self, text='TextEdit', cmd='', **options):
        super().__init__(text=text, cmd=cmd, **options)

        self.cursor_pos = len(self.text)
        self.cursor_img = pygame.Surface((2, self.rect.height))
        self.cursor_img.fill(Color('red'))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_rect.topleft = self.rect.topright

    def do_event(self, event):
        """Move cursor left/right, add/backspace text."""
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                App.scene.focus = None
                exec(self.cmd)
            elif event.key == K_BACKSPACE:
                t0 = self.text[:self.cursor_pos-1]
                t1 = self.text[self.cursor_pos:]
                self.text = t0 + t1
                self.cursor_pos = max(0, self.cursor_pos-1)
            elif event.key in (K_TAB, K_UP, K_DOWN):
                pass
            elif event.key == K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos-1)
                
            elif event.key == K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos+1)

            elif not (event.mod & KMOD_META + KMOD_CTRL):
                t0 = self.text[:self.cursor_pos]
                t1 = self.text[self.cursor_pos:]
                self.text = t0 + event.unicode + t1
                self.cursor_pos += 1

            self.render()

        if event.type == MOUSEBUTTONDOWN:
            for i in range(len(self.text+' ')):
                txt = self.text[:i]
                w, h = self.font.size(self.text[:i])
                if w+3 > (event.pos[0] - self.rect.left):
                    break
            self.cursor_pos = i

        w, h = self.font.size(self.text[:self.cursor_pos])
        self.cursor_rect = self.rect.move((w, 0))


    def draw(self):
        Node.draw(self)
        if self == App.scene.focus:
            t = pygame.time.get_ticks()
            if (t % 600) > 300:
                App.screen.blit(self.cursor_img, self.cursor_rect)

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

    def draw(self):
        App.screen.blit(self.img, self.rect)
        Node.draw(self)

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

    def __init__(self, text='Button', cmd='',  **options):
        super().__init__(text, **options)
        #self.__dict__.update(Button.options)

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
        #Node.draw(self)

if __name__ == '__main__':
    app = App()
    Scene(caption='Scene 0')
    Text('Scene 0')
    Ellipse(Color('pink'), Color('magenta'), 10)
    Rectangle(Color('red'), Color('blue'), 10)

    Scene(caption='Scene 1', bg=Color('cyan'))
    Text('Scene 1')
    # Button('Scene', cmd='print(App.scene)')
    # Button('Button 1', cmd='print(123)')
    TextList(['Amsterdam', 'Berlin', 'Calcutta'])
    TextList(['Charlie', 'Daniel', 'Tim', 'Jack'], pos=(200, 20))

    Scene(caption='visible, outlined, movable, resizable')
    Node(visible=False)
    Node(visible=True, outlined=False)
    Node(outlined=True, movable=False)
    Node(resizable=False)

    app.run()