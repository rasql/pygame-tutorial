"""Display text in different size, color and font."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(caption='Text')
        Text('Default text')
        Text('fontsize = 24', fontsize=24)
        Text('fontcolor = RED', fontcolor=Color('red'))
        Text('48 pts, blue', fontsize=48, fontcolor=Color('blue'))
        Text('background = yellow', background=Color('yellow'))

        Text('italic', pos=(400, 20), italic=True)
        Text('bold', bold=True)
        Text('underline', underline=True, font_bg=None)

if __name__ == '__main__':
    Demo().run()