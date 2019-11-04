"""Simple board game."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Board Game')
        Board(dir=(1, 0))
        Board()
        Board()

if __name__ == '__main__':
    Demo().run()