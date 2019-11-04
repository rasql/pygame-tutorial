"""Template for making applications."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='My application')
        Node()
        Text()
        Button()
        
if __name__ == '__main__':
    Demo().run()