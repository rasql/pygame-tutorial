#!/Users/raphael/anaconda3/bin/python3
"""
boardgames.py
Provides a framework for programming board games with Pygame.

Author: Raphael Holzer
Date:   January 2019

The Board class:
n, m    number of cells (row, column)
i, j    index of cell (row, column)
dx, dy  size of cell
x0, y0  origin of first cell

screen  display surface of main window
w, h    size of display window
title   title of display window

fps     frames per second
frame   current frame number
t0      starting time
t       current time

images  list of loaded images
sounds  list of loaded sounds
colors  list of colors

T       number matrix
C       color matrix
V       visibilty matrix
L       display object list
H       history list

event loop
quit + K_ESCAPE  quit the game

enter, mouseup -> play(board)
direction keys -> move(board)
every loop     -> loop(board)

n  ->  new(board)
r  ->  random(board)
t  ->  test(board)
"""

import pygame, os, sys
import numpy as np
from pygame.locals import *
from time import time, sleep


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (160, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 160, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 160)
DARKLBLUE = (0, 0, 160)
YELLOW = (255, 255, 0)
DARKYELLOW = (160, 160, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (127, 127, 127)
LIGHTGRAY = (200, 200, 200)
LIME = (200, 255, 0)
BEIGE = (255, 255, 127)

class Cell():
    """Represents a single cell of the board."""
    def __init__(self, i=0, j=0, k=0, col=None):
        self.i = i
        self.j = j
        self.k = k
        self.col = col
        
    def __str__(self):
        text = 'Cell ({}, {}) index {} color {}'
        return text.format(self.i, self.j, self.k, self.col)

class Board():
    """Represents a (n x m) board game."""
    dirs = dirs = {K_DOWN:(1, 0), K_UP:(-1, 0), K_RIGHT:(0, 1), K_LEFT:(0, -1)}
    
    def __init__(self, n=8, m=8, dx=20, dy=20, x0=40, y0=40, bg=WHITE, title='Board', fps=60):
        """ Create a (n, m) grid of (dx, dy)-sized tiles placed at (x0, y0). """
        self.n = n
        self.m = m
        self.dx = dx
        self.dy = dy
        self.x0 = x0
        self.y0 = y0
        self.x1 = 200
        self.y1 = y0
        self.w = x0 + m * dx + self.x1
        self.h = y0 + n * dy + self.y1
        
        self.bg = bg
        self.fps = fps
        self.frame = 0
        self.title = title
        self.pos = np.array((0, 0), dtype = int)
        self.dir = np.array((0, 0), dtype = int)
        self.active = True
        self.t0 = time()
        self.t = time() + 0.01
        #pygame.init() #makes Python crass with message: illegal instruction 4
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.font = pygame.font.SysFont('Helvetica', dy//2)
        self.font2 = pygame.font.SysFont('Helvetica', 12)
        self.fontL = pygame.font.SysFont('Helvetica', 100)
        self.text2_pos = [0, 0]
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)
        
        self.V = np.ones((n, m), dtype=int)  # Visible
        self.T = np.zeros((n, m), dtype=int) # Table
        self.C = np.zeros((n, m), dtype=int) # Color
        self.L = []
        self.p = 1

        self.grid_col = BLACK
        self.grid_d = 1
        self.grid_center = False #True for Go
        self.grid_x2 = 3
        
        self.colors = [WHITE, LIGHTGRAY]
        self.images = []
        self.sounds = []

        self.txt_col = BLACK
        
        self.cursor = True
        self.cursor_col = RED
        self.cursor_img = None
        self.cursor_val = None
        self.mouse_down = False
        self.surf_list = []
        
        #events
        self.event_type = None
        self.event_name = None
        self.event_key = None
        self.event_mod = None
        self.event_unicode = None
        
        #action functions
        self.move = lambda x : None
        self.play = lambda x : None
        self.loop = lambda x : None
        self.keys = {K_t:lambda x :print('test')}
        self.keys[K_s] = lambda x :self.show_start('Snake', YELLOW, RED)
        self.keys[K_x] = lambda x :self.show_start('Over', BLACK, BLUE)
                
        
    def __str__(self):
        text = 'Board ({}, {}) of {}'
        return text.format(self.n, self.m, self.title)

    def show_text(self, txt, col=YELLOW, bg=None):
        """Show large rotating title text."""
        self.textL = self.fontL.render(txt, True, col, bg)
        self.textL2 = self.fontL.render(txt, True, WHITE, bg)
        phi = 0
        t0 = time()
        while time() < t0 + 3:
            surf = pygame.transform.rotate(self.textL, phi)
            surf2 = pygame.transform.rotate(self.textL2, -phi)
            rect = surf.get_rect()
            rect.center = (self.w//2, self.h//2)
            self.screen.blit(surf, rect)
            self.screen.blit(surf2, rect)           
            pygame.display.update()
            phi += 2

    def show_info(self):
        """Displays game info on the side."""
        x = self.x0 + self.m * self.dx + 20
        y = self.y0
        self.draw_text2('t={:.2f}'.format(self.t - self.t0), x, y)
        self.draw_text2('frame={}'.format(self.frame))
        self.draw_text2('fps={:.1f}'.format(self.frame/(self.t - self.t0)))
        self.draw_text2('pos={}'.format(self.pos))
        self.draw_text2('dir={}'.format(self.dir))
        self.draw_text2('type={}'.format(self.event_type))
        self.draw_text2('name={}'.format(self.event_name))
        self.draw_text2('key={}'.format(self.event_key))
        self.draw_text2('mod={}'.format(self.event_mod))
        self.draw_text2('unicode={}'.format(self.event_unicode))
        
    def game_over(self):
        self.show_text('Game Over')
        
    def set_grid(self, col=BLACK, d=1, center=False, x2=3):
        """Set grid parameters."""
        self.grid_col = col##        board.draw_text2(board.n, 1, 'frame={}'.format(board.frame))
##        board.draw_text2(board.n, 2, 'fps={:.1f}'.format(board.frame/(board.t - board.t0)))
##        board.draw_text2(board.n, 3, 'pos={}'.format(board.pos))
##        board.draw_text2(board.n, 4, 'dir={}'.format(board.dir))                
        self.grid_d = d
        self.grid_center = center
        self.grid_x2 = x2

    def load_images(self, folder):
        """Load images from a folder."""
        cwd = os.getcwd()
        dir = cwd + '/' + folder
        files = os.listdir(dir)
        for file in files:
            img = pygame.image.load(dir + '/' + file)
            self.images.append(img)
    
    def load_sounds(self, folder):
        """Load sounds from a folder."""
        pygame.mixer.init()
        cwd = os.getcwd()
        dir = cwd + '/' + folder
        files = os.listdir(dir)
        for file in files:
            snd = pygame.mixer.Sound(dir + '/' + file)
            self.sounds.append(snd)

    def set_T(self, T):
        """Set the integer matrix T."""
        self.T = T

    def shuffle_T(self):
        """Shuffles the values of T."""
        np.random.shuffle(self.T)

    def init_T(self, k):
        """Inizialize T with zeros (0), range (1), pairs (2)."""
        if k == 0:
            self.T = np.zeros((self.n, self.m), dtype=int)
        elif k == 1:
            self.T = np.arange(self.n * self.m, dtype=int)
            self.T = np.reshape(self.T, (self.n, self.m))
        elif k == 2:
            self.T = np.array(list(range( (self.n * self.m) // 2)) * 2, dtype=int)
            self.T = np.reshape(self.T, (self.n, self.m))

    def set_C(self):
        """Set checkerboard pattern."""
        for i in range(self.n):
            for j in range(self.m):
                self.C[i, j] = (i + j) % 2

    def get_rect(self, i, j):
        """Return a Rect object for the tile [i, j]."""
        x = self.x0 + j * self.dx
        y = self.y0 + i * self.dy
        return Rect(x, y, self.dx, self.dy)
    
    def get_index(self, x, y):
        """Return index [i, j] from pixel position (x, y)."""
        i = (y - self.y0) // self.dy
        j = (x - self.x0) // self.dx
        i = min(max(i, 0), self.n-1)
        j = min(max(j, 0), self.m-1)
        return [i, j]
    
    def get_random_pos(self):
        """Return a random tuple (i, j)."""
        i = np.random.randint(self.n)
        j = np.random.randint(self.m)
        return [i, j]
        
    def draw_bg(self):
        """Draw the background color."""
        self.screen.fill(self.bg)
    
    def draw_grid(self):
        """Draw the vertical and horizontal grid lines."""
        if self.grid_center == True:
            (n, m) = (self.n, self.m)
            (dx, dy) = (self.dx // 2, self.dy // 2)
        else:
            (n, m) = (self.n + 1, self.m + 1)
            (dx, dy) = (0, 0)

        x0 = self.x0 + dx
        y0 = self.y0 + dy

        # vertical lines
        for j in range(m):
            p0 = (x0 + j * self.dx, y0)
            p1 = (x0 + j * self.dx, y0 + (n-1) * self.dy)
            pygame.draw.line(self.screen, self.grid_col, p0, p1, self.grid_d)       
        # horizontal lines
        for i in range(n):
            p0 = (x0, y0 + i * self.dy)
            p1 = (x0 + (m-1) * self.dx, y0 + i * self.dy)
            pygame.draw.line(self.screen, self.grid_col, p0, p1, self.grid_d)  
 
    def draw_rect(self, i, j, col, d=0):
        """Draw a colored tile at position [i, j]."""
        pygame.draw.rect(self.screen, col, self.get_rect(i, j), d)

    def draw_rects(self, L, col):
        """Draw colored tile from a list L."""
        for (i, j) in L:
            self.draw_rect(i, j, col)

    def draw_text(self, i, j, text, col, bg=None):
        """Draw text at position [i, j]."""
        txt = self.font.render(text, True, col, bg)
        rect = txt.get_rect()
        rect.center = self.get_rect(i, j).center
        self.screen.blit(txt, rect)
        
    def draw_text2(self, text, x=None, y=None, col=BLACK, bg=None):
        """Draw small text."""
        self.text2_pos[1] += 20
        if x != None:
            self.text2_pos[0] = x
        if y != None:
            self.text2_pos[1] = y
        txt = self.font2.render(text, True, col, bg)
        rect = txt.get_rect()
        rect.topleft = self.text2_pos
        self.screen.blit(txt, rect)
 
    def draw_C(self):
        """Draw colors."""
        for i in range(self.n):
            for j in range(self.m):
                col = self.C[i, j]
                if col > 0:
                     self.draw_rect(i, j, self.colors[col], 0)
                        
    def draw_T(self):
        """Draw the number matrix T."""
        for i in range(self.n):
            for j in range(self.m):
                t = self.T[i, j]
                if t != 0 and self.V[i, j] == 1:
                    if len(self.images) > 0:
                        self.draw_img(i, j, t)
                    else:
                        self.draw_text(i, j, str(t), BLACK)                    

    def draw_img(self, i, j, k):
        """Draw image k at tile [i, j]."""
        if k < len(self.images):
            img = self.images[k]
            r = self.get_rect(i, j)
            self.screen.blit(img, r)

    def update(self):
        """Update the display and wait for the next tick."""
        self.t = time()
        self.frame += 1
        self.loop(self)
        self.draw_bg()
        self.draw_C()
        if self.cursor:
            self.draw_rect(*self.pos, RED, 2)
        self.draw_grid()
        self.draw_T()
        self.show_info()
        for (surf, rect) in self.surf_list:
            self.screen.blit(surf, rect)
        pygame.display.update()
        self.clock.tick(self.fps)

    def do_event(self, event):
        """Decode quit event, arrow key and mouse events."""
        self.event = event
        self.event_type = event.type
        self.event_name = pygame.event.event_name(event.type)
        self.surf_list = []
        if event.type == QUIT:
            self.active = False
            
        elif event.type == KEYDOWN:
            self.event_key = event.key
            self.event_mod = event.mod
            self.event_unicode = event.unicode
            if event.key == K_ESCAPE:
                self.active = False
            elif event.key == K_RETURN:
                self.play(self)
                
            elif event.key in self.dirs:
                self.dir = np.array(self.dirs[event.key])
                self.pos += self.dir
                 
                self.pos[0] = min(max(self.pos[0], 0), self.n-1)
                self.pos[1] = min(max(self.pos[1], 0), self.m-1)
                self.move(self)
            elif event.key in self.keys:
                self.keys[event.key](self)
 
        elif event.type == MOUSEMOTION:
            self.event_pos = event.pos
            self.event_rel = event.rel
            self.pos = self.get_index(*event.pos)
            if self.mouse_down:
                (x, y) = event.pos
                x -= self.dx//2
                y -= self.dy//2
                self.surf_list.append((self.cursor_img, (x, y)))
                
        elif event.type == MOUSEBUTTONDOWN:
            self.mouse_down = True
            (i, j) = self.get_index(*event.pos)
            t = self.T[i, j]
            if t != 0 and len(self.images)>0:
                self.cursor_img = self.images[t]
                self.T[i, j] = 0
                self.cursor_val = t
                
        elif event.type == MOUSEBUTTONUP:
            self.mouse_down = False
            (i, j) = self.get_index(*event.pos)
            self.pos = [i, j]         
            t = self.T[i, j]
            if t == 0 and len(self.images) > 0:
                self.T[i, j] = self.cursor_val
            self.play(self)
            
## ---------------------------------------------------------------
def set_game(game):
    if game == 'go':
        def play(board):
            i, j = board.pos
            t = board.T[i, j]
            if t == 0:
                board.T[i, j] = board.p
                board.p = 3 - board.p
                board.L.append((i, j))
           
        board = Board(19, 19, 40, 40, 40, 40, BEIGE, 'Go')
        board.grid_center = True
        board.play = play        

    elif game == 'chess':
        board = Board(8, 8, 100, 100, 50, 50, WHITE, 'Chess')
        board.set_C()
        T = np.array([  [3, 5, 7, 9,11, 7, 5, 3],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [4, 6, 8,10,12, 8, 6, 4]])
        board.set_T(T)
        board.load_images('chess')
        #board.show_text('Chess', YELLOW, RED)

    elif game == 'sudoku':
        board = Board(9, 9, 50, 50, 25, 25, WHITE, 'Sudoku')
        T = np.array([  [5, 3, 0, 0, 7, 0, 0, 0, 0],
                        [6, 0, 0, 1, 9, 5, 0, 0, 0],
                        [0, 9, 8, 0, 0, 0, 0, 6, 0],
                        [8, 0, 0, 0, 6, 0, 0, 0, 3],
                        [4, 0, 0, 8, 0, 3, 0, 0, 1],
                        [7, 0, 0, 0, 2, 0, 0, 0, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 0],
                        [0, 0, 0, 4, 1, 9, 0, 0, 5],
                        [0, 0, 0, 0, 8, 0, 0, 7, 9]])
        board.set_T(T)
        
    elif game == 'simon':
        def show(board, k):
            """Show cell i."""
            (i, j) = (k//2, k%2)
            col = board.colors[k+4+1]
            board.draw_rect(i, j, col)
            board.sounds[k-1].play()
            pygame.display.update()
            sleep(0.2)
            col = board.colors[k+1]
            board.draw_rect(i, j, col)
            pygame.display.update()
            
        def play(board):
            i = board.pos[0] * 2 + board.pos[1]
            show(board, i)
       
        def random(board):
            board.L.append(np.random.randint(1, 4))
            print(board.L)
            for k in board.L:
                show(board, k)
                sleep(0.3)
                          
        board = Board(2, 2, 200, 200, 100, 50, WHITE, 'Simon')
        board.load_sounds('simon')
        board.C = np.array([[1, 2], [3, 4]])
        board.colors = [WHITE, DARKRED, DARKGREEN, DARKBLUE, DARKYELLOW, RED, GREEN, BLUE, YELLOW]
        board.play = play
        board.L = [np.random.randint(0, 4)]
        board.keys[K_r] = random
        random(board)
        board.i = 0
        
    elif game == 'snake':
        def loop(board):
            head = board.snake[-1].copy()
            head += board.dir
            print(type(head), type(board.snake))
             
            if list(head) in board.snake:
  #              board.show_text('Over', YELLOW, RED)
                pass
                
            board.snake.append(head)            
            if head == board.apple:
                board.apple = board.get_random_pos()
            else:
                board.snake.pop(0)
            board.draw_rect(*board.apple, RED)
            board.draw_rects(board.snake, GREEN)
            
        def random(board):
            board.apple = board.get_random_pos() 

        board = Board(15, 20, 30, 30, 40, 40, LIME, 'Snake', 5)
        board.loop = loop
        board.apple = board.get_random_pos()
        board.snake = [board.get_random_pos()]
        print(board.apple, board.snake)
        board.keys[K_r] = random
        #board.show_text('Snake', YELLOW, RED)
       
    elif game == 'puzzle':
        def play(board):
            i, j = board.pos
            L = board.L
            if board.V[i, j] == 0:
                board.V[i, j] = 1
            board.L.append((i, j))
            if len(board.L) > 2 :
                if board.T[L[0]] != board.T[L[1]]:
                    board.V[L[0]] = 0
                    board.V[L[1]] = 0
                board.L = [(i, j)]
            
        board = Board(6, 8, 80, 80, 40, 40, YELLOW, 'Memory Puzzle')
        board.V = np.zeros((board.n, board.m), dtype=int)
        board.init_T(2)
        board.shuffle_T()
        board.play = play
        
    elif game == 'slide':
        def play(board):
            pos = list(board.T.flatten()).index(0)
            (i0, j0) = pos // board.m, pos % board.m
            i = i0 - board.dir[0]
            j = j0 - board.dir[1]           
            if 0 <= i < board.n and 0 <= j < board.m:
                (board.T[i, j], board.T[i0, j0]) = (board.T[i0, j0], board.T[i, j]) 
            
        board = Board(4, 4, 100, 100, 20, 20, WHITE, 'Sliding Puzzle')
        board.init_T(1)
        board.shuffle_T()
        board.move = play
 #       board.keys[K_q] = lamda board:
        
    return board

def slide(board):
    (i, j) = board.pos
    print(i, j)
    print(board.dir)
    print(board.cursor_img)
    r = board.get_rect(i, j)
    for i in range(board.dx):
        r.move_ip(1, 0)
        board.screen.blit(board.cursor_img, r)
        pygame.display.update()
        sleep(0.01)
 
def test(board):
    c = Cell(1, 2, 3, RED)
    print(c)
    print(board)
 
def main():
    """Test the boardgame library functions."""
    
    games = 'chess simon puzzle chess go slide go sudoku snake'.split()
    gi = 0
    game = games[gi]
    board = set_game(game)
    board.keys[K_t] = test
    
    while board.active:
        for event in pygame.event.get():
            board.do_event(event)
            if event.type == KEYDOWN:
                if event.key == K_g:
                    gi = (gi + 1) % len(games)
                    board = set_game(games[gi])
                     
        board.update()
        
    pygame.quit()

if __name__ == '__main__':
    main()