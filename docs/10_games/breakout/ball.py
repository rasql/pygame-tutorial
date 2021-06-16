# App with a bouncing ball

from app import *

class Ball:
    def __init__(self, file=None, size=(50, 50)):
        self.rect = Rect(50, 50, 20, 20)
        self.color = 'red'
        self.speed = [2, 1]
        if file:
            self.image = pygame.image.load(file)
            self.image = pygame.transform.scale(self.image, size)
        else:
            self.image = pygame.Surface(self.rect.size)
            self.image.fill(self.color)
            
    def do(self, event):
        # react to events
        if event.type == MOUSEBUTTONDOWN:
            self.rect.center = event.pos

    def update(self):
        # move or interact with other objects
        self.rect.move_ip(self.speed)
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        
if __name__ == '__main__':
    app = App()
    ball = Ball('pokemon-ball.png')
    app.add(ball)
    app.run()