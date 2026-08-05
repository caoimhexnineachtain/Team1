import pygame 
from os.path import join
from random import randint

class Catus(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))


pygame.init()
pygame.display.set_caption('Penguine Runner')
running = True
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
TOP_COLOR = (135, 206, 235)    
BOTTOM_COLOR = (144, 238, 144)  
TOP_HEIGHT = (WINDOW_HEIGHT * 3) // 4

catus_surf = pygame.image.load(join('Leah', 'Happy Catus.png')).convert_alpha()
# running = True

all_sprites = pygame.sprite.Group()
catus_sprites = pygame.sprite.Group()
# for i in range(3):
    # Catus(all_sprites, catus_surf)


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            all_sprites.update(dt)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, TOP_COLOR, (0, 0, WINDOW_WIDTH, TOP_HEIGHT))
    pygame.draw.rect(screen, BOTTOM_COLOR, (0, TOP_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - TOP_HEIGHT))
    pygame.display.flip()
   
    pygame.display.update()

pygame.quit()