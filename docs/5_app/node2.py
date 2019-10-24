
"""Nodes with color, border and image."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Nodes with color, border, image')
        Node(level=1, size=(100, 30), border_col = Color('cyan'), border_thick=1)
        Node(border_thick = 2, bg=(255, 0, 0, 127))
        Node(border_thick = 4)
        Node(color=Color('orange'))
        Node(file='background/forest.jpg')

        Node(file='', bg=Color('yellow'), pos=(200,20), size=(100, 100))
        Node(size=(100, 50))
        Node()

if __name__ == '__main__':
    Demo().run()