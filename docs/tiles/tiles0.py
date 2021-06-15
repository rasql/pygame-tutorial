import pygame

file = 'tmw_desert_spacing.png'
image = pygame.image.load(file)
rect = image.get_rect()
print(image)

pygame.init()
screen = pygame.display.set_mode(rect.size)

screen.blit(image, rect)
pygame.display.update()

while True:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()