# App class
import pygame
from pygame.locals import *
import numpy as np

class Sprite:
    def __init__(self, file=None, pos=(0, 0), size=None):
        self.parent = None
        self.size = size
        self.rect = Rect(pos, (20, 20))
        self.position = np.array(pos, dtype=float)
        self.velocity = np.array([1.5, 0.5], dtype=float)

        self.angle = 0
        self.angular_velocity = 0

        self.color = 'red'
        self.speed = [0, 0]
        if file:
            self.image = pygame.image.load(file)
            if self.size:
                self.image = pygame.transform.scale(self.image, size)
                self.rect.size = self.image.get_size()
        else:
            self.image = pygame.Surface(self.rect.size)
            self.image.fill(self.color)
        self.image0 = self.image.copy()

    def set_pos(self, pos):
        self.position = np.array(pos, dtype=float)
        self.rect.center = pos
 
    def set_angle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect.size = self.image.get_size()

    def do(self, event):
        pass

    def update(self):
        self.move()

    def move(self):
        self.position += self.velocity

        if self.angular_velocity:
            self.angle += self.angular_velocity
            self.image = pygame.transform.rotate(self.image0, self.angle)
            self.rect.size = self.image.get_size()

        self.rect.center = self.position
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def distance(self, other):
        distance = self.position - other.position
        distance *= distance
        d = np.sqrt(np.sum(distance))
        return d


class App:
    def __init__(self, file=None, caption='Pygame'):
        pygame.init()
        pygame.display.set_caption(caption)
        self.flags = RESIZABLE
        self.size = (640, 240)
        self.screen = pygame.display.set_mode(self.size, self.flags)
        self.running = True
        self.updating = True
        self.objects = []
        self.bg_color = 'gray'
        if file:
            self.load_image(file)
        else:
            self.image = pygame.Surface(self.size)
            self.image.fill(self.bg_color)
            self.rect = self.image.get_rect()
        self.key_cmd = {}

    def load_image(self, file):
        self.image = pygame.image.load(file).convert()
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size, self.flags)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.do(event)
            self.update()
            self.draw()

    def add_cmd(self, key, cmd):
        self.key_cmd[key] = cmd
        print(self.key_cmd)

    def add(self, object):
        self.objects.append(object)
        object.parent = self

    def do(self, event):
        if event.type == QUIT:
            self.running = False
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.updating = not self.updating

            if event.key in self.key_cmd:
                cmd = self.key_cmd[event.key]
                eval(cmd)

        for obj in self.objects:
            obj.do(event)

    def update(self):
        if self.updating:
            for obj in self.objects:
                obj.update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        for obj in self.objects:
            obj.draw(self.screen)
        pygame.display.update()
        
if __name__ == '__main__':
    app = App('space.png', 'Asteroids')

    ship = Sprite('spaceship.png', size=(100, 50), pos=(300, 200))
    app.add(ship)
    app.add(Sprite('asteroid.png', size=(100, 100), pos=(100, 300)))
    app.add(Sprite('asteroid.png', size=(150, 150), pos=(400, 100)))
    
    app.add_cmd(K_a, 'print(123)')
    app.add_cmd(K_b, "self.load_image('space.png')")
    app.run()