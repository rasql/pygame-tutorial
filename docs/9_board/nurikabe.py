"""Nurikabe puzzle game."""
from app import *

# https://en.wikipedia.org/wiki/Nurikabe_(puzzle)
nurikabe1 = """
2........2
......2...
.2..7.....
..........
......3.3.
..2....3..
2..4......
..........
.1....2.4.
"""

# https://www.puzzles-mobile.com/nurikabe/random/5x5-easy
nurikabe2 = """
3....
.....
.....
..4.1
.2...
"""

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Nurikabe')
        n = Board(dx=20, dy=20, m=9, n=10, checker=(Color('white'), Color('white')))
        n.set_Num(nurikabe1)
        n.render()
    
        n2 = Board(dx=40, dy=40, m=5, n=5, dir=(1, 0))
        n2.set_Num(nurikabe2)
        n2.render()

if __name__ == '__main__':
    Demo().run()