import pygame
import sys
from os.path import join
from random import randint


class Cactus(pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups):
         super().__init__(groups)
         self.original_surf = surf
         self.image = surf
         self.rect = self.image.get_rect(midbottom=pos)
         self.pos = pygame.math.Vector2(self.rect.topleft)
         self.start_time = pygame.time.get_ticks()
         self.lifetime = 4000
         self.speed = 600  

        # Adjust to match the game's scrolling speed
        def update(self, dt):
            self.pos.x -= self.speed * dt
            self.rect.x = round(self.pos.x)
            if self.rect.right < -250:
                self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.start_x = WINDOW_WIDTH // 2
        self.ground_y = 550
        self.normal_surf = pygame.image.load(join('caoimhe', 'images', 'Player.png')).convert_alpha()
        self.image = self.normal_surf
        self.normal_surf = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect(midtop=(self.start_x, self.ground_y))
        
        
        # Same positioning method as the cactus
        # self.rect = self.image.get_rect(midbottom=(self.start_x, self.ground_y))
        self.direction = pygame.Vector2()
        self.speed = 300

        self.hit_surf = pygame.image.load(join('caoimhe', 'images', 'dizzyplayer.png')).convert_alpha()
        self.hit_surf = pygame.transform.scale(self.hit_surf, (250, 250)) 

        self.image = self.normal_surf

        self.rect = self.image.get_rect(midbottom=(self.start_x, self.ground_y))

        # Mask
        self.mask = pygame.mask.from_surface(self.image)
        self.is_flashing = False
        self.flash_time = 0
        self.flash_duration = 450
        self.health = 3
        self.damage_cooldown = 500
        self.last_hit_time = 0
        self.gravity = 1200
        self.jump_speed = -600
        self.velocity_y = 0
        self.on_ground = True
        self.start_x = WINDOW_WIDTH // 2
        
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Gravity
        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt

        # Land back on ground
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.on_ground = True

        # Keep player in the same x position
        self.rect.centerx = self.start_x
        self.flash_timer()

    def flash(self):
        self.health -= 1
        self.is_flashing = True
        self.flash_time = pygame.time.get_ticks()
        self.image = self.hit_surf
 
    def flash_timer(self):
        if self.is_flashing:
            if pygame.time.get_ticks() - self.flash_time >= self.flash_duration:
                self.is_flashing = False  
                self.image = self.normal_surf

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, cactus_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        current_time = pygame.time.get_ticks()
        if current_time - player.last_hit_time >= player.damage_cooldown:

            player.flash()
            player.last_hit_time = current_time

            # Remove one heart
            if player.health == 2:
                heart3.kill()

            elif player.health == 1:
                heart2.kill()

            elif player.health <= 0:
                heart1.kill()
                running = False


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (0, 0, 0))

    # Top left position
    text_rect = text_surf.get_frect(topleft=(20, 20))

    screen.blit(text_surf, text_rect)

    pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 10), 4, 10)


class Hearticon(pygame.sprite.Sprite): 
    def __init__(self, position): 
        super().__init__() 
        self.image = pygame.image.load(join("caoimhe", "Images", 'hearticon1.png')).convert_alpha() 
        # Make the hearts a suitable size 
        self.image = pygame.transform.scale(self.image, (50, 50) ) 
        # Position 
        self.rect = self.image.get_rect(topright=position )

# Initialise Pygame
pygame.init()



# Screen settings
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
cactus_surf = pygame.image.load(join("caoimhe", "Images", 'Cactus.png')).convert_alpha()
cactus_surf = pygame.transform.scale(cactus_surf, (250, 250))
font = pygame.font.Font(join('Leah', 'Oxanium-Bold.ttf'), 20)
text_surf = font.render('text', True, (240,240,240))


# #sprites
all_sprites = pygame.sprite.Group()
cactus_sprites = pygame.sprite.Group()
# heart_sprites = pygame.sprite.Group()
# player = Player(all_sprites)
# heart = Hearticon()
# heart_sprites.add(heart)
heart_sprites = pygame.sprite.Group()
player = Player(all_sprites)
heart1 = Hearticon((WINDOW_WIDTH - 10, 10))
heart2 = Hearticon((WINDOW_WIDTH - 70, 10))
heart3 = Hearticon((WINDOW_WIDTH - 130, 10))
heart_sprites.add(heart1, heart2, heart3)


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
         y = 500
         Cactus(cactus_surf, (x, y), (all_sprites, cactus_sprites))
    
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
    heart_sprites.draw(screen)
    collisions()
    display_score()
      
    pygame.display.flip()
   

pygame.quit()
sys.exit()