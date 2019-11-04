"""Image puzzle."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__(size=(640, 580))

        Scene(caption='Photo puzzle')    
        Puzzle(file='../../images/cat.jpg', div=(4, 4))
        Puzzle(file='../../images/sunset.jpg', pos=(20, 300))
 
if __name__ == '__main__':
    Demo().run()