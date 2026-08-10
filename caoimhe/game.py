import pygame
import sys
from os.path import join
# Initialise Pygame
pygame.init()



# Screen settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 500
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Runner")

# Load background
background = pygame.image.load(join("caoimhe", "Images", "desert_background.png.png")).convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Background scrolling
bg_x = 0
scroll_speed = 4  # Increase for faster scrolling

clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # Move background
    bg_x -= scroll_speed

    # Reset position
    if bg_x <= -WINDOW_WIDTH:
        bg_x = 0

    # Draw two backgrounds
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WINDOW_WIDTH, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()