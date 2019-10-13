
"""Embedded Nodes"""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Nodes - vertical placement')
        Node(size=(200, 100))
        Node(size=(50, 50))
        Node()



if __name__ == '__main__':
    Demo().run()