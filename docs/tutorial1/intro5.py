"""Display a red text on the screen."""

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 48)
        s = 'Hello world.'
        self.text = self.font.render(s, False, RED)
        self.screen = pygame.display.set_mode((640, 240))

    def run(self):
        """Run the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            self.screen.blit(self.text, (20, 20))
            pygame.display.flip()

if __name__ == '__main__':
  Game().run()