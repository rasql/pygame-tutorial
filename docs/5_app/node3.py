
"""Nodes which change stacking order."""
from app import *

class Demo(App):
    def __init__(self): 
        super().__init__()
        
        Scene(caption='Stacking order')
        Node(size=(100, 100), pos=(10, 10), dir=(0.2, 0.2), bg=Color('yellow'))
        Node(bg=Color('blue'))
        Node(bg=Color('red'))
        Node(bg=Color('green'))

if __name__ == '__main__':
    Demo().run()