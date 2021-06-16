from app import *

class SpaceShip(Sprite):
    def __init__(self, file, pos=(0, 0), size=None):
        super().__init__(file, pos, size)

    def do(self, event):
        # react to events
        if event.type == MOUSEBUTTONDOWN:
            self.rect.center = event.pos


class Asteroid(Sprite):
    def __init__(self, file):
        
        self.position = np.random.rand(2) * 1000
        n = np.random.randint(10, 100)
        self.size = (n, n)
        super().__init__(file, self.position, self.size)

        self.velocity = (np.random.rand(2) - 0.5) * 5
        self.angular_velocity = (np.random.rand(1) - 0.5) * 2
 

    def update(self):
        self.move()    

        w, h = self.parent.rect.size
        self.position[0] %= w + self.rect.w
        self.position[1] %= h + self.rect.h

        self.rect.center = self.position
        
        
if __name__ == '__main__':
    app = App('space.png', 'Asteroids')

    ship = Sprite('spaceship.png', size=(100, 50), pos=(300, 200))
    app.add(ship)
    for i in range(6):
        app.add(Asteroid('asteroid.png'))

    app.run()