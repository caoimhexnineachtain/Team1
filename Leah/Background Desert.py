import pygame
from os.path import join

# general setup
pygame.init()
pygame.display.set_caption('Penguine Runner')
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 700
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# sprite class
class Desert(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
# load image
desert_image = pygame.image.load(join('Leah', 'Desert Image.png')).convert_alpha()
desert_surf = pygame.transform.scale(desert_image, (1280, 700))

# sprite class
class Desert(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


# sprites
all_sprites = pygame.sprite.Group()

desert = Desert(desert_image, (0, 0))
all_sprites.add(desert)


while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            all_sprites.update()

    display_surface.fill((0, 0, 0))
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()