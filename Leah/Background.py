import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT =1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Penguine Runner')
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('yellow')

    pygame.display.update()
 
pygame.quit()



