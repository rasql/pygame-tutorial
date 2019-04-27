"""Choose the RGB components of the background color 
by pressing the R, G, and B keys ."""

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        self.red = 200
        self.green = 100
        self.blue = 100
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
                        self.red += 10
                        self.red %= 256
                    elif event.key == pygame.K_g:
                        self.green += 10
                        self.green %= 256
                    elif event.key == pygame.K_b:
                        self.blue += 10
                        self.blue %= 256

            self.str = 'R={}, G={}, B={}'.format(self.red, self.green, self.blue)
            self.text = self.font.render(self.str, False, BLACK)
            self.screen.fill((self.red, self.green, self.blue))
            self.screen.blit(self.text, (20, 20))
            pygame.display.flip()

if __name__ == '__main__':
  Game().run()