"""Chess game."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__(size=(640, 480))
        
        Scene(caption='Chess')
        Chess(folder='chess')

if __name__ == '__main__':
    Demo().run()