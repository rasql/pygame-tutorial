"""Horizontal and vertical text alignement."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Text Alignment', bg=Color('pink'))
        Text('left', size=(200, 40), fontsize=24)
        Text('center', h_align=1)
        Text('right', h_align=2)
        Text(bg=Color('blue'), fontcolor=Color('white'))
        
        Text('top', pos=(250, 20), h_align=1)
        Text('middle', v_align=1)
        Text('bottom', v_align=2)
        
if __name__ == '__main__':
    Demo().run()