import pygame, os
from pygame.locals import *
import numpy as np

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file = 'tmw_desert_spacing.png'

class Editor(pygame.sprite.Sprite):
    # Create an image editor
    group = pygame.sprite.Group()
    color_dict = {'r':'red', 'g':'green', 'b':'blue',
    'y':'yellow', 'c':'cyan', 'm':'magenta', 'w':'white', 'k':'black'}

    def __init__(self, rect=None):
        super().__init__()
        self.image = pygame.Surface((200, 100))
        self.bg = 'gray'
        self.image.fill(self.bg)
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()
        
        self.drawing = False
        self.p0 = (0, 0)
        self.color = 'black'
        print(pygame.Color(self.color))

        self.stroke = 1
        Editor.group.add(self)

    def do(self, event):
        if event.type == KEYDOWN:
            if event.unicode in 'rbgycmwk':
                self.color = self.color_dict[event.unicode]
                print(self.color)
            elif event.unicode in '123456789':
                self.stroke = int(event.unicode)
                print('stroke', self.stroke)
            elif event.key == K_o:
                path = filedialog.askopenfilename()
                print(path)
                self.image = pygame.image.load(path)
                self.rect.size = self.image.get_size()

            elif event.key == K_s:
                path = filedialog.askopenfilename(initialdir=".")
                self.image.save('xxx.png')


        elif event.type == MOUSEBUTTONDOWN:
            self.p0 = event.pos
            self.drawing = True

        elif event.type == MOUSEMOTION:
            print(event)
            p1 = event.pos
            pygame.draw.line(self.image, self.color, self.p0, p1, self.stroke)
            self.p0 = p1
        elif event.type == MOUSEBUTTONUP:
            self.drawing = False



class Text(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self, text, pos=(0, 0)):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.color = (255, 255, 255)
        self.text = text
        self.pos = pos
        self.render(text)
        Text.group.add(self)

    def render(self, text):
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        screen.blit(self.image, self.pos)

class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'


class Tilemap:
    def __init__(self, tileset, size=(10, 20), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32*w, 32*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def do(self, event):
        # react to user events
        if event.type == MOUSEBUTTONDOWN:
            print(event.pos)

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'      


class App:
    W = 800
    H = 600
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(App.SIZE)
        self.screen.fill('black')
        pygame.display.set_caption('Pygame Tile Demo')
        pygame.display.update()

        self.running = True

        self.tileset = Tileset(file)
        self.tilemap = Tilemap(self.tileset, rect=(50, 50, 500, 300))
        self.tilemap.set_random()
        self.label = Text('Tile demo') 

        self.img_editor1 = Editor()
        self.img_editor2 = Editor((100, 500, 200, 100))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_m:
                        print(self.tilemap.map)
                    elif event.key == K_r:
                        self.tilemap.set_random()
                    elif event.key == K_z:
                        self.tilemap.set_zero()
                    elif event.key == K_s:
                        self.save_image()

                self.tilemap.do(event)
                self.img_editor1.do(event)
                        
            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            
            Text.group.draw(self.screen)
            Editor.group.draw(self.screen)
            pygame.display.update()
            
        pygame.quit()

    def save_image(self):
        # Save a screen shot.

        path = os.path.abspath(__file__)
        head, tail = os.path.split(path)
        root, ext = os.path.splitext(path)
        pygame.image.save(self.screen, root + '.png')

app = App()
app.run()