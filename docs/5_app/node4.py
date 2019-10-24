
"""Nodes which change stacking order."""
from app import *

class Demo(App):
    def __init__(self): 
        super().__init__()
        
        Scene(caption='visible, movable, resizable')
        Text('visible')
        Text('not visible', visible=False)
        Text('not movable', visible=True, movable=False)
        Text('not movable, not resizable', resizable=False)

if __name__ == '__main__':
    Demo().run()