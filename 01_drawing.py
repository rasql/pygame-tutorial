# Import the game library
import pygame


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

PI = 3.1415


# Initialize the game engine
pygame.init()

# Open a window
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("PyGame")


done = False
clock = pygame.time.Clock()

# --- main loop ---
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print('User pressed the key', event.key, chr(event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('User pressed a mouse button')
    
    screen.fill(WHITE)
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()