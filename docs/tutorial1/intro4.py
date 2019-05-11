"""This program changes the background color 
between red, green and blue"""

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game():
    """Is the main game object."""
    def __init__(self):
        pygame.init()
        self.color = BLACK
        self.screen = pygame.display.set_mode((640, 240))

    def run(self):
        """Runs the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.color = RED
                    elif event.key == pygame.K_g:
                        self.color = GREEN
                    elif event.key == pygame.K_b:
                        self.color = BLUE

            self.screen.fill(self.color)
            pygame.display.flip()

if __name__ == '__main__':
  Game().run()