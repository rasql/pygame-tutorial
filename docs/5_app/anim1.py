"""Animation: bouger"""

from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Images')
        Node(bg=Color('white'), size=(80, 80), dir=(1, 0))
        Node(file='animals/bird-icon.png')
        Node(file='animals/black-cat-icon.png')
        Node(file='animals/bunny-icon.png', border_col=Color('red'))
        Node(file='animals/gold-fish-icon.png', bg=Color('white'))
        Node(file='animals/cow-icon.png')

if __name__ == '__main__':
    Demo().run()