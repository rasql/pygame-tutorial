"""Display buttons with different size, color and font."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(caption='Button')
        Button('Button', cmd='print(self)')
        Button('Scene', cmd='print(App.scene)')
        Button('Size', size=(100, 100))
        Button('Color', button_color=Color('red'))
        Button('Border', border_color=Color('blue'))
        
if __name__ == '__main__':
    Demo().run()