import pygame
import sys
from os.path import join
from random import randint, uniform


class Cactus(pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups):
         super().__init__(groups)
         self.original_surf = surf
         self.image = surf
         self.rect = self.image.get_rect(center=pos)
         self.pos = pygame.math.Vector2(self.rect.topleft)
         self.start_time = pygame.time.get_ticks()
         self.lifetime = 4000
         self.speed = 600  # Adjust to match the game's scrolling speed

        def update(self, dt):
            self.pos.x -= self.speed * dt
            self.rect.x = round(self.pos.x)
            if self.rect.right < -250:
                self.kill()

# Initialise Pygame
pygame.init()



# # Screen settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 500
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Runner")

# # Load background
background = pygame.image.load(join("caoimhe", "Images", "desert_background.png.png")).convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# # Background scrolling
bg_x = 0
scroll_speed = 10 # Increase for faster scrolling

clock = pygame.time.Clock()

# #import
cactus_surf = pygame.image.load(join('Leah', 'Cactus.png')).convert_alpha()
cactus_surf = pygame.transform.scale(cactus_surf, (250, 250))

# #sprites
all_sprites = pygame.sprite.Group()
cactus_sprites = pygame.sprite.Group()

cactus_event = pygame.event.custom_type()
pygame.time.set_timer(cactus_event, 900)
running = True


while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == cactus_event:
         x = WINDOW_WIDTH + randint(200, 1000)
         y = 375
         Cactus(cactus_surf, (x, y), (all_sprites, cactus_sprites))
    
#      # Move background
    bg_x -= scroll_speed

#     # Reset position
    if bg_x <= -WINDOW_WIDTH:
        bg_x = 0

#     # Draw two backgrounds
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WINDOW_WIDTH, 0))



#     #sprites
    all_sprites.update(dt)
    all_sprites.draw(screen)
        
    pygame.display.flip()
   

pygame.quit()
sys.exit()