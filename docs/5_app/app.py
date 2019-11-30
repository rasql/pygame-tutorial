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

DBL_CLICK_TIMER = pygame.USEREVENT
DBL_CLICK_TIMEOUT = 200

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
    key_repeat = 200, 100

    def __init__(self, size=(640, 240), shortcuts={}):
        """Initialize pygame and the application."""
        pygame.init()
        pygame.key.set_repeat(*App.key_repeat)
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

            (K_e, KMOD_LCTRL): 'Ellipse(pos=pygame.mouse.get_pos(), size=(100, 60))',
            (K_i, KMOD_LCTRL): 'Node(pos=pygame.mouse.get_pos(), size=(100, 60))',
            (K_n, KMOD_LCTRL): 'Node(pos=pygame.mouse.get_pos(), size=(100, 60))',
            (K_r, KMOD_LCTRL): 'Rectangle(pos=pygame.mouse.get_pos(), size=(100, 60))',
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
                #'caption': 'Pygame',  # window caption
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

    def __init__(self, caption='Pygame', remember=True, **options):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        self.nodes = []
        self.caption = caption

        self.clicks = 0  # for double-clicks
        self.text = ''   # for copy/paste

        # Reset Node options to default
        Node.reset_options()

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
            pygame.time.set_timer(DBL_CLICK_TIMER, DBL_CLICK_TIMEOUT)
            self.clicks += 1

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

        elif event.type == DBL_CLICK_TIMER:
            pygame.time.set_timer(DBL_CLICK_TIMER, 0)
            print(self.clicks, 'clicks in', self.focus)
            
            if self.focus:
                if self.clicks == 2:
                    self.focus.double_click()
                elif self.clicks == 3:
                    self.focus.triple_click()

            self.clicks = 0
        
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
        App.selection = self.selection
        for x in self.selection:
            self.nodes.remove(x)
        self.selection = []

    def copy(self):
        """Copies the selected objects and places them in App.selection."""
        App.selection = self.selection

    def paste(self):
        """Pastes the objects from App.selection."""
        print('paste')
        # obj = App.focus
        # obj2 = eval(type(obj).__name__+'()')
        # obj2.rect = obj.rect.copy()
        # #®obj2.__dict__.update(obj.__dict__)
        # obj2.rect.topleft = pygame.mouse.get_pos()
        # obj2.label_rect.bottomleft = pygame.mouse.get_pos()
        # self.nodes.append(obj2)

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
                'keep': True,
                'file': '',
                'bg': None,
                'img': None,
                'cmd': '',  # command string

                'visible': True,
                'movable': True,
                'resizable': True,
                }

    # current options dictionary for each node
    options = options0.copy()
    resizing = False
    moving = False

    # color and size/thickness
    label = Color('red'), 14
    outline = Color('red'), 1
    focus = Color('blue'), 1
    selection = Color('green'), 2

    # key direction vectors
    dirs = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1)}

    @classmethod
    def reset_options(cls):
        cls.options = cls.options0.copy()

    @staticmethod
    def increment_id():
        Node.options['id'] += 1 

    def __init__(self, **options):
        # update existing Node options, without adding new ones
        self.set_options(Node, options)
        self.increment_id()
        
        self.calculate_pos(options)
        self.rect = Rect(*self.pos, *self.size)
        
        App.scene.nodes.append(self)
        self.render_label()

        self.create_img()
        self.color_img()
        if self.file != '':
            self.load_img()

    def set_options(self, cls, options):
        """Set instance options from class options."""

        if 'keep' in options:
            Node.options['keep'] = options['keep']

        if Node.options['keep']:
            # update class options from instance option
            for key in options:
                if key in cls.options:
                    cls.options[key] = options[key]

        self.__dict__.update(cls.options)
        self.__dict__.update(options)


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

        elif event.type == MOUSEBUTTONUP:
            Node.resizing = False
            Node.moving = False

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

class TextObj:
    """Create a text surface image."""
    options = { 'fontname': None,
                'fontsize': 24,
                'fontcolor': Color('black'),

                'italic': False,
                'bold': False,
                'underline': False,

                'width': 300,
                'align': 0,  # 0=left, 1=center, 2=right
                'bg': None,
                'x': 0,
    }

    def __init__(self, text='Text', **options):
        """Instantiate and render the text object."""
        # update existing Text options, without adding new ones
        for k in options:
            if k in TextObj.options:
                TextObj.options[k] = options[k]

        self.__dict__.update(TextObj.options)
        
        self.text = text
        self.set_font()
        self.render_text()

    def set_font(self):
        """Set the font and its properties."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

    def render_text(self):
        """Render the text into an image."""
        img = self.font.render(self.text, True, self.fontcolor, self.bg)
        self.rect = img.get_rect()
        self.align_image(img)

    def align_image(self, img):
        w, h = self.font.size(self.text)
        w0 = self.width
        self.x = 0
        if w0 > 0:
            self.x = (0, (w0-w)//2, (w0-w))[self.align]
            self.img = pygame.Surface((w0, h))
            if self.bg != None:
                self.img.fill(self.bg)
            self.img.blit(img, (self.x, 0))
            self.rect.size = self.img.get_size()
        else:
            self.img = img

class Text(Node):
    """Create a text object horizontal and vertical alignement."""

    def __init__(self, text='Text', **options):
            super().__init__(**options)
    
            self.txt = TextObj(text, **options)
            self.rect.size = self.txt.rect.size
            self.img = self.txt.img

class TextLines(Node):
    options = {
        'interline': 1,
    }
    def __init__(self, text, **options):
        super().__init__(**options)
        self.set_options(TextLines, options)

        self.text = text
        self.lines = text.split('\n')
        self.line0 = TextObj(self.lines[0], **options)
        self.h = self.line0.font.get_linesize()
        n = len(self.lines)
        self.rect.width = self.line0.width
        self.rect.height = (n-1)*self.interline*self.h+self.h
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
        bg = TextObj.options['bg']
        if bg != None:
            self.img.fill(bg)
        self.render()

    def render(self):
        for i, line in enumerate(self.lines):
            txt = TextObj(line)
            y = self.interline * self.h * i
            self.img.blit(txt.img, (0, y))

class EditableTextObj(TextObj):
    """Create keyboard and mouse-editable text with cursor and selection."""
    cursor_style = Color('red'), 2  # cursor color and width
    selection_style = Color('pink'), 0
    blink_rate = 600, 400   # interval, on_time
    
    def __init__(self, text='EditableText', cmd='', **options):
        super().__init__(text, **options)

        # Set cursor index to the end of text string
        self.cmd = cmd
        self.i = len(self.text)
        self.i2 = self.i
        self.set_char_positions()
        self.render()

    def set_char_positions(self):
        """Make a list of all character positions."""
        self.char_positions = [0]
        for i in range(len(self.text)):
            w, h = self.font.size(self.text[:i+1])
            self.char_positions.append(w)

    def get_char_index(self, position):
        """Return the character index for a given position."""
        for i, pos in enumerate(self.char_positions):
            if position <= pos:
                return i
        # if not found return the highest index
        return i

    def move_cursor(self, d):
        """Move the cursor by d characters, and limit to text length."""
        mod = pygame.key.get_mods()
        n = len(self.text)
        self.i = min(max(0, self.i+d), n)

        if mod & KMOD_META:
            self.i = n if d == 1 else 0

        if mod & KMOD_ALT:
            while (0 < self.i < n) and self.text[self.i] != ' ':
                self.i += d

        if not mod & KMOD_SHIFT:
            self.i2 = self.i

    def get_selection(self):
        """Get ordered tuple of selection indices.""" 
        if self.i < self.i2:
            return self.i, self.i2
        else:
            return self.i2, self.i

    def copy_text(self):
        """Copy text to Scene.text buffer."""
        i, i2 = self.get_selection()
        text = self.text[i:i2]
        App.scene.text = text

    def cut_text(self):
        """Cut text and place copy in Scene.text buffer."""
        self.copy_text()
        self.insert_text('')

    def insert_text(self, text):
        """Insert text at the cursor position or replace selection."""
        i, i2 = self.get_selection()
        text1 = self.text[:i]
        text2 = self.text[i2:]
        self.text = text1 + text + text2
        self.set_char_positions()
        self.i = i + len(text)
        self.i2 = self.i

    def select_word(self):
        """Select word at current position."""
        i = i2 = self.i
        n = len(self.text)

        while (0 < i < n) and self.text[i] != ' ':
                i -= 1
        
        while (0 < i2 < n) and self.text[i2] != ' ':
                i2 += 1

        self.i = i2
        self.i2 = i+1 if self.text[i]==' ' else i

    def select_all(self):
        """Select the whole text."""
        self.i = len(self.text)
        self.i2 = 0

    def do_event(self, event):
        """Move cursor, handle selection, add/backspace text, copy/paste."""
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                App.scene.focus = None
                print(self.cmd)
                try:
                    exec(self.cmd)
                except:
                    print(f'cmd error in {self}')

            elif event.key == K_BACKSPACE:
                # delete previous charactor or selection
                if self.i == self.i2:
                    self.i = max(0, self.i-1)
                self.insert_text('')

            elif event.key in (K_TAB, K_UP, K_DOWN, K_LCTRL, K_LMETA, K_LALT, K_LSHIFT):
                pass
            
            elif event.key == K_LEFT:
                self.move_cursor(-1)
            
            elif event.key == K_RIGHT:
                self.move_cursor(1)

            elif not (event.mod & KMOD_META + KMOD_CTRL):
                self.insert_text(event.unicode)

            elif event.key == K_x and event.mod & KMOD_META:
                self.cut_text()

            elif event.key == K_c and event.mod & KMOD_META:
                self.copy_text()

            elif event.key == K_v and event.mod & KMOD_META:
                self.insert_text(App.scene.text)

            elif event.key == K_a and event.mod & KMOD_META:
                self.select_all()

            self.render()

        elif event.type == MOUSEBUTTONDOWN:
            pos = event.pos[0] - self.rect.left - self.x
            if pos < 3:
                pos = 0

            self.i = self.get_char_index(pos)
            if not pygame.key.get_mods() & KMOD_SHIFT:
                self.i2 = self.i

        elif event.type == MOUSEMOTION and event.buttons[0]:
            pos = event.pos[0] - self.rect.left - self.x
            if pos < 3:
                pos = 0 

            self.i = self.get_char_index(pos)

        self.render()

    def render(self):
        """Render cursor, selection and text to an image."""
        h = self.font.get_height()
        p = self.char_positions[self.i]
        p2 = self.char_positions[self.i2]

        self.cursor_rect = Rect(p, 0, 2, h)

        if p2 < p:
            p, p2 = p2, p
        
        self.selection_rect = Rect(p, 0, p2-p, h)

        w, h = self.font.size(self.text)
        img = pygame.Surface((w+2, h))
        
        col, d = self.selection_style
        pygame.draw.rect(img, col, self.selection_rect, d)
        txt = self.font.render(self.text, True, self.fontcolor)
        img.blit(txt, (0, 0))
        
        col, d = self.cursor_style
        pygame.draw.rect(img, col, self.cursor_rect)
        self.align_image(img)

class EditableText(Node):
    """Create an editable text node."""
    def __init__(self, text='CursorText', **options):
        super().__init__(**options)

        self.txt = EditableTextObj(text, **options)
        self.rect.size = self.txt.rect.size
        self.txt.rect = self.rect 

        self.img = self.txt.img
        self.rect.height = self.txt.font.get_height()

    def do_event(self, event):
        self.txt.do_event(event)
        self.img = self.txt.img

    def draw(self):
        # self.txt.draw()
        Node.draw(self)
        if self == App.scene.focus:
            t = pygame.time.get_ticks()
            interval, on_time = EditableTextObj.blink_rate
            if (t % interval) < on_time:
                col, d = EditableTextObj.cursor_style
                rect = self.txt.cursor_rect.move(self.rect.topleft)
                rect.move_ip(self.txt.x, 0)
                pygame.draw.rect(App.screen, Color('blue'), rect)


    def double_click(self):
        """Select the current word."""
        self.txt.select_word()

    def triple_click(self):
        self.txt.select_all()

class Button(Node):
    """Create a button object with command.""" 
    options = { 'border': 2,
                'bg': Color('gray'),
                'size': (160, 40),
                'autosize': False,
                'align': 1,
                'state': False,
        }

    def __init__(self, text='Button', cmd='', **options):
        super().__init__(**options)
        self.set_options(Button, options)

        self.cmd = cmd
        self.label = TextObj(text, bg=None, **options)
        self.render()

    def render(self):
        self.img.fill(Color('lightblue'))
        self.label.render_text()
        w, h = self.rect.size
        self.label.rect.center = w//2, h//2
        self.img.blit(self.label.img, self.label.rect)

    def do_event(self, event):
        super().do_event(event)
        if event.type == MOUSEBUTTONDOWN:
            self.state = not self.state
            try: 
                exec(self.cmd)
            except:
                print('cmd error')

            if self.state:
                self.label.text = 'ON'
            else:
                self.label.text = 'OFF'
            self.render()


class Toggle:
    """Add toggle button behavior."""

    def switch_state(self):
        self.state = not self.state
        try: 
            exec(self.cmd)
        except:
            print('cmd error') 
        self.render()

    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.switch_state()
        
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.switch_state()


class Checkbox(Toggle, Node):
    options = {
        'state': False,
        'style': (Color('blue'), 2),
    }

    def __init__(self, **options):
        super().__init__(**options)
        self.set_options(Checkbox, options)

        self.label = TextObj(**options)
        w, h = self.label.img.get_size()
        self.size = w+h, h
        self.rect.size = self.size
        
        self.img = pygame.Surface((w+h, h), flags=SRCALPHA)
        self.state = False
        self.render()

    def render(self):
        col, d = self.style
        w, h = self.label.img.get_size()
        a = self.label.font.get_ascent()

        self.img.blit(self.label.img, (h, 0))
        pygame.draw.rect(self.img, (0, 0, 0, 0), Rect(0, 0, a, a))
        pygame.draw.rect(self.img, Color('black'), Rect(0, 0, a, a), d)
        if self.state:
            pygame.draw.line(self.img, col, (0, 0), (a, a), d)
            pygame.draw.line(self.img, col, (0, a), (a, 0), d)
            
class Radiobutton(Checkbox):

    def render(self):
        col, d = self.style
        w, h = self.label.img.get_size()
        a = self.label.font.get_ascent()

        self.img.blit(self.label.img, (h, 0))

        pygame.draw.rect(self.img, (0, 0, 0, 0), Rect(0, 0, a, a))
        pygame.draw.ellipse(self.img, Color('black'), Rect(0, 0, a, a), 1)
        if self.state:
            pygame.draw.ellipse(self.img, Color('black'), Rect(3, 3, a-6, a-6), 0)


class ListBox(Node):
    """Show a list of text items."""

    options = { 'm': 10,        # listbox height
                'width': 100,   # in pixels
                'wrap': False,  # cursors wraps around
                'align': 0,     # 0=left, 1=center, 2=right
                'mode': 1,      # 0=none, 1=one, 2=multiple selections
                'style': (Color('black'), Color('white')),     # font color, background color
                'sel_style': (Color('white'), Color('blue')),  # font color, background color
                'fontsize': 24,
    }

    def __init__(self, items, i=0, **options):
        super().__init__(**options)
        self.set_options(ListBox, options)

        self.set_list(items)
        self.font = pygame.font.Font(None, self.fontsize)
        self.h = self.font.size('fg')[1]
        self.render()

    def set_list(self, items):
        """Set items and selection list."""
        self.i = 0
        self.i0 = 0     # first ListBox item
        self.i2 = 0     # cursor
        self.items = items
        self.n = len(items)
        self.sel = [0] * self.n
        
    def render(self):
        w0 = self.width
        fg, bg = self.style

        self.img0 = pygame.Surface((w0, self.m * self.h))
        self.img0.fill(bg)
        self.rect.size = self.img0.get_size()
        
        for i in range(min(self.m, self.n)):
            if self.sel[self.i0 + i]:
                fg, bg = self.sel_style
            else:
                fg, bg = self.style

            text = self.font.render(self.items[self.i0 + i], True, fg)
            w, h = text.get_size()
            x = (0, (w0-w)//2, w0-w)[self.align]

            rect = Rect(0, i * self.h, w0, h)
            self.img0.fill(bg, rect)
            self.img0.blit(text, (x, i*self.h))
        self.img = self.img0.copy()

    def scroll(self, d):
        """Scroll listbox up and down."""
        i0 = self.i0
        n = max(0, self.n - self.m)
        self.i0 = max(0, min(i0+d, n))

    def move_cursor(self, d):
        """Move the active cell up or down."""
        mod = pygame.key.get_mods()
        i, n = self.i, self.n

        # when ALT pressed move a screenful
        if mod & KMOD_ALT:
            d *= self.m-1

        if self.wrap:
            i = (i + d) % n
        else:
            i = max(0, min(i+d, n-1))
        
        # adjust visible part
        if i < self.i0:
            self.i0 = i
        elif i >= self.i0 + self.m:
            self.i0 = i - self.m + 1

        # when ALT pressed move to begin or end
        if mod & KMOD_META:
            if d == 1:
                i = n - 1
                self.i0 = max(0, n - self.m)
            else:
                i = 0
                self.i0 = 0

        self.i = i
        # self.sel[i] = 1
        self.select(i)

    def select(self, i):
        # Select item i
        mod = pygame.key.get_mods()
        self.i = i
        self.item = self.items[i]

        if self.mode == 1:
            self.select_all(0)
            self.sel[i] = 1
        elif self.mode == 2:
            if mod & KMOD_SHIFT:
                self.sel[i] = 1
            elif mod & KMOD_META:
                self.sel[i] = 1 - self.sel[i]
            else:
                self.select_all(0)
                self.sel[i] = 1
            
        
    def select_all(self, val):
         for i in range(self.n):
            self.sel[i] = val

    def do_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                x, y = event.pos
                x -= self.rect.left
                y -= self.rect.top
                i = y // self.h + self.i0
                i = min(i, self.n-1)
                self.select(i)

            # scroll with mouse pad
            elif event.button == 4:
                self.scroll(-1)
            elif event.button == 5:
                self.scroll(1)
        
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.move_cursor(1)
            elif event.key == K_UP:
                self.move_cursor(-1)
            elif event.key == K_RETURN:
                exec(self.cmd)
            elif event.key == K_a:
                if event.mod & KMOD_META and self.mode == 2:
                    self.select_all(1)
                   
        self.render()

class ListMenu:
    """Display a drop-down menu."""
    def __init__(self, items, **options):
        self.items = items

class SliderObj:
    """Define a slider object."""
    options = {
        'x0': 0,
        'x1': 100,
        'dx': 1,
        'size': (100,30),
        'orientation': 0,  # 0=horizontal, 1=vertical
        'slider_style': (Color('blue'), Color('white'), 4, 2), 
        'slider_size': (10, 20),
        'slider_type': 0,  # 0=rectangle 1=circle
    }
    style_label = (Color('black'))

    def __init__(self, **options):
        # update existing SliderObj options, without adding new ones
        for k in options:
            if k in SliderObj.options:
                SliderObj.options[k] = options[k]
        self.__dict__.update(SliderObj.options)

        self.x = (self.x1 + self.x0)/2

        self.img = pygame.Surface(self.size, flags=SRCALPHA)
        self.rect = self.img.get_rect()

        self.font = pygame.font.Font(None, 18)
        self.render()

    def render(self):
        w, h = self.size
        col, col2, d, d2 = self.slider_style
        w0, h0 = self.slider_size

        img_x0 = self.font.render(str(self.x0), True, col)
        img_x1 = self.font.render(str(self.x1), True, col)
        img_x  = self.font.render(f'{self.x:.1f}', True, col)
        
        rect_x0 = img_x0.get_rect()
        rect_x1 = img_x1.get_rect()
        rect_x = img_x.get_rect()

        if self.orientation == 0:
            rect_x0.bottomleft = (0, h)
        else:
            rect_x0.bottomleft = (0, h)

        if self.orientation == 0:
            rect_x1.bottomright = w, h
        else:
            rect_x1.topleft = 0, 0//2

        if self.orientation == 0:
            rect_x.midbottom = w//2, h
        else:
            rect_x.midleft = 0, h//2
        
        if self.orientation == 0:
            self.slider_rect = Rect(0, 0, w0, h0)
        else:
            self.slider_rect = Rect(0, 0, h0, w0)

        if self.orientation == 0:
            self.slider_rect.topleft = (self.x-self.x0) / (self.x1-self.x0) * (w-w0), 0
        else:
            self.slider_rect.topright = w, (self.x1-self.x) / (self.x1-self.x0) * (h-w0)

        self.img.fill((0, 0, 0, 0))
        self.img.blit(img_x0, rect_x0)
        self.img.blit(img_x1, rect_x1)
        self.img.blit(img_x, rect_x)
        
        if self.orientation == 0:
            p0 = 0, h0//2
            p1 = w, h0//2
        else:
            p0 = w-h0//2, 0
            p1 = w-h0//2, h

        pygame.draw.line(self.img, col, p0, p1, d)

        if self.slider_type == 0:
            pygame.draw.rect(self.img, col2, self.slider_rect)
            pygame.draw.rect(self.img, col, self.slider_rect, d2)
        else:
            pygame.draw.ellipse(self.img, col2, self.slider_rect)
            pygame.draw.ellipse(self.img, col, self.slider_rect, d2)


    def do_event(self, event):
        keys = {K_DOWN:-1, K_LEFT:-1, K_UP:1, K_RIGHT:1}
        if event.type == KEYDOWN:
            if event.key in keys:
                dx = keys[event.key] * self.dx
                if event.mod & KMOD_ALT:
                    dx *= 10
                if event.mod & KMOD_META:
                    dx *= 100
                self.x = max(self.x0, min(self.x + dx, self.x1))
                self.render()

        if event.type == MOUSEMOTION and event.buttons[0] == 1:
            dx, dy = event.rel
            w, h = self.size
            x = self.x1 - self.x0
            if self.orientation == 0:
                self.x += (dx/w)*x
            else:
                self.x += (-dy/h)*x
            self.x = max(self.x0, min(self.x, self.x1))
            self.render()

class Slider(Node):
    def __init__(self, **options):
        super().__init__(**options)
        self.slider = SliderObj(**options)
        self.slider.rect = self.rect
        self.img = self.slider.img

    def do_event(self, event):
        self.slider.do_event(event)

class Spinbox(Node):
    """Input a number."""
    options = { 'min': 0,
                'max': 10,
                'inc': 1,
                'val': 5,
                'lbl': 'Spinbox',
                'w': (100, 100)
                }
    def __init__(self, **options):
        super().__init__(**options)
        self.set_options(Spinbox, options)
        self.label = TextObj(self.lbl, **options)
        self.value = TextObj(str(self.val))
        x0, x1 = self.w
        h = self.label.img.get_size()[1]
        self.img = pygame.Surface((x0+x1, h))
        self.img.set_colorkey(Color('white'))
        self.rect.size = self.img.get_size()
        self.render()

    def render(self):
        self.img.fill(Color('white'))
        self.img.blit(self.label.img, (0, 0))
        self.img.blit(self.value.img, (self.w[0], 0))
        self.img0 = self.img.copy()

    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                exec(self.cmd)
            elif event.key in (K_RIGHT, K_UP):
                self.val = min(self.max, self.val + self.inc)
            elif event.key in (K_LEFT, K_DOWN):
                self.val = max(self.min, self.val - self.inc)
            self.value.text = str(self.val)
            self.value.render()
            self.render()

class Rectangle(Node):
    """Draw a rectangle on the screen."""
    options = { 'fg': Color('green'),
                'bg': Color('black'),
                'thickness': 2}

    def __init__(self, **options):
        super().__init__(**options)
        self.set_options(Rectangle, options)
        self.render()

    def render(self):
        self.img0 = pygame.Surface(self.rect.size, flags=SRCALPHA)
        if self.fg != None:
            pygame.draw.rect(self.img0, self.fg, Rect(0, 0, *self.rect.size), 0)
        pygame.draw.rect(self.img0, self.bg, Rect(0, 0, *self.rect.size), self.thickness)
        self.img = self.img0.copy()


class Ellipse(Rectangle):
    """Draw an ellipse on the screen."""

    def render(self):
        self.img0 = pygame.Surface(self.rect.size, flags=SRCALPHA)
        if self.fg != None:
            pygame.draw.ellipse(self.img0, self.fg, Rect(0, 0, *self.rect.size), 0)
        pygame.draw.ellipse(self.img0, self.bg, Rect(0, 0, *self.rect.size), self.thickness)
        self.img = self.img0.copy()

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

    # def switch_Num(self, dir):
    #     i1, j1
    #     i2 = i + di
    #     j2 = j + dj
    #     if 0 < i2 < n:
    #         tmp = self.Num[i1, j1]
    #         self.Num[i1, j1] = self.Num[i2, j2]
    #         self.Num[i2, j2] = tmp

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
    Scene('Introduction')
    TextLines('''An app can have multiple scenes\n
    cmd+s - goes to the next scene
    cmd+shift+s - goes to the previous scene
    
    cmd+f - toggle full screen
    cmd+r - toggle resizable
    cmd+g - toggle no-frame''')

    Scene('Debugging')
    TextLines('''Debug shortcuts\n
    cmd+o - show outline
    cmd+l - show labels
    cmd+e - show events
    
    cmd+q - quit the app
    cmd+h - hide window
    cmd+p - save screen shot to current folder''')

    Scene('Create objects')
    TextLines('''Create objects\n
    ctrl+r - new Rectangle
    ctrl+e - new Ellipse
    ctrl+t - new Text
    ctrl+n - new Node''')
    Rectangle()
    Ellipse(fg=Color('pink'), bg=Color('magenta'), thickness=10)
    
    Scene('Scene shortcuts', shortcuts={(K_1, KMOD_NONE):'print(1)'})
    Text('Pressing "1" prints 1 to the console')

    Scene('Scene shortcuts', shortcuts={(K_1, KMOD_NONE):'print(1111111)'}, remember=False)
    Text('Pressing "1" prints 1111111 to the console')

    Scene(caption='ListBox')
    ListBox(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

    cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 'Harrington', 'Melbourne']
    ListBox(cities, dir=(1, 0), cmd='App.scene.set_status(self.item)')

    Scene(caption='Node size')
    Node(size=(40, 40), dir=(1, 1))
    Node(size=(100, 30))
    Node(size=(60, 60))
    Node(size=(20, 20))

    Scene(caption='Ellipse and Rectangle')
    Ellipse(fg=Color('yellow'))
    Rectangle(fg=Color('pink'))
    Ellipse(fg=Color('green'))
    Rectangle(fg=Color('orange'))

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
    
    Scene(caption='Board - number puzzle')
    b = Board(m=4, n=4)
    b.colors = (None, Color('red'))*8

    b.Num = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    b.Num = np.arange(16).reshape((4, 4))
    b.render()

    Scene('TextObj')
    Text('TextObj', size=(150, 25))
    Text('underline', underline=True)
    Text('italic', italic=True)
    Text('bold', bold=True)
    Text('red', fontcolor=Color('red'))
    Text('size=48', fontsize=48, keep=True)
    
    names = ['Charlie', 'Daniel', 'Tim', 'Jack']
    cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 
        'Harrington', 'Melbourne', 'New York', 'Oslo', 'Paris']    
    constants = dir(pygame.locals)
    
    Scene('ListBox')
    Text('Text alignement: left, center, right', fontsize=24, width=0, 
        fontcolor=Color('black'), italic=False, bold=False, underline=False)
    ListBox(names, cmd='print(self.item)')
    ListBox(cities, dir=(1, 0), wrap=True, align=1, mode=1)
    ListBox(constants, width=300, align=2, wrap=False, mode=2)

    Scene('ListBox')
    Text('Single item selection')
    ListBox(names, cmd='print(self.item)', width=100, align=0, mode=1)
    ListBox(cities, dir=(1, 0), wrap=True)
    ListBox(constants, width=300, align=2, wrap=False)

    Scene('ListBox')
    Text('Multiple item selection')
    ListBox(names, cmd='print(self.item)', width=100, align=0, mode=2)
    ListBox(cities, dir=(1, 0), wrap=True)
    ListBox(constants, width=300, align=2, wrap=False)

    Scene('Checkbox')
    for x in ('Monday', 'Tuesday', 'Wednesday'):
        Checkbox(text=x, cmd='print(self, self.state)')

    Radiobutton.pos = (200, 20)
    for x in ('Java', 'Python', 'C++'):
        Radiobutton(text=x)

    Scene('Multi-line text') 
    TextLines('align=0\nThis is text is extending over\nmultiple lines', align=0, width=400)
    TextLines('align=1\nThis is text is extending over\nmultiple lines', align=1)
    TextLines('align=2\nThis is text is extending over\nmultiple lines', align=2)    

    Scene('Multi-line text') 
    TextLines('This is text extending\nover multiple lines')
    TextLines('interline=1.5\nThis is text is extending over\nmultiple lines', align=1, interline=1.5)
    TextLines('interline=0.8\nThis is text is extending over\nmultiple lines', align=2, interline=0.8)        #\nScene('ListMenu')
    # ListBox(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

    Scene('Rectangles')
    Rectangle(fg=Color('yellow'), thickness=10)
    Rectangle(fg=Color('cyan'))
    Rectangle(fg=None)

    Scene('TextEdit - editable text')
    EditableText('This is left-aligned editable text', align=0, width=400, fontsize=24)
    EditableText('This is centered editable text', align=1) 
    EditableText('This is right-aligned editable text', align=2) 
    EditableText('This text has a cmd fonction', cmd='print(self.text)') 
    
    Scene('Text - alignement and autosize')
    Text('left (align=0)', align=0, width=300)
    Text('center (align=1)', align=1)
    Text('right (align=2)', align=2)
    Text('fontcolor=blue', fontcolor=Color('blue'))
    Text('background=cyan', bg=Color('cyan'))
    Text('autosize (width=0)', width=0)

    Scene('Buttons')
    Button(file='../../images/ui/blue_button00.png', cmd='print(self, self.state)')
    Button('Start', cmd='print(self, self.state)')
    Button('Stop')
    Node(file='../../images/ui/green_button00.png', cmd='print(123)', pos=(200, 20))
    Node(file='../../images/ui/red_button00.png')
    Node(file='../../images/ui/blue_boxCheckmark.png', size=(38, 36))
    Node(file='../../images/ui/blue_boxCross.png')
    
    Scene('Slider')
    Text('Horizontal slider')
    Slider(size=(100, 40))
    Slider(size=(200, 40), x0=-50, x1=50, dx=10)
    Slider(size=(300, 30), x0=0, x1=10, dx=1, slider_type=1, slider_size=(14, 14))

    Scene('Slider')
    Text('Vertical slider')
    Slider(orientation=1, size=(40, 200), dir=(1, 0))
    Slider(size=(40, 100))
    Slider(size=(40, 150))

    Scene('Spinbox')
    Spinbox()
    Spinbox(val=7)
    Spinbox(lbl='max=100', max=100, fontsize=36)
    Spinbox(lbl='inc=10', inc=10)

    app.run()