"""Configure App with size and shortcut options."""

from app import *

class Demo(App):
    def __init__(self):
        super().__init__(size=(800, 600), shortcuts={(K_1, KMOD_NONE): 'print(123)'})
        Scene()
        Scene(bg=Color('yellow'))

if __name__ == '__main__':
    Demo().run()