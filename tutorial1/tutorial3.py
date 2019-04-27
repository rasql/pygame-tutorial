import pygame

class Game():
    """Is the main game object."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 240))

    def run(self):
        """Runs the main event loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

if __name__ == '__main__':
  Game().run()