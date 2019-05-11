"""Display the mouse position as a label and 
move the label position with the mouse."""

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 48)
        self.str = '(0, 0)'
        self.pos = (0, 0)
        self.screen = pygame.display.set_mode((640, 240))

    def run(self):
        """Run the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    self.str = '({}, {})'.format(*event.pos)
                    self.pos = event.pos

            self.text = self.font.render(self.str, False, WHITE)
            self.screen.fill(BLACK)
            self.screen.blit(self.text, self.pos)
            pygame.display.flip()

if __name__ == '__main__':
  Game().run()