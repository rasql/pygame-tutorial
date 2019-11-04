"""Sudoko puzzle game."""
from app import *

# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
sudoku1 = """
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
"""

# https://www.theguardian.com/lifeandstyle/2018/apr/16/sudoku-easy-4035
sudoku2 = """
8769.....
.1...6...
.4.3.58..
4.....21.
.9.5.....
.5..4.3.6
.29.....8
..469.17334
.....1..4
"""

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Sudoku')
        s = Sudoku(dx=20, dy=20)
        s.set_Num(sudoku1)
        s.render()

        Button('Reset', dir=(1, 0), cmd='print(123)')
        # s2 = Sudoku(dir=(1, 0))
        # s2.set_Num(sudoku2)

        

if __name__ == '__main__':
    Demo().run()