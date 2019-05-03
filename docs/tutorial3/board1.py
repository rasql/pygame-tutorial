import pygame
import numpy as np
from pygame.locals import *
from pygamelib import *

class Board:
    """Represents a nxm board with n rows and m columns.
    n, m    number of cells (row, column)
    i, j    index of cell (row, column)
    dx, dy  size of cell
    x0, y0  origin of first cell
    """
    def __init__(self, n=8, m=8, dx=20, dy=20, x0=0, y0=0):
        self.n = n
        self.m = m
        self.i = 0
        self.j = 0
        self.col = RED
        self.dx = 20
        self.dy = 20
        self.x0 = x0
        self.y0 = y0
        self.T = np.zeros((n, m), int)
        
    def draw(self):
        x1 = self.x0 + self.m * self.dx
        y1 = self.y0 + self.n * self.dy
        for i in range(self.n+1):
            y = self.y0 + i * self.dy
            pygame.draw.line(Game.screen, BLACK, (self.x0, y), (x1, y))
        for j in range(self.m+1):
            x = self.x0 + j * self.dx
            pygame.draw.line(Game.screen, BLACK, (x, self.y0), (x, y1))

        for i in range(self.n):
            font = pygame.font.Font(None, 24)
            for j in range(self.m):
                x = self.x0 + j * self.dx
                y = self.y0 + i * self.dy
                text = font.render(str(self.T[i, j]), True, BLACK)
                rect = text.get_rect()
                rect.center = x + self.dx//2, y + self.dy//2
                Game.screen.blit(text, rect)
        
        rect = pygame.Rect(self.get_pos(self.i, self.j), (self.dx, self.dy))
        pygame.draw.rect(Game.screen, RED, rect, 3)

    def get_pos(self, i, j):
        x = self.x0 + self.j * self.dx
        y = self.y0 + self.i * self.dy
        return x, y


class BoardDemo(Game):
    """Draw text in different sizes and colors."""
    def __init__(self):
        super(BoardDemo, self).__init__()
        Text('Board')

        self.board = Board(10, 16, x0=100, y0=10)
        print(self.board.T)
        self.objects.append(self.board)

    def on_event(self, event):
        """React to mouseclicks and keydown events."""
        d = {K_LEFT:(-1, 0), K_RIGHT:(1, 0), K_UP:(0, -1), K_DOWN:(0, 1), }
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.board.T = np.random.randint(0, 3, (self.board.n, self.board.m))
            if event.key in d:
                self.board.j += d[event.key][0]
                self.board.i += d[event.key][1]
                self.board.j = self.board.j % self.board.m
                self.board.i = self.board.i % self.board.n   

if __name__ == '__main__':
    BoardDemo().run()