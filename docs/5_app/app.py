"""
App
---

- there is only one App object
- an app has multiple scenes (App.scenes)
- an app has one current scene (App.scene)
- an app has one window to draw in (App.screen)

Scene

- a scene has multiple nodes or objects (App.scene.nodes)
- objects are ordered: the last in the list is displayed last
- the object which is clicked becomes active
- the active object becomes the top object
- the active oject has focus (App.scene.focus)
- TAB and shift-TAB select the next object

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

- display outline (cmd+O)
- display node label (cmd+L)
- print events to console (cmd+E)
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
        for node in self.nodes:
            node.update()

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
    """Create a node object with automatic position and inherited size."""
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
            last = App.scene.nodes[-1].rect
            x = self.pos[0] + self.dir[0] * (last.size[0] + self.gap[0])
            y = self.pos[1] + self.dir[1] * (last.size[1] + self.gap[1])
            self.pos = x, y
            Node.options['pos'] = x, y
        
        Node.options['id'] += 1

        self.rect = Rect(*self.pos, *self.size)
        self.img = pygame.Surface(self.rect.size, flags=SRCALPHA)
        App.scene.nodes.append(self)

        # create node label
        font = pygame.font.Font(None, Node.label[1])
        self.label_img = font.render(str(self), True, Node.label[0])
        self.label_rect = self.label_img.get_rect()
        self.label_rect.bottomleft = self.rect.topleft

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
                #if self.file != '':
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
        """Draw the node and its children."""
        if self.visible:
            App.screen.blit(self.img, self.rect)
        
        if App.debug & DBG_OUTLINE:
            pygame.draw.rect(App.screen, Node.outline[0], self.rect, Node.outline[1])

        if App.debug & DBG_LABELS:
            App.screen.blit(self.label_img, self.label_rect)

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
    fontbg = None

    italic = False
    bold = False
    underline = False

    h_align = 0
    v_align = 0

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
        w, h = self.rect.size
        w0, h0 = self.font.size(self.text)
        if w == 0:
            w = w0 
        if h==0:
            h = h0
        self.rect.size = w, h

        self.img0 = pygame.Surface((w, h), flags=SRCALPHA)
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
    options = { 'border': 2,
                'size': (160, 40),
        }


    def __init__(self, text='Button', cmd='',  **options):
        super().__init__(text, **options)
        #self.__dict__.update(Button.options)

        self.cmd = cmd
    #     self.rect.size = 160, 40
    #     self.button_color = Color('green')
    #     self.render()

    # def render(self):
    #     """Create the button image with background color and centered text."""
    #     self.img0 = pygame.Surface(self.rect.size)
    #     self.img0.fill(Color('green'))
    #     self.text_img = self.font.render(self.text, True, self.fontcolor, self.fontbg)
    #     self.text_rect = self.text_img.get_rect()
    #     self.text_rect.center = self.rect.center
    #     self.img0.blit(self.text_img, self.text_rect)
    #     self.img = self.img0.copy()
    #     self.size = self.rect.size

    def do_event(self, event):
        super().do_event(event)
        if event.type == MOUSEBUTTONDOWN:
            exec(self.cmd)


if __name__ == '__main__':
    app = App()
    Scene(caption='Scene 0')
    Text('Scene 0')
    Ellipse(Color('pink'), Color('magenta'), 10)
    Rectangle(Color('red'), Color('blue'), 10)

    Scene(caption='TextList', bg=Color('cyan'))
    Text('TextMenu')
    TextMenu(['Amsterdam', 'Berlin', 'Calcutta', 'Paris', 'Tokyo'], cmd='print(self.text)')
    
    Scene(caption='InputNum', bg=Color('cyan'))
    Text('Enter numeric input')
    InputNum(cmd='print(self.num)')
    InputNum(num=1.2, inc=0.2, cmd='print(self.num)')

    Scene(caption='TextList')
    TextList(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

    cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 'Harrington', 'Melbourne']
    TextList(cities, dir=(1, 0))

    Scene(caption='Buttons', bg=Color('cyan'))
    Text('Buttons')
    Button('print(scene)', cmd='print(App.scene)')
    Button('print(123)', cmd='print(123)')


    Scene(caption='Node size')
    Node(size=(40, 40), dir=(1, 1))
    Node(size=(80, 80))
    Node(size=(60, 60))
    Node(size=(20, 20))



    app.run()