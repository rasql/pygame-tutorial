"""Display different scene background images."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(img_folder='../background', file='forest.jpg', caption='Forest')
        Text('Forest scene', fontcolor=Color('white'))
        Scene(file='lake.jpg', caption='Lake')
        Text('Lake scene')
        Scene(file='sunset.jpg', caption='Sunset')
        Text('Sunset scene', fontcolor=Color('white'))
        Scene(file='', bg=Color('lightgreen'), caption='Green background')
        Text('Colored background scene')

if __name__ == '__main__':
    Demo().run()