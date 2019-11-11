"""
App

- there is only one App object
- an app has multiple scenes (App.scenes)
- an app has one current scene (App.scene)
- an app has one window to draw in (App.screen)

Scene

- a scene has multiple nodes (App.scene.nodes)
- nodes are ordered: the last in the list is displayed last
- the node which is clicked becomes active
- the active node becomes the top node
- the active node has focus (App.scene.focus)
- TAB and shift-TAB select the next node

Node (object)

- nodes have default position and size (pos, size)
- nodes are automatically placed at creation (dir, gap)
- nodes inherit options (color, size, ...) from the previous object
- ARROW keys move the active object

A Node object has the following properties

- clickable: mouse-click has effect
- movable: can be moved (mouse, arrow-keys)
- visible: is drawn
- has focus

Debug

- print events to console (cmd+E)
- display node label (cmd+L)
- display outline (cmd+O)
"""

import copy
import inspect
import os
import sys

import numpy as np
import pygame
from pygame.locals import *

DBG_EVENTS = 1
DBG_LABELS = 2
DBG_OUTLINE = 4

class App:
    """Create a single-window app with multiple scenes having multiple objects."""
    scenes = []     # scene list
    scene = None    # current scene
    screen = None   # main display window
    running = True  # the app is running
    focus = None    # current object for cut/copy/paste
    selection = None # list of selected objects (cut/copy/paste)
    root = None
    debug = DBG_LABELS + DBG_OUTLINE

    def __init__(self, size=(640, 240), shortcuts={}):
        """Initialize pygame and the application."""
        pygame.init()
        self.flags = 0  # RESIZABLE, FULLSCREEN, NOFRAME
        self.rect = Rect(0, 0, *size)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.root = self

        self.shortcuts = {
            (K_ESCAPE, KMOD_NONE): 'App.running=False',
            (K_q, KMOD_LMETA): 'App.running=False',
            (K_f, KMOD_LMETA): 'self.toggle_fullscreen()',
            (K_r, KMOD_LMETA): 'self.toggle_resizable()',
            (K_g, KMOD_LMETA): 'self.toggle_frame()',
            
            (K_h, KMOD_LMETA): 'pygame.display.iconify()',
            (K_p, KMOD_LMETA): 'self.capture()',
            (K_s, KMOD_LMETA): 'self.next_scene()',
            (K_s, KMOD_LMETA+KMOD_LSHIFT): 'self.next_scene(-1)',
            (K_TAB, KMOD_NONE): 'App.scene.next_focus()',
            (K_TAB, KMOD_LSHIFT): 'App.scene.next_focus(-1)',

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

            (K_d, KMOD_LMETA): 'App.scene.debug()',
            }
        # update shortcuts with the argument
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

    def multi_click(self):
        """Detect double and triple clicks"""

    def next_scene(self, d=1):
        """Switch to the next scene."""
        i = App.scenes.index(App.scene)
        n = len(App.scenes)
        i = (i+d) % n
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
                'bg': Color('gray'),  # background color
                'caption': 'Pygame',  # window caption
                'img_folder': '',     # image folder
                'snd_folder': '',     # sound folder
                'file': '',  # background image file
                'focus': None,  # currently active node
                'status': '',
                'shortcuts': {},

                'selecting': False,
                'selection': [],
                'selection_rect': Rect(0, 0, 0, 0),
                'selection_surround': False,
                'moving': False,
                }
    selection_border = (Color('cyan'), 1)
    status_line = (Color('black'), Color('gray'), 20)  # col, bg, size

    def __init__(self, remember=True, **options):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        self.nodes = []

        # Reset Node options to default
        Node.options = Node.options0.copy()

        # update existing Scene options, without adding new ones
        if remember:
            for k in options:
                if k in Scene.options:
                    Scene.options[k] = options[k]
                else:
                    raise TypeError(f"'{k}' is an invalid keyword argument for Scene()")

        # Add/update instance options from class options
        self.__dict__.update(Scene.options)
        if not remember:
            self.__dict__.update(options)
        Scene.options['id'] += 1

        self.rect = App.screen.get_rect()
        if self.file != '':
            self.load_img(self.file)
        else:
            self.img = pygame.Surface(self.rect.size)
            self.img.fill(self.bg)

        self.render_status()
        self.enter()

    def load_img(self, file): 
        """Load the background image."""
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
        path = os.path.join(path, self.img_folder, file)       
        self.img = pygame.image.load(path)    
        self.img = pygame.transform.smoothscale(self.img, self.rect.size)
     
    def enter(self):
        """Enter a scene."""
        pygame.display.set_caption(self.caption)
    
    def update(self):
        """Update the nodes in a scene."""
        for node in self.nodes:
            node.update()

    def set_status(self, txt):
        """Set status text and render it."""
        self.status = txt
        self.render_status()

    def render_status(self):
        """Render the status text."""
        col, bg, size = Scene.status_line
        font = pygame.font.Font(None, size)
        self.status_img0 = font.render(self.status, True, col, bg)

        w, h = font.size(self.status)
        self.status_rect = Rect(0, 0, self.rect.width, h)
        self.status_rect.bottomleft = self.rect.bottomleft

        self.status_img = pygame.Surface((self.rect.width, h), flags=SRCALPHA)
        if bg != None:
            self.status_img.fill(bg)
        self.status_img.blit(self.status_img0, (0, 0))

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.blit(self.img, self.rect)
        for node in self.nodes:
            node.draw()
        
        col, d = Scene.selection_border
        pygame.draw.rect(App.screen, col, self.selection_rect, d)
        App.screen.blit(self.status_img, self.status_rect)
        
        pygame.display.flip()

    def do_event(self, event):
        """Handle the events of the scene."""
        mods = pygame.key.get_mods()
        if App.debug & DBG_EVENTS:
            print(event)
            self.set_status(str(event))

        if event.type == KEYDOWN:
            k = event.key
            m = event.mod
            if (k, m) in self.shortcuts:
                exec(self.shortcuts[k, m])

        if event.type == MOUSEBUTTONDOWN:
            if self.selection_rect.collidepoint(event.pos):
                self.moving = True
            else:
                self.focus = None
                for node in reversed(self.nodes):
                    if node.rect.collidepoint(event.pos):
                        self.focus = node
                        self.set_status(str(node))

                        # place node on top
                        self.nodes.remove(node)
                        self.nodes.append(node)
                        break
                if self.focus == None:
                    self.set_status(str(self))
                    self.selecting = True
                    self.selection_rect = Rect(event.pos, (0, 0))

        elif event.type == MOUSEMOTION:
            if self.selecting:
                self.selection_rect.width += event.rel[0]
                self.selection_rect.height += event.rel[1]
            if self.moving:
                for node in self.selection:
                    node.rect.move_ip(event.rel)
                    node.label_rect.move_ip(event.rel)
                self.selection_rect.move_ip(event.rel)

        elif event.type == MOUSEBUTTONUP:
            self.selection_rect.normalize()
            self.selecting = False
            self.moving = False
            self.selection = []
            for node in self.nodes:
                if self.selection_surround:
                    if self.selection_rect.contains(node.rect):
                        self.selection.append(node)
                else:
                    if self.selection_rect.colliderect(node.rect):
                        self.selection.append(node)

            if len(self.selection) > 0:
                self.selection_rect = self.selection[0].rect.copy()
                for x in self.selection[1:]:
                    self.selection_rect.union_ip(x.rect)
                self.selection_rect.inflate_ip((4, 4))
        
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
        App.focus = self.focus
        self.nodes.remove(self.focus)
        self.focus = None

    def copy(self):
        """Copies the selected objects and places them in App.selection."""
        App.focus = self.focus

    def paste(self):
        """Pastes the objects from App.selection."""
        print('paste')
        obj = App.focus
        obj2 = eval(type(obj).__name__+'()')
        obj2.rect = obj.rect.copy()
        #®obj2.__dict__.update(obj.__dict__)
        obj2.rect.topleft = pygame.mouse.get_pos()
        obj2.label_rect.bottomleft = pygame.mouse.get_pos()
        self.nodes.append(obj2)

    def debug(self):
        """Print all scene/node options."""
        obj = self.focus if self.focus else self
        print('===', obj, '===')
        for k, v in obj.__dict__.items():
            print(k, '=', v)

    def __str__(self):
        return f'Scene{self.id}'


class Node:
    """Create a node object with automatic position and inherited size."""
   # initial options for nodes in a new scene
    options0 = {'pos': (20, 20),
                'size': (100, 40),
                'dir': (0, 1),
                'gap': (10, 10),

                'id': 0,
                'file': '',
                'bg': None,
                'img': None,
                'cmd': '',  # command string

                'visible': True,
                'movable': True,
                'resizable': True,
                }

    # current options dictionary for each node
    options = {}
    resizing = False
    moving = False

    # color and size/thickness
    label = Color('red'), 14
    outline = Color('red'), 1
    focus = Color('blue'), 1
    selection = Color('green'), 2
    dbl_click_time = 300

    # key direction vectors
    dirs = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1)}

    def __init__(self, **options):
        # update existing Node options, without adding new ones
        for k in options:
            if k in Node.options:
                Node.options[k] = options[k]

        # create instance attributes from current class options
        self.__dict__ = Node.options.copy()
        Node.options['id'] += 1
        self.t0 = 0
        self.t1 = 0
        
        self.calculate_pos(options)
        self.rect = Rect(*self.pos, *self.size)
        
        App.scene.nodes.append(self)
        self.render_label()

        self.create_img()
        self.color_img()
        if self.file != '':
            self.load_img()

    def create_img(self):
        """Create the image surface, and the original img0."""
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
        self.img0 = self.img.copy()

    def color_img(self):
        """Add background color to the image."""
        if self.bg == None:
            self.img.fill((0, 0, 0, 0))
        else:
            self.img.fill(self.bg)
        self.img0 = self.img.copy()
    
    def set_background(self, img):
        """Set background color or transparency."""
        if self.bg == None:
            img.fill((0, 0, 0, 0))
        else:
            img.fill(self.bg)
        
    def load_img(self):
        """Load the image file."""
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
        path = os.path.join(path, self.file)
        
        img = pygame.image.load(path)
        self.img0 = pygame.Surface(img.get_size(), flags=SRCALPHA)
        self.set_background(self.img0)
        self.img0.blit(img, (0, 0))

        self.img = pygame.transform.smoothscale(self.img0, self.rect.size)

    def calculate_pos(self, options):
        """Calculate the next node position."""
        if self.id > 0 and 'pos' not in options: 
            last = App.scene.nodes[-1].rect
            x = self.pos[0] + self.dir[0] * (last.size[0] + self.gap[0])
            y = self.pos[1] + self.dir[1] * (last.size[1] + self.gap[1])
            self.pos = x, y
            Node.options['pos'] = x, y
   
    def render_label(self):
        """Create and render the node label."""
        col, size = Node.label
        font = pygame.font.Font(None, size)
        self.label_img = font.render(str(self), True, col)
        self.label_rect = self.label_img.get_rect()
        self.label_rect.bottomleft = self.rect.topleft

    def do_event(self, event):
        """React to events happening for focus node."""
        mods = pygame.key.get_mods()

        if event.type == MOUSEBUTTONDOWN:
            # detect double click
            t = pygame.time.get_ticks()
            if t - self.t1 < Node.dbl_click_time:
                self.triple_click()
            elif t- self.t0 < Node.dbl_click_time:
                self.double_click()
            self.t1 = self.t0
            self.t0 = t

            # click in resize button
            r = Rect(0, 0, 7, 7)
            r.bottomright = self.rect.bottomright
            if r.collidepoint(event.pos) and self.resizable:
                Node.resizing = True
            else:
                Node.moving = True

        elif event.type == MOUSEMOTION: 
            # resize the node
            if Node.resizing:
                dx, dy = event.rel
                if mods & KMOD_LALT:
                    self.rect.inflate_ip(2*dx, 2*dy)
                else:
                    self.rect.width += dx
                    self.rect.height += dy
                self.rect.normalize()
                #if self.file != '':
                if isinstance(self, (Ellipse, Rectangle)):
                    self.render()
                else:
                    self.img = pygame.transform.smoothscale(self.img0, self.rect.size)
                
            if Node.moving and self.movable:
                screen_rect =  App.screen.get_rect()
                if screen_rect.contains(self.rect.move(event.rel)):
                    self.rect.move_ip(event.rel)
                    self.label_rect.move_ip(event.rel)

        elif event.type == MOUSEBUTTONUP:
            Node.resizing = False
            Node.moving = False
        
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
        """Draw the node and optionally the outline, label and focus."""
        if self.visible:
            App.screen.blit(self.img, self.rect)
        
        if App.debug & DBG_OUTLINE:
            pygame.draw.rect(App.screen, Node.outline[0], self.rect, Node.outline[1])

        if App.debug & DBG_LABELS:
            App.screen.blit(self.label_img, self.label_rect)

        if self in App.scene.selection:
            col, d = Node.selection
            pygame.draw.rect(App.screen, col, self.rect, d)
    
        if self == App.scene.focus:
            pygame.draw.rect(App.screen, Node.focus[0], self.rect, Node.focus[1])
            if self.resizable:
                r = Rect(0, 0, 7, 7)
                r.bottomright = self.rect.bottomright
                pygame.draw.rect(App.screen, Node.focus[0], r, Node.focus[1])
    
    def double_click(self):
        App.scene.set_status(f'double-click in {self}')
        print('double-click in', self)

    def triple_click(self):
        App.scene.set_status(f'triple-click in {self}')
        print('triple-click in', self)

    def __str__(self):
        return self.__class__.__name__ + str(self.id)


class Text(Node):
    """Create a text object which knows how to draw itself."""

    options = { 'fontname': None,
                'fontsize': 36,
                'fontcolor': Color('black'),
                'fontbg': None,

                'italic': False,
                'bold': False,
                'underline': False,
                'autosize': True,

                'h_align': 0,
                'v_align': 0,
    }

    def __init__(self, text='Text', cmd='', **options):
        """Instantiate and render the text object."""
        super().__init__(**options)

        # update existing Text options, without adding new ones
        for k in options:
            if k in Text.options:
                Text.options[k] = options[k]

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
        if self.autosize:
            self.size = self.font.size(self.text)
            self.rect.size = self.size

        self.img0 = pygame.Surface(self.size, flags=SRCALPHA)
        if self.bg != None:
            self.img0.fill(self.bg)
        self.text_img = self.font.render(self.text, True, self.fontcolor, self.fontbg)
        self.text_rect = self.text_img.get_rect()
        
        w, h = self.rect.size
        w0, h0 = self.text_img.get_size()
        
        if self.h_align == 0:
            x = 0
        elif self.h_align == 1:
            x = (w-w0)//2
        else:
            x = w-w0

        if self.v_align == 0:
            y = 0
        elif self.v_align == 1:
            y = (h-h0)//2
        else:
            y = h-h0
        
        self.rect.size = w, h
        self.img0.blit(self.text_img, (x, y))
        self.img = self.img0.copy()

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
        #Node.do_event(self, event)
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
  
    def __init__(self, items, i=0, **options):
        super().__init__(**options)

        self.items = items
        self.i = i
        self.n = len(items)

        
        self.font = pygame.font.Font(None, 24)
        self.h = self.font.size('')[1]
        self.img_sel = pygame.Surface((100, self.h))
        self.img_sel.fill(Color('gray'))
        self.render()
        
    def render(self):
        self.item = self.items[self.i]
        self.img0 = pygame.Surface((100, self.n * self.h))
        self.rect.size = self.img0.get_size()
        self.img0.fill(Color('white'))
        self.img0.blit(self.img_sel, (0, self.i * self.h))
        for i in range(self.n):
            text = self.font.render(self.items[i], True, Color('black'))
            w, h = text.get_size()
            self.img0.blit(text, ((100-w)/2, i*h))
        self.img = self.img0.copy()

    def draw(self):
        Node.draw(self)

    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            x -= self.rect.left
            y -= self.rect.top
            self.i = y // self.h
            self.render()
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.i = (self.i + 1) % self.n
            elif event.key == K_UP:
                self.i = (self.i - 1) % self.n
            elif event.key == K_RETURN:
                exec(self.cmd)
            self.render()
            
                
    
class TextMenu(Text):
    """Select a text item from an items list."""
    def __init__(self, items, i=0, **options):
        super().__init__(items[i], **options)
        self.items = items
        self.n = len(items)
        self.i = i

    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                #App.scene.focus = None
                exec(self.cmd)
            if event.key == K_RIGHT:
                self.i = (self.i + 1) % self.n
            if event.key == K_LEFT:
                self.i = (self.i - 1) % self.n
            self.text = self.items[self.i]
            self.render()

class InputNum(Text):
    """Input a number."""
    def __init__(self, num=5, min=0, max=10, inc=1, **options):
        self.text = num
        super().__init__(str(num), **options)
        self.min = min
        self.max = max
        self.num = num
        self.inc = inc

    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                exec(self.cmd)
            if event.key in (K_RIGHT, K_UP):
                self.num = min(self.max, self.num + self.inc)
            if event.key in (K_LEFT, K_DOWN):
                self.num = max(self.min, self.num - self.inc)
            self.text = str(self.num)
            self.render()

class Rectangle(Node):
    """Draw a rectangle on the screen."""

    def __init__(self, color=Color('green'), color2=Color('black'), thick=3, **options):
        super().__init__(**options)
        self.color = color
        self.color2 = color2
        self.thick = thick
        self.render()

    def render(self):
        self.img0 = pygame.Surface(self.rect.size, flags=SRCALPHA)
        pygame.draw.rect(self.img0, self.color, Rect(0, 0, *self.rect.size), 0)
        pygame.draw.rect(self.img0, self.color2, Rect(0, 0, *self.rect.size), self.thick)
        self.img = self.img0.copy()


class Ellipse(Node):
    """Draw an ellipse on the screen."""
    options = {'border_col':Color('black'),
               'border_thick':2,
               'color':Color('yellow',
               )}

    def __init__(self, color, color2=(0, 0, 0), thick=1, **options):
        super().__init__(**options)
        self.color = color
        self.color2 = color2
        self.thick = thick
        self.render()   

    def render(self):
        self.img0 = pygame.Surface(self.rect.size, flags=SRCALPHA)
        pygame.draw.ellipse(self.img0, self.color, Rect(0, 0, *self.rect.size), 0)
        pygame.draw.ellipse(self.img0, self.color2, Rect(0, 0, *self.rect.size), self.thick)
        self.img = self.img0.copy()


class Button(Text):
    """Create a button object with command.""" 
    options = { 'border': 2,
                'bg': Color('yellow'),
                'size': (160, 40),
                'autosize': False,
                'v_align': 1,
                'h_align': 1,
        }

    def __init__(self, text='Button', cmd='',  **options):
        print(Button.options)
        super().__init__(text, **Button.options)
        self.cmd = cmd

    def do_event(self, event):
        super().do_event(event)
        if event.type == MOUSEBUTTONDOWN:
            exec(self.cmd)

class Board(Node):
    """Draw a mxn board grid with m lines and n columns.
    m, n    number of cells (row, col)
    i, j    index of cell (row, col)
    dx, dy  size of cell
    Num     numeric matrix
    Num0    initial numeric matrix
    Col     color matrix
    """
    options = {
        'm': 4,
        'n': 4,
        'i': 0,
        'j': 0,
        'dx': 40,
        'dy': 40,
        'selection': [],
        'grid': (Color('black'), 1),  # grid color and thickness
        'selection_col': (Color('green'), 2),  # selection color and thickness
        'focus_col': (Color('red'), 2),  # current focus cell (i, j)
        'images': [None],
        'colors': [Color('white'), Color('gray')],
        'folder': '',
        'drag': False,
        'centered': False,  # grid is centered as in Go
        'keys': '0123456789', # keys which are accepted
    }

    def __init__(self, **options):
        super().__init__(**options)

        # update existing Board options, without adding new ones
        for k in options:
            if k in Board.options:
                Board.options[k] = options[k]

        self.__dict__.update(Board.options)

        # update board size
        self.size = self.n * self.dx, self.m * self.dy
        self.rect.size = self.size
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)

        self.Num = np.zeros((self.m, self.n), dtype='int8')
        self.Num0 = self.Num.copy()
        self.Col = self.Num.copy()

        self.font = pygame.font.Font(None, self.dy)
        self.render()

    def set_Num(self, s):
        """Load Num table from a string."""
        s = s.replace('.', '0')
        lines = s.split()
        m = len(lines)
        n = len(lines[0])
        self.Num = np.zeros((m, n), dtype='int8')
        for i in range(m):
            for j in range(n):
                self.Num[i, j] = int(lines[i][j])
        self.Num0 = self.Num.copy()
        self.render()

    def switch_Num(self, dir):
        i1, j1
        i2 = i + di
        j2 = j + dj
        if 0 < i2 < n:
            tmp = self.Num[i1, j1]
            self.Num[i1, j1] = self.Num[i2, j2]
            self.Num[i2, j2] = tmp

    def set_checkerboard(self):
        self.Col = np.fromfunction(lambda i, j: (i+j)%2, (self.m, self.n), dtype='int8')

    def load_images(self):
        name = type(self).__name__
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
    
        path = os.path.join(path, self.folder)
        dir = os.listdir(path)
        dir.sort()
        
        for file in dir:
            img_path = os.path.join(path, file)
            root, ext = os.path.splitext(img_path)
            if ext in ['.png', '.jpg']:
                img = pygame.image.load(img_path)
                img = pygame.transform.smoothscale(img, (self.dx, self.dy))
                self.images.append(img)

    def render_colors(self):
        """Render the background colors."""
        for i in range(self.m):
            for j in range(self.n):
                rect = self.get_rect(i, j)
                col = self.colors[self.Col[i, j]]
                if col != None:
                    pygame.draw.rect(self.img, col, rect)

    def render_grid(self):
        """Render the grid lines."""
        col = self.grid[0]
        d = self.grid[1]
        x0, y0 = 0, 0
        dx, dy = self.dx, self.dy
        x1, y1 = self.rect.size
        m = self.m+1
        n = self.n+1
        
        if self.centered:
            m, n = m-1, n-1
            x0 += dx//2
            y0 += dy//2
            x1 -= dx//2
            y1 -= dy//2
            
        for i in range(m):
            y = y0 + i * dy
            pygame.draw.line(self.img, col, (x0, y), (x1, y), d)
        for j in range(n):
            x = x0 + j * dx
            pygame.draw.line(self.img, col, (x, y0), (x, y1), d)

    def render_num(self):
        """Draw number."""
        for i in range(self.m):
            for j in range(self.n):
                k = self.Num[i, j]
                if k != 0:
                    img = self.font.render(str(k), True, Color('black'))
                    rect = img.get_rect()
                    rect.center = self.get_rect(i, j).center
                    self.img.blit(img, rect)

    def render_tile(self):
        """Draw number."""
        for i in range(self.m):
            for j in range(self.n):
                k = self.Num[i, j]
                if k != 0:
                    img = self.images[k]
                    rect = img.get_rect()
                    rect.center = self.get_rect(i, j).center
                    self.img.blit(img, rect)

    def render_sel(self):
        col = self.selection_col[0]
        d = self.selection_col[1]      
        for i, j in self.selection:
            pygame.draw.rect(self.img, col, self.get_rect(i, j), d)

    def render_focus(self):
        col = self.focus_col[0]
        d = self.focus_col[1]
        pygame.draw.rect(self.img, col, self.get_rect(self.i, self.j), d)

    def render(self):
        """Render the whole board."""
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
        self.render_colors()
        self.render_grid()
        self.render_num()
        self.render_sel()
        self.render_focus()
        if len(self.images) > 1: 
            self.render_tile()

    def get_rect(self, i, j):
        dx = self.dx
        dy = self.dy
        return Rect(j*dx, i*dy, dx, dy)

    def get_index(self, x, y):
        """Get index (i, j) from mouse position (x, y)."""
        x = x - self.rect.left
        y = y - self.rect.top
        i = y // self.dy
        j = x // self.dx
        return i, j
            
    def do_event(self, event):
        """React to events."""
        mods = pygame.key.get_mods()
        if event.type == MOUSEBUTTONDOWN:
            self.drag = True

            i, j = self.get_index(*event.pos)
            k = self.Num[i, j]
            self.drag_rect = self.get_rect(i, j)
            # self.drag_img = self.images[k]

            if mods & KMOD_META:
                self.selection.append((i, j))
            else:
                self.selection = [(i, j)]
            print(self.selection)
            self.render()

        elif event.type == MOUSEMOTION:
            if self.drag:
                self.drag_rect.move_ip(event.rel)

        elif event.type == MOUSEBUTTONUP:
            self.drag = False

        elif event.type == KEYDOWN:
            if event.key in self.dirs:
                if self.selection == []:
                    self.selection = [(0, 0)]
                i, j = self.selection[0]
                dj, di = self.dirs[event.key]
                i += di
                j += dj
                
                i = max(0, min(i, self.m-1))
                j = max(0, min(j, self.n-1))
                self.selection = [(i, j)]
                self.i = i
                self.j = j
                self.render()
            if event.unicode in self.keys:
                print(event.unicode)
                if self.Num0[self.i, self.j] == 0:
                    self.Num[self.i, self.j] = int(event.unicode)
                    self.render()

            elif event.key == K_RETURN:
                k = self.Num[self.i, self.j]
                k = (k+1) % 3
                self.Num[self.i, self.j] = k
                self.render()
                
class Num():
    pass
"""
move(dir)
pos = find(0)
if pos+dir exist
    switch(pos, pos+dir)

"""

class Sudoku(Board):
    """Create a sudoko game board."""
    def __init__(self, **options):
        super().__init__(m=9, n=9, **options)

    def render_grid(self):
        """Override the grid lines."""
        super().render_grid()

        col = self.grid[0]
        d = self.grid[1] * 2
        x1, y1 = self.rect.size
        for x in [3 * self.dx, 6 * self.dx]:
            pygame.draw.line(self.img, col, (x, 0), (x, y1), d)
        for y in [3 * self.dy, 6 * self.dy]:
            pygame.draw.line(self.img, col, (0, y), (x1, y), d)


class Chess(Board):
    """Create a sudoko game board."""
    def __init__(self, **options):
        super().__init__(m=8, n=8, colors=[Color('white'), Color('brown')], centered=False, **options)
        self.set_checkerboard()
        self.folder='chess'
        self.load_images()
        self.reset()

    def reset(self):
        self.Num = np.zeros((self.m, self.n), dtype='int8')
        self.Num[0, :] = [3, 5, 7, 9, 11, 7, 5, 3]
        self.Num[1, :] = 1
        self.Num[6, :] = 2
        self.Num[7, :] = [4, 6, 8, 10, 12, 8, 6, 4]
        self.render()


class Go(Board):
    def __init__(self, **options):
        super().__init__(m=19, n=19, dx=10, dy=10, centered=True, colors=[Color('beige')], **options)

    def render(self):
        """Render the Go board and add extra dots on certain intersections."""
        super().render()
        pts = []
        if self.n == 19:
            pts = [(3, 3), (9, 3), (16, 3), (3, 9), (9, 9), (16, 9),
            (3, 16), (9, 16), (16, 16)]
        for (i, j) in pts:
            x = j * self.dx + self.dx//2
            y = i * self.dy + self.dy//2
            pygame.draw.circle(self.img, Color('black'), (x, y), 3)


class Puzzle(Node):
    """Take an image and create a puzzle."""
    def __init__(self, div=(3, 3), **options):
        super().__init__(**options)

        self.divide_img(*div)

    def divide_img(self, m, n):
        (w, h) = self.img.get_size()
        self.images = []

        w0 = w//n
        h0 = h//m

        for i in range(m):
            y = i * h0
            for j in range(n):
                x = j * w0
                img = self.img.subsurface(Rect(x, y, w0, h0))
                self.images.append(img)
                if (i, j) == (0, 0):
                    node = Node(size=(w0, h0), dir=(1, 0), resizable=False)
                else:
                    node = Node(size=(w0, h0), dir=(0.1, 0.1))    
                node.img = img
                node.img0 = img
                   

if __name__ == '__main__':
    app = App()
    Scene(caption='Scene 0', shortcuts={(K_1, KMOD_NONE):'print(1)'})
    Text('Scene 0')
    Ellipse(Color('pink'), Color('magenta'), 10)
    Rectangle(Color('red'), Color('blue'), 10)

    Scene(caption='TextList', bg=Color('cyan'), shortcuts={(K_1, KMOD_NONE):'print(1111111)'}, remember=False)
    Text('TextMenu')
    TextMenu(['Amsterdam', 'Berlin', 'Calcutta', 'Paris', 'Tokyo'], cmd='print(self.text)')
    
    Scene(caption='InputNum')
    Text('Enter numeric input')
    InputNum(cmd='print(self.num)')
    InputNum(num=1.2, inc=0.2, cmd='print(self.num)')

    Scene(caption='TextList')
    TextList(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

    cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 'Harrington', 'Melbourne']
    TextList(cities, dir=(1, 0), cmd='App.scene.set_status(self.item)')

    Scene(caption='Node size')
    Node(size=(40, 40), dir=(1, 1))
    Node(size=(100, 30))
    Node(size=(60, 60))
    Node(size=(20, 20))

    Scene(caption='Ellipse and Rectangle')
    Ellipse(Color('yellow'))
    Rectangle(Color('pink'))
    Ellipse(Color('green'))
    Rectangle(Color('orange'))

    Scene(caption='Board game - selection with mouse and arrow keys')
    Board(dir=(1, 0))
    Board()
    Board()

    Scene(caption='Board size')
    Board(dir=(1, 0))
    Board(m=5)
    Board(n=5)

    Scene(caption='Board checker color')
    Board(dir=(1, 0), m=4, n=4)
    Board()
    Board()

    Scene(caption='Board - Go')
    Go(dir=(1, 0))
    Go()
    # Chess(dx=20, dy=20)

    Scene(caption='Board - Memory puzzle')
    b = Board(m=4, n=4, dx=50, dy=50, centered=False, folder='../animals')
    b.images = []
    b.load_images()
    b.Num = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    b.render()

    Board(dir=(1, 0))

    Scene(caption='Board - Set colors at random')
    b = Board()
    b.colors = [Color('red'), Color('green'), Color('blue'), Color('yellow'),
        Color('pink'), Color('lightblue'), Color('darkred')]
    for i in range(b.m):
        for j in range(b.n):
            b.Col[i, j] = np.random.randint(0, len(b.colors))
    b.render()

    Scene(caption='Board - Puzzle')
    Puzzle(file='../../images/cat.jpg', size=(200, 200))
    
    Scene(caption='Board - Puzzle', selection_surround=True)
    Puzzle(file='../../images/river.jpg', size=(200, 200))

    Scene('Nodes with images')
    Node(file='../animals/cat-icon.png', size=(100, 100), dir=(1, 0))
    Node(file='../animals/dog-icon.png', bg=Color('yellow'))
    Node(file='../animals/cow-icon.png')
    Node(file='', bg=None)
    
    Scene(caption='Buttons', bg=Color('beige'))
    Text('Buttons')
    #Text('Text', size=(200,40), bg=Color('gray'), autosize=False, v_align=1, h_align=1, cmd='print(self, self.text)')
    Button('print(scene)', cmd='print(App.scene)')
    Button('print(123)', cmd='print(123)')
    Button(file='../animals/cat-icon.png', size=(100, 100), pos=(300, 20))
    Text('Buttons')
    
    Scene(caption='Board - number puzzle')
    b = Board(m=4, n=4)
    b.colors = (None, Color('red'))*8
    print(b.colors)
    b.Num = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    b.Num = np.arange(16).reshape((4, 4))
    b.render()

    app.run()

"""
class Num(nparray) - add more functions
class Graph - points, links (Mill)
pts = ((0, 0), (3, 0), (6, 0), (3, 3))
lines = [[1, 3], [3, 2]]
Games : Pong, Snake, Asteroids, Bricks
Games : Mines, 2048
Chess, possible moves, protected positions
rook, bishop, knight, queen, king, pawn
board history, playback
is it a solution ?
is it an end position ?
"""