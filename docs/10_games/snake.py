"""Template for making games."""

import pygame
from pygame.locals import *
from pygamelib import *

class Snake(Shape):
    """Represent the snake as a list of coordinates."""
    def __init__(self, board):
        super(Snake, self).__init__()
        self.board = board
        self.snake = [[0, 0], [1, 0], [2, 0]]
        self.dir = 0

    def draw(self):
        for index in self.snake:
            self.board.fill(index, GREEN)
    
    def on_key(self, event):
        print(event)
        d = {K_UP:0, K_DOWN:0, K_LEFT:0, K_RIGHT:0}
        if event.key in d:
            print(event)

class SnakeDemo(App):
    """Make a subclass of the Game class."""
    def __init__(self):
        super(SnakeDemo, self).__init__()
        Text('Snake', size=48, bgcolor=CYAN)
        Text('Eat the apples', size=24)
        
        board = Board(10, 20, pos=(200, 10))
        Snake(board)

if __name__ == '__main__':
    SnakeDemo().run()