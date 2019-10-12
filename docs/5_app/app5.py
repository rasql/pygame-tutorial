from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(file='animals/bird-icon.png', caption='Bird', )
        Scene(file='animals/cat-icon.png', caption='Cat')
        Node()
        Scene(file='animals/bunny-icon.png', caption='Bunny')
        Node()
        Scene(bg=Color('lightgreen'), caption='Green')
        Node()

if __name__ == '__main__':
    Demo().run()