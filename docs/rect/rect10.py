from rect import *

n = 50
rects = random_rects(n)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key == K_r:
                rects = random_rects(n)
   
    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, rect, 1)

    for r in rects:
        if rect.colliderect(r):
            pygame.draw.rect(screen, RED, r, 2)
        else:
            pygame.draw.rect(screen, BLUE, r, 1)
    
    pygame.display.flip()

pygame.quit()