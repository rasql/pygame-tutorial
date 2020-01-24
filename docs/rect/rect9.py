from rect import *

points = random_points(100)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_r:
                points = random_points(100)
   
    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, rect, 1)
    for p in points:
        if rect.collidepoint(p):
            pygame.draw.circle(screen, RED, p, 4, 0)
        else:
            pygame.draw.circle(screen, BLUE, p, 4, 0)
    
    pygame.display.flip()

pygame.quit()