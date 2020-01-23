from rect import *

rect = Rect(100, 50, 50, 50)
v = [2, 2]

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    rect.move_ip(v)

    if rect.left < 0:
        v[0] *= -1
    if rect.right > width:
        v[0] *= -1
    if rect.top < 0:
        v[1] *= -1
    if rect.bottom > height:
        v[1] *= -1
   
    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, rect)
    pygame.display.flip()

pygame.quit()