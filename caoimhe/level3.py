import pygame
import sys
from os.path import join
from random import randint


# ============================================================
# HAY BALE
# ============================================================

class HayBail(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):

        super().__init__(groups)

        self.image = surf

        # Collision mask
        self.mask = pygame.mask.from_surface(
            self.image
        )

        # Put hay bale on the ground
        self.rect = self.image.get_rect(
            midbottom=pos
        )

        self.ground_y = 550

        
        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        # Movement speed
        self.speed = 600


    def update(self, dt):

        # Move hay bale from right to left
        self.pos.x -= self.speed * dt

        self.rect.x = round(
            self.pos.x
        )

        # Delete when off screen
        if self.rect.right < 0:

            self.kill()


# ============================================================
# ICE CUBE COLLECTABLE
# ============================================================

class IceCube(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):

        super().__init__(groups)

        self.image = surf

        # Collision mask
        self.mask = pygame.mask.from_surface(
            self.image
        )

        # Position
        self.rect = self.image.get_rect(
            center=pos
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        # Same speed as hay bales
        self.speed = 600


    def update(self, dt):

        # Move towards penguin
        self.pos.x -= self.speed * dt

        self.rect.x = round(
            self.pos.x
        )

        # Remove when off screen
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

        # Ground level
        self.ground_y = 550


        # ====================================================
        # LOAD PENGUIN
        # ====================================================

        self.image = pygame.image.load(join('caoimhe', 'Images', 'Player.png')).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (250, 250)
        )


        # ====================================================
        # POSITION
        # ====================================================

        self.rect = self.image.get_rect(
            midbottom=(
                self.start_x,
                self.ground_y
            )
        )


        # ====================================================
        # MOVEMENT
        # ====================================================

        self.direction = pygame.Vector2()

        self.speed = 300


        # ====================================================
        # JUMP
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
    # UPDATE PLAYER
    # ========================================================

    def update(self, dt):

        keys = pygame.key.get_pressed()


        # ====================================================
        # LEFT / RIGHT
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
        # KEEP PENGUIN ON SCREEN
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
# HAY BALE COLLISIONS
# ============================================================

def collisions():

    global game_over

    collision_sprites = pygame.sprite.spritecollide(
        player,
        HayBail_sprites,
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

            print("Penguin hit!")

            print(
                "Health:",
                player.health
            )


        # Game over
        if player.health <= 0:

            game_over = True


# ============================================================
# COLLECT ICE CUBES
# ============================================================

def collect_ice_cubes():

    global collectable_score

    collected = pygame.sprite.spritecollide(
        player,
        ice_cube_sprites,
        True,
        pygame.sprite.collide_mask
    )


    if collected:

        collectable_score += len(
            collected
        )

        print(
            "Ice cubes:",
            collectable_score
        )


# ============================================================
# SCORE
# ============================================================

def display_score():

    # ========================================================
    # TIME SCORE
    # ========================================================

    current_time = (
        pygame.time.get_ticks()
        // 100
    )


    score_text = font.render(
        "Score: " + str(current_time),
        True,
        (0, 0, 0)
    )


    score_rect = score_text.get_frect(
        topleft=(20, 20)
    )


    # Background
    pygame.draw.rect(
        screen,
        (240, 240, 240),
        score_rect.inflate(20, 10),
        0,
        10
    )


    # Border
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        score_rect.inflate(20, 10),
        3,
        10
    )


    screen.blit(
        score_text,
        score_rect
    )


    # ========================================================
    # ICE CUBE SCORE
    # ========================================================

    ice_text = font.render(
        "Ice Cubes: "
        + str(collectable_score),
        True,
        (0, 0, 0)
    )


    ice_rect = ice_text.get_frect(
        topleft=(20, 65)
    )


    pygame.draw.rect(
        screen,
        (240, 240, 240),
        ice_rect.inflate(20, 10),
        0,
        10
    )


    pygame.draw.rect(
        screen,
        (0, 0, 0),
        ice_rect.inflate(20, 10),
        3,
        10
    )


    screen.blit(
        ice_text,
        ice_rect
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global collectable_score
    global bg_x


    # Reset health
    player.health = 3


    # Reset player position
    player.rect.midbottom = (
        player.start_x,
        player.ground_y
    )


    # Reset jump
    player.velocity_y = 0

    player.on_ground = True


    # Reset score
    collectable_score = 0


    # Remove all hay bales
    HayBail_sprites.empty()


    # Remove all ice cubes
    ice_cube_sprites.empty()


    # Reset background
    bg_x = 0


    # Reset timer
    pygame.time.set_ticks()


# ============================================================
# GAME OVER SCREEN
# ============================================================

def game_over_screen():

    global game_over


    while game_over:

        for event in pygame.event.get():


            # =================================================
            # QUIT
            # =================================================

            if event.type == pygame.QUIT:

                pygame.quit()

                sys.exit()


            # =================================================
            # KEYBOARD
            # =================================================

            if event.type == pygame.KEYDOWN:


                # Restart
                if event.key == pygame.K_r:

                    reset_game()

                    game_over = False


                # Quit
                elif event.key == pygame.K_q:

                    pygame.quit()

                    sys.exit()


        # ====================================================
        # DRAW GAME OVER IMAGE
        # ====================================================

        screen.blit(
            game_over_image,
            (0, 0)
        )


        pygame.display.flip()

        clock.tick(60)


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
    "There's Snow Place Like Home"
)


# ============================================================
# BACKGROUND
# ============================================================

background = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "farm_background.png"
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


# ============================================================
# HAY BALE IMAGE
# ============================================================

HayBail_surf = pygame.image.load(join('caoimhe', 'Images','haybail.png')).convert_alpha()


HayBail_surf = pygame.transform.scale(
    HayBail_surf,
    (200, 200)
)


# ============================================================
# ICE CUBE IMAGE
# ============================================================

ice_cube_surf = pygame.image.load(
    join(
        'Leah',
        'ice.cube.png'
    )
).convert_alpha()


ice_cube_surf = pygame.transform.scale(
    ice_cube_surf,
    (80, 80)
)


# ============================================================
# GAME OVER IMAGE
# ============================================================

game_over_image = pygame.image.load(
    join(
        'Leah',
        'game.over.jpg'
    )
).convert_alpha()


game_over_image = pygame.transform.scale(
    game_over_image,
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
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

HayBail_sprites = pygame.sprite.Group()

ice_cube_sprites = pygame.sprite.Group()


# ============================================================
# CREATE PLAYER
# ============================================================

player = Player(
    all_sprites
)


# ============================================================
# ICE CUBE SCORE
# ============================================================

collectable_score = 0


# ============================================================
# HAY BALE EVENT
# ============================================================

HayBail_event = pygame.event.custom_type()

pygame.time.set_timer(
    HayBail_event,
    900
)


# ============================================================
# ICE CUBE EVENT
# ============================================================

ice_cube_event = pygame.event.custom_type()

pygame.time.set_timer(
    ice_cube_event,
    1500
)


# ============================================================
# GAME OVER VARIABLE
# ============================================================

game_over = False


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True


while running:


    # ========================================================
    # DELTA TIME
    # ========================================================

    dt = clock.tick(60) / 1000


    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():


        # ====================================================
        # QUIT
        # ====================================================

        if event.type == pygame.QUIT:

            running = False


        # ====================================================
        # HAY BALE SPAWN
        # ====================================================

        if event.type == HayBail_event:

            x = WINDOW_WIDTH + randint(
                200,
                1000
            )


            # Ground level
            y = WINDOW_HEIGHT


            HayBail(
                HayBail_surf,
                (
                    x,
                    y
                ),
                (
                    all_sprites,
                    HayBail_sprites
                )
            )


        # ====================================================
        # ICE CUBE SPAWN
        # ====================================================

        if event.type == ice_cube_event:

            x = WINDOW_WIDTH + randint(
                200,
                1000
            )


            # Random height
            y = randint(
                180,
                350
            )


            IceCube(
                ice_cube_surf,
                (
                    x,
                    y
                ),
                (
                    all_sprites,
                    ice_cube_sprites
                )
            )


    # ========================================================
    # GAME OVER
    # ========================================================

    if game_over:

        game_over_screen()

        continue


    # ========================================================
    # MOVE BACKGROUND
    # ========================================================

    bg_x -= (
        scroll_speed
        * dt
    )


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
    # HAY BALE COLLISIONS
    # ========================================================

    collisions()


    # ========================================================
    # ICE CUBE COLLECTION
    # ========================================================

    collect_ice_cubes()


    # ========================================================
    # DRAW SPRITES
    # ========================================================

    all_sprites.draw(
        screen
    )


    # ========================================================
    # DISPLAY SCORE
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