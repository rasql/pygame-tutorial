"""Text with size, alignment, fontcolor, font background..."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Text', bg=Color('pink'))
        Text(size=(100, 40))
        Text(bg=Color('yellow'), h_align=1)
        Text(fontcolor=Color('red'))
        Text(fontbg=Color('green'), cmd='print(self.text)')

        Text(pos=(200, 20))
        Text(italic=True, v_align=1)
        Text(underline=True, fontsize=24)
        Text(bold=True)
        
if __name__ == '__main__':
    Demo().run()