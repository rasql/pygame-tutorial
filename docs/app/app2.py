from pg_app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene()
        Text('Nodes')
        Node()
        Node()
        Text('Game')
        Node()

        Scene(bg=Color('yellow'))
        Text('Game')
        Node()
        Node()
        Node()

        Scene(bg=Color('green'))
        Text('Game Over')
        Node()
        Node()
        Node()

if __name__ == '__main__':
    Demo().run()