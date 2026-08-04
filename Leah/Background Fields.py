import pygame
pygame.init()
pygame.display.set_caption('Penguine Runner')
running = True

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
TOP_COLOR = (135, 206, 235)    
BOTTOM_COLOR = (144, 238, 144)  
TOP_HEIGHT = (HEIGHT * 3) // 4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.draw.rect(screen, TOP_COLOR, (0, 0, WIDTH, TOP_HEIGHT))
    
    
    pygame.draw.rect(screen, BOTTOM_COLOR, (0, TOP_HEIGHT, WIDTH, HEIGHT - TOP_HEIGHT))

  
    pygame.display.flip()

pygame.quit()