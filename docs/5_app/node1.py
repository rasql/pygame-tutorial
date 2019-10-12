from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Nodes - vertical placement')
        Node()
        Node()
        Node()

        Node(pos=(200, 20), size=(200, 50), color=Color('blue'), d=3)
        Node()
        Node()

        Scene(caption='Nodes - horizontal placement')
        Node(dir=(1, 0), pos=(0, 0), gap=(0, 0))
        Node()
        Node()

        Node(pos=(0, 100), color=Color('green'))
        Node()
        Node()

        Scene(caption='Nodes - diagonale placement')
        Node(dir=(1, 1), gap=(0, 0))
        Node()
        Node()

if __name__ == '__main__':
    Demo().run()