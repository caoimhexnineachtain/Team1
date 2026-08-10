import pygame
import sys
from os.path import join
from random import randint


# ============================================================
# MUSHROOM
# ============================================================

class Mushroom(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):

        super().__init__(groups)

        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 4000
        self.speed = 600

    def update(self, dt):

        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        # Remove mushroom when it leaves the screen
        if self.rect.right < 0:
            self.kill()


# ============================================================
# PLAYER
# ============================================================

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):

        super().__init__(groups)

        # Starting X position
        self.start_x = WINDOW_WIDTH // 2


        # Ground position
        self.ground_y = WINDOW_HEIGHT

        # Load player image
        self.image = pygame.image.load(
            join(
                'Leah',
                'Player.png'
            )
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (250, 250)
        )

        # Put penguin on the ground
        self.rect = self.image.get_rect(
            midbottom=(
                self.start_x,
                self.ground_y
            )
        )

        # ====================================================
        # MOVEMENT
        # ====================================================


        self.ground_y = 550
        self.image = pygame.image.load(join("caoimhe", "Images", 'Player.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect(midtop=(self.start_x, self.ground_y))
        
        
        # Same positioning method as the cactus
        # self.rect = self.image.get_rect(midbottom=(self.start_x, self.ground_y))
        self.direction = pygame.Vector2()

        self.speed = 300

        # ====================================================
        # GRAVITY
        # ====================================================

        self.gravity = 1200

        self.jump_speed = -600

        self.velocity_y = 0

        self.on_ground = True

        # ====================================================
        # MASK
        # ====================================================

        self.mask = pygame.mask.from_surface(
            self.image
        )

        # ====================================================
        # FLASH
        # ====================================================

        self.normal_surf = self.image.copy()

        self.flash_surf = self.mask.to_surface(
            unsetcolor=(0, 0, 0, 0),
            setcolor=(255, 255, 255, 255)
        )

        self.is_flashing = False

        self.flash_time = 0

        self.flash_duration = 150

        # ====================================================
        # HEALTH
        # ====================================================

        self.health = 3

        self.damage_cooldown = 500

        self.last_hit_time = 0


    # ========================================================
    # PLAYER UPDATE
    # ========================================================

    def update(self, dt):

        keys = pygame.key.get_pressed()


        # ====================================================
        # LEFT / RIGHT MOVEMENT
        # ====================================================

        self.direction.x = (
            int(keys[pygame.K_RIGHT])
            - int(keys[pygame.K_LEFT])
        )

        self.rect.x += (
            self.direction.x
            * self.speed
            * dt
        )


        # ====================================================
        # JUMP
        # ====================================================

        if (
            keys[pygame.K_SPACE]
            and self.on_ground
        ):

            self.velocity_y = self.jump_speed

            self.on_ground = False


        # ====================================================
        # GRAVITY
        # ====================================================

        self.velocity_y += (
            self.gravity * dt
        )

        self.rect.y += (
            self.velocity_y * dt
        )


        # ====================================================
        # LAND ON GROUND
        # ====================================================

        if self.rect.bottom >= self.ground_y:

            self.rect.bottom = self.ground_y

            self.velocity_y = 0

            self.on_ground = True


        # ====================================================
        # KEEP PLAYER ON SCREEN
        # ====================================================

        if self.rect.left < 0:

            self.rect.left = 0

        if self.rect.right > WINDOW_WIDTH:

            self.rect.right = WINDOW_WIDTH


        # ====================================================
        # FLASH TIMER
        # ====================================================

        self.flash_timer()


    # ========================================================
    # PLAYER HIT
    # ========================================================

    def flash(self):

        self.health -= 1

        self.is_flashing = True

        self.flash_time = pygame.time.get_ticks()


    # ========================================================
    # FLASH TIMER
    # ========================================================

    def flash_timer(self):

        if self.is_flashing:

            if (
                pygame.time.get_ticks()
                - self.flash_time
                >= self.flash_duration
            ):

                self.is_flashing = False


# ============================================================
# COLLISIONS
# ============================================================

def collisions():

    global running

    collision_sprites = pygame.sprite.spritecollide(
        player,
        mushroom_sprites,
        False,
        pygame.sprite.collide_mask
    )

    if collision_sprites:

        current_time = pygame.time.get_ticks()

        # Damage cooldown
        if (
            current_time
            - player.last_hit_time
            >= player.damage_cooldown
        ):

            player.flash()

            player.last_hit_time = current_time

            print(
                "Penguin hit!"
            )

            print(
                "Health:",
                player.health
            )

        # Game over
        if player.health <= 0:

            running = False


# ============================================================
# SCORE
# ============================================================

def display_score():

    current_time = (
        pygame.time.get_ticks()
        // 100
    )

    text_surf = font.render(
        str(current_time),
        True,
        (0, 0, 0)
    )

    text_rect = text_surf.get_frect(
        topleft=(20, 20)
    )

    # Score background
    pygame.draw.rect(
        screen,
        (240, 240, 240),
        text_rect.inflate(20, 10),
        0,
        10
    )

    # Score border
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        text_rect.inflate(20, 10),
        4,
        10
    )

    # Score text
    screen.blit(
        text_surf,
        text_rect
    )


# ============================================================
# INITIALISE PYGAME
# ============================================================

pygame.init()


# ============================================================
# SCREEN SETTINGS
# ============================================================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

screen = pygame.display.set_mode(
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)

pygame.display.set_caption(
    "Desert Runner"
)


# ============================================================
# BACKGROUND
# ============================================================

background = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "jungle_background.png"
    )
).convert()

background = pygame.transform.scale(
    background,
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)


# ============================================================
# BACKGROUND SCROLLING
# ============================================================

bg_x = 0

scroll_speed = 100


# ============================================================
# CLOCK
# ============================================================

clock = pygame.time.Clock()

# #import
cactus_surf = pygame.image.load(join("caoimhe", "Images", 'Cactus.png')).convert_alpha()
cactus_surf = pygame.transform.scale(cactus_surf, (250, 250))
font = pygame.font.Font(join('Leah', 'Oxanium-Bold.ttf'), 20)
text_surf = font.render('text', True, (240,240,240))

# ============================================================
# MUSHROOM IMAGE
# ============================================================

mushroom_surf = pygame.image.load(
    join(
        'Leah',
        'newmushroom.png'
    )
).convert_alpha()

mushroom_surf = pygame.transform.scale(
    mushroom_surf,
    (250, 250)
)


# ============================================================
# FONT
# ============================================================

font = pygame.font.Font(
    join(
        'Leah',
        'Oxanium-Bold.ttf'
    ),
    20
)


# ============================================================
# SPRITE GROUPS
# ============================================================

all_sprites = pygame.sprite.Group()

mushroom_sprites = pygame.sprite.Group()


# ============================================================
# CREATE PLAYER
# ============================================================

player = Player(
    all_sprites
)


# ============================================================
# MUSHROOM EVENT
# ============================================================

mushroom_event = pygame.event.custom_type()

pygame.time.set_timer(
    mushroom_event,
    900
)


# ============================================================
# GAME LOOP
# ============================================================

running = True

while running:

    # Delta time
    dt = clock.tick(60) / 1000


    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # Quit
        if event.type == pygame.QUIT:

            running = False


        # Mushroom spawn
        if event.type == mushroom_event:

            x = WINDOW_WIDTH + randint(
                200,
                1000
            )

            # Mushroom sits on bottom of screen
            y = WINDOW_HEIGHT

            Mushroom(
                mushroom_surf,
                (
                    x,
                    y
                ),
                (
                    all_sprites,
                    mushroom_sprites
                )
            )


    # ========================================================
    # MOVE BACKGROUND
    # ========================================================

    bg_x -= scroll_speed * dt


    # Reset background
    if bg_x <= -WINDOW_WIDTH:

        bg_x = 0


    # ========================================================
    # DRAW BACKGROUND
    # ========================================================

    screen.blit(
        background,
        (
            bg_x,
            0
        )
    )

    screen.blit(
        background,
        (
            bg_x + WINDOW_WIDTH,
            0
        )
    )


    # ========================================================
    # UPDATE SPRITES
    # ========================================================

    all_sprites.update(dt)


    # ========================================================
    # COLLISIONS
    # ========================================================

    collisions()


    # ========================================================
    # DRAW SPRITES
    # ========================================================

    all_sprites.draw(
        screen
    )


    # ========================================================
    # SCORE
    # ========================================================

    display_score()


    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()


# ============================================================
# QUIT
# ============================================================

pygame.quit()

sys.exit()       