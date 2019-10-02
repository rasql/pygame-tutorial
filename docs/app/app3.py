from pglib.app import *
from pglib.draw import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Scene 1', size=(500, 300))
        Text('Nodes')
        Node()
        Node()
        Node()

        Scene(bg=Color('yellow'), size=(640, 480), caption='My GREAT GAME')
        Text('Rectangle')
        Rectangle(d=0, size=(50, 50))
        Rectangle()
        Rectangle()

        Scene(bg=Color('green'))
        Text('Ellipse')
        Ellipse()
        Ellipse()
        Node()

if __name__ == '__main__':
    Demo().run()