from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Nodes - vertical placement')
        Node()
        Node()
        Node()

        Node(pos=(200, 20), size=(200, 50))
        Node()
        Node()

        Scene(caption='Nodes - horizontal placement')
        Node(dir=(1, 0), gap=(0, 0))
        Node()
        Node()

        Node(pos=(20, 100)
        Node()
        Node()

        Scene(caption='Nodes - diagonal placement')
        Node(dir=(1, 1), gap=(0, 0))
        Node()
        Node()

if __name__ == '__main__':
    Demo().run()