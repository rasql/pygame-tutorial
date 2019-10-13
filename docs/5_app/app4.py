from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(file='background/forest.jpg', caption='Forest')
        Text('Forest scene', fontcolor=Color('white'))
        Scene(file='background/lake.jpg', caption='Lake')
        Text('Lake scene')
        Scene(file='background/sunset.jpg', caption='Sunset')
        Text('Sunset scene', fontcolor=Color('white'))
        Scene(file='', bg=Color('lightgreen'), caption='Green background')
        Text('Colored background scene')

if __name__ == '__main__':
    Demo().run()