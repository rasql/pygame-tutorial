import pygame
from pygame.locals import *
from pygamelib import *

class Game():
    """Define the main game object and its attributes."""
    def __init__(self):
        pygame.init()
        self.bg = YELLOW
        self.str = 'arrow : move, alt+arrow : resize, key : color, alt+key : bg color'
        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((640, 240))
        self.rect = pygame.Rect(100, 100, 200, 50)
        self.col = BLUE

    def run(self):
        """Run the main event loop."""
        color = {K_r:RED, K_b:BLUE, K_g:GREEN, K_m:MAGENTA, 
            K_c:CYAN, K_y:YELLOW, K_k:BLACK, K_w:WHITE}
        d = {K_UP:(0, -10), K_DOWN:(0, 10), K_LEFT:(-10, 0), K_RIGHT:(10, 0)}
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in d:
                        vec = d[event.key]
                        if event.mod & KMOD_ALT:
                            self.rect.inflate_ip(vec)
                        else:
                            self.rect.move_ip(vec)
                    elif event.key in color:
                        if event.mod & KMOD_ALT:
                            self.bg = color[event.key]
                        else:
                            self.col = color[event.key]

            self.draw()

    def draw(self):
        self.screen.fill(self.bg)
        self.text = self.font.render(self.str, True, BLACK)
        self.screen.blit(self.text, (10, 10))
        pygame.draw.rect(self.screen, self.col, self.rect)
        pygame.display.flip()

if __name__ == '__main__':
  Game().run()