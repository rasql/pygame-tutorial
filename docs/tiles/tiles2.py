import pygame, os
from pygame.locals import *
import numpy as np

file = 'tmw_desert_spacing.png'

print(__file__)
path = os.path.abspath(__file__)
dir = os.path.dirname(path)

base = os.path.basename(path)
print(base)

root, ext = os.path.splitext(path)
print(root)

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

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'      


class Game:
    W = 1200
    H = 800
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        pygame.display.set_caption('Pygame Tile Demo')
        self.running = True

        self.tileset = Tileset(file)
        self.tilemap = Tilemap(self.tileset)
        self.map2 = Tilemap(self.tileset)

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
                        

            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
            
        pygame.quit()

    def save_image(self):
        # Save a screen shot.

        path = os.path.abspath(__file__)
        head, tail = os.path.split(path)
        root, ext = os.path.splitext(path)
        pygame.image.save(self.screen, root + '.png')

game = Game()
game.run()