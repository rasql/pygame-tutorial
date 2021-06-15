import pygame
import os, time
from pygame.locals import *

path = os.path.abspath(__file__)
dir = os.path.dirname(path)
print(dir)

files = os.listdir(dir + '/sounds')


RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
WHITE = 255, 255, 255

class Sounds:
    def __init__(self):
        path = os.path.abspath(__file__)
        dir = os.path.dirname(path) + '/sounds/'
        self.click = pygame.mixer.Sound(dir + 'click.wav')
        self.load = pygame.mixer.Sound(dir + 'load.wav')
        self.positive = pygame.mixer.Sound(dir + 'positive.wav')


class Text:
    def __init__(self, text, pos=(0, 0)):
        self.font = pygame.font.Font(None, 24)
        self.color = (255, 255, 255)
        self.text = text
        self.pos = pos
        self.render(text)

    def render(self, text):
        self.image = self.font.render(text, 1, self.color)

    def draw(self):
        Game.screen.blit(self.image, self.pos)

class Game:
    W = 640
    H = 480

    def __init__(self):
        pygame.init()
        Game.screen = pygame.display.set_mode([Game.W, Game.H])
        pygame.display.set_caption('Pygame Demo')
        self.running = True
        self.group = pygame.sprite.Group
        self.txt = Text('pygame')
        self.sounds = Sounds()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    print(event)
                    if event.key == K_d:
                        self.debugging = not self.debugging
                        print(f'debug: {self.debugging}')

                    elif event.key == K_l:
                        self.sounds.load.play()

                    elif event.key == K_t:
                        #print('resolution:', pygame.TIMER_RESOLUTION)
                        print('ticks:', pygame.time.get_ticks())

                elif event.type == MOUSEBUTTONDOWN:
                    self.sounds.click.play()


            Game.screen.fill(BLUE)
            self.txt.draw()
            pygame.display.flip()


if __name__ == '__main__':
    Game().run()

