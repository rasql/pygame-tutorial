"""Create a game of pong."""
from app import *

class Ball(Node):
    def __init__(self):
        speed = [1, 1]

class Pong(Node):
    def __init__(self, **options):
        super().__init__(**options)
        self.dx = 1
        self.dy = 1
        self.ball = Node(pos=self.rect.center, size=(20, 20), bg=Color('blue'))

    def update(self):
        b = self.ball.rect
        f = self.rect
        b.move_ip((self.dx, self.dy))
        if b.top < f.top or b.bottom > f.bottom:
            self.dy *= -1
        if b.left < f.left or b.right > f.right:
            self.dx *= -1

    def draw(self):
        pygame.draw.rect(App.screen, Color('red'), self.rect, 2)
        self.ball.draw()
        Node.draw(self)

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(caption='PONG')
        Pong(size=(300, 200))

if __name__ == '__main__':
    Demo().run()