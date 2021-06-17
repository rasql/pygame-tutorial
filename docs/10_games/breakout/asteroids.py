from app import *

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
        

class SpaceShip(Sprite):
    def __init__(self, file, pos=(0, 0), size=None):
        super().__init__(file, pos, size)
        self.angular_v0 = 1
        self.velocity = np.array((0, 0))

    def do(self, event):
        # react to events
        if event.type == MOUSEBUTTONDOWN:
            self.rect.center = event.pos

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.angular_velocity = self.angular_v0
            elif event.key == K_RIGHT:
                self.angular_velocity = -self.angular_v0
            elif event.key == K_UP:
                dx = -np.sin(np.radians(self.angle))
                dy = -np.cos(np.radians(self.angle))
                self.velocity = np.array((dx, dy))

            elif event.key == K_r:
                print('reset')
                self.velocity = np.array((0, 0))
                self.angle = 0
                self.set_pos(self.parent.rect.center)


        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                self.angular_velocity = 0
            if event.key == K_UP:
                self.velocity = np.array((0, 0))


class Bullets(Sprite):
    def __init__(self, file, pos, size):
        super().__init__(file=file, pos=pos, size=size)

        
if __name__ == '__main__':
    app = App('space.png', 'Asteroids')

    ship = SpaceShip('spaceship.png', size=(100, 100), pos=(300, 200))
    app.add(ship)

    for i in range(6):
        app.add(Asteroid('asteroid.png'))

    app.run()