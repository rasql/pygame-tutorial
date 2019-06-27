from pg_app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene()
        Text('Nodes')
        Node()
        Node()
        Node()

        Scene(bg=Color('yellow'))
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