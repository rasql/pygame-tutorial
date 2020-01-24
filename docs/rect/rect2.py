from rect import *

pts = ('topleft', 'topright', 'bottomleft', 'bottomright',
        'midtop', 'midright', 'midbottom', 'midleft', 'center')

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, rect, 4)
    for pt in pts:
        pos = eval('rect.'+pt)
        draw_text(pt, pos)
        pygame.draw.circle(screen, RED, pos, 3)

    pygame.display.flip()

pygame.quit()