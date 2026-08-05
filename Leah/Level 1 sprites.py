import pygame
import sys
from os.path import join
from random import randint, uniform

#classes
class Catus(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center = pos)

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

#import
catus_surf = pygame.image.load(join('Leah', 'Happy Catus.png')).convert_alpha()

#sprites
all_sprites = pygame.sprite.Group()
catus_sprites = pygame.sprite.Group()

catus_event = pygame.event.custom_type()
running = True


while running:
    dt = clock.tick() / 1000
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



    #sprites
    all_sprites.update(dt)
    all_sprites.draw(screen)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()