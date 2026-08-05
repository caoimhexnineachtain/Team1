import pygame 
from os.path import join
from random import randint, uniform

class Catus(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        # self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        # self.speed = randint(400,500)
      
   
    # def update(self, dt):
    #     self.rect.center += self.direction * self.speed * dt
    #     if pygame.time.get_ticks() - self.start_time >= self.lifetime:
    #         self.kill()
    #     self.rotation += self.rotation_speed * dt
    #     self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
    #     self.rect = self.image.get_rect(center = self.rect.center)


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Penguine Runner')
running = True
clock = pygame.time.Clock()


TOP_COLOR = (135, 206, 235)    
BOTTOM_COLOR = (144, 238, 144)  
TOP_HEIGHT = (WINDOW_HEIGHT * 3) // 4

catus_surf = pygame.image.load(join('Leah', 'Happy Catus.png')).convert_alpha()

all_sprites = pygame.sprite.Group()
catus_sprites = pygame.sprite.Group()

catus_event = pygame.event.custom_type()
# pygame.time.set_timer(catus_event, 500)


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == catus_event:
            x, y = randint(200, WINDOW_WIDTH), randint(200, 400)
            Catus(catus_surf, (x, y), (all_sprites, catus_sprites))


    pygame.draw.rect(display_surface, TOP_COLOR, (0, 0, WINDOW_WIDTH, TOP_HEIGHT))
    pygame.draw.rect(display_surface, BOTTOM_COLOR, (0, TOP_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - TOP_HEIGHT))
   
    all_sprites.update(dt)

    all_sprites.draw(display_surface)
    
    pygame.display.flip()
   

pygame.quit()