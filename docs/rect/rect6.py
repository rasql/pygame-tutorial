from rect import *

r0 = Rect(50, 60, 200, 80)
r1 = Rect(100, 20, 100, 140)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key in dir:
                r1.move_ip(dir[event.key])

    clip = r0.clip(r1)
    union = r0.union(r1)
    
    screen.fill(GRAY)
    pygame.draw.rect(screen, YELLOW, union, 0)
    pygame.draw.rect(screen, GREEN, clip, 0)
    pygame.draw.rect(screen, BLUE, r0, 4)
    pygame.draw.rect(screen, RED, r1, 4)
    pygame.display.flip()

pygame.quit()