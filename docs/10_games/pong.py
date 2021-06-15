"""The game of PONG."""

import pygame
from pygame.locals import *
from pygamelib import *

class Ball:
    def __init__(self, pos, field):
        self.pos = pos
        self.field = field
        self.speed = [1, 1]
        self.color = RED
        self.rect = pygame.Rect(pos, (20, 20))

    def update(self):
        self.rect.move_ip(self.speed)

        if self.rect.left < self.field.rect.left:
            self.speed[0] = abs(self.speed[0])
        if self.rect.right > self.field.rect.right:
            self.speed[0] = -abs(self.speed[0])

        if self.rect.top < self.field.rect.top:
            self.speed[1] = abs(self.speed[1])
        if self.rect.bottom > self.field.rect.bottom:
            self.speed[1] = -abs(self.speed[1])

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, 0)

class Pad:
    def __init__(self, keys, field):
        self.keys = keys
        self.field = field
        self.speed = [0, 0]
        self.color = GREEN
        self.rect = pygame.Rect(self.field.rect.topleft, (10, 50))

    def do(self, event):
        if event.type == KEYDOWN:
            if event.key == self.keys[0]:
                self.speed[1] = -2
            if event.key == self.keys[1]:
                self.speed[1] = 2

        elif event.type == KEYUP:
            self.speed[1] = 0
                

    def update(self):
        self.rect.move_ip(self.speed)

        if self.rect.top < self.field.rect.top:
            self.rect.top = self.field.rect.top
        if self.rect.bottom > self.field.rect.bottom:
            self.rect.bottom = self.field.rect.bottom

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, 0)

class Field:
    def __init__(self, rect):
        self.color = BLUE
        self.stroke = 2
        self.rect = pygame.Rect(rect)

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, self.stroke)



class PongDemo(App):
    """Play the game of Pong."""
    def __init__(self):
        super().__init__()
        Text('Pong', size=48)

        self.field = Field((200, 10, 400, 200))
        self.ball = Ball(self.field.rect.center, self.field)
 
        self.pad = Pad((K_UP, K_DOWN), self.field)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()

                self.pad.do(event)

            self.update()
            self.draw()

    def update(self):
        self.ball.update()
        self.pad.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.ball.draw()
        self.pad.draw()
        self.field.draw()
        pygame.display.flip()
                
if __name__ == '__main__':
    PongDemo().run()