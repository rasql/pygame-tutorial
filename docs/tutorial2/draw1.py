"""Draw text, rectangles and a circle."""

import pygame
from pygamelib import *

class App():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        self.bg = RED
        self.str = 'Hello world.'
        self.font = pygame.font.Font(None, 48)
        self.screen = pygame.display.set_mode((640, 240))

    def run(self):
        """Run the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print('R')
            self.draw()

    def draw(self):
        self.screen.fill(self.bg)
        self.text = self.font.render(self.str, False, BLACK)
        self.screen.blit(self.text, (20, 20))
        pygame.draw.rect(self.screen, BLUE, (100, 100, 200, 100))
        pygame.draw.rect(self.screen, GREEN, (400, 100, 50, 100))
        pygame.draw.circle(self.screen, YELLOW, (100, 100), 50)
        
        pygame.display.flip()

if __name__ == '__main__':
  App().run()