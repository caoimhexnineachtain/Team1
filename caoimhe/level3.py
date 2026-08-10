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

        # Put mushroom on the ground
        self.rect = self.image.get_rect(
            midbottom=pos
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        self.speed = 600

    def update(self, dt):

        # Move mushroom to the left
        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        # Remove when off screen
        if self.rect.right < 0:
            self.kill()


# ============================================================
# ICE CUBE COLLECTABLE
# ============================================================

class IceCube(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        super().__init__(groups)

        self.image = surf

        self.rect = self.image.get_rect(
            center=pos
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        # Same movement speed as the mushrooms
        self.speed = 600

    def update(self, dt):

        # Move ice cube towards the penguin
        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        # Remove when it leaves the screen
        if self.rect.right < 0:
            self.kill()


# ============================================================
# PLAYER
# ============================================================

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)

        # Starting position
        self.start_x = WINDOW_WIDTH // 2

        # Ground level
        self.ground_y = WINDOW_HEIGHT

        # Load penguin
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
        # GROUND
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

        # Flash timer
        self.flash_timer()

    def flash(self):

        self.health -= 1

        self.is_flashing = True

        self.flash_time = pygame.time.get_ticks()

    def flash_timer(self):

        if self.is_flashing:

            if (
                pygame.time.get_ticks()
                - self.flash_time
                >= self.flash_duration
            ):
                self.is_flashing = False


# ============================================================
# COLLISIONS WITH MUSHROOMS
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

        if (
            current_time
            - player.last_hit_time
            >= player.damage_cooldown
        ):

            player.flash()

            player.last_hit_time = current_time

            print("Penguin hit!")
            print("Health:", player.health)

        # Game Over
        if player.health <= 0:

            running = False


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

        collectable_score += len(collected)

        print(
            "Ice cubes:",
            collectable_score
        )


# ============================================================
# SCORE
# ============================================================

def display_score():

    # Time score
    current_time = pygame.time.get_ticks() // 100

    score_text = font.render(
        "Score: " + str(current_time),
        True,
        (0, 0, 0)
    )

    score_rect = score_text.get_frect(
        topleft=(20, 20)
    )

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        score_rect.inflate(20, 10),
        0,
        10
    )

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


    # Ice cube score
    ice_text = font.render(
        "Ice Cubes: " + str(collectable_score),
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
# GAME OVER SCREEN
# ============================================================

def game_over_screen():

    global running

    game_over = True

    while game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Restart
                if event.key == pygame.K_r:

                    game_over = False

                    restart_game()

                # Quit
                if event.key == pygame.K_q:

                    pygame.quit()
                    sys.exit()


        # Draw Game Over image
        screen.blit(
            game_over_image,
            (0, 0)
        )

        pygame.display.flip()

        clock.tick(60)


# ============================================================
# RESTART GAME
# ============================================================

def restart_game():

    global collectable_score

    # Reset health
    player.health = 3

    # Reset position
    player.rect.midbottom = (
        player.start_x,
        player.ground_y
    )

    # Reset jump
    player.velocity_y = 0

    player.on_ground = True

    # Reset score
    collectable_score = 0

    # Remove all mushrooms
    mushroom_sprites.empty()

    # Remove all ice cubes
    ice_cube_sprites.empty()

    # Reset background
    global bg_x
    bg_x = 0


# ============================================================
# INITIALISE PYGAME
# ============================================================

pygame.init()


# ============================================================
# SCREEN
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
# MUSHROOM IMAGE
# ============================================================

mushroom_surf = pygame.image.load(
    join(
        'Leah',
        'mushroom.png'
    )
).convert_alpha()

mushroom_surf = pygame.transform.scale(
    mushroom_surf,
    (250, 250)
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

mushroom_sprites = pygame.sprite.Group()

ice_cube_sprites = pygame.sprite.Group()


# ============================================================
# PLAYER
# ============================================================

player = Player(
    all_sprites
)


# ============================================================
# SCORE
# ============================================================

collectable_score = 0


# ============================================================
# MUSHROOM EVENT
# ============================================================

mushroom_event = pygame.event.custom_type()

pygame.time.set_timer(
    mushroom_event,
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
# MAIN GAME
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


        # ====================================================
        # SPAWN MUSHROOM
        # ====================================================

        if event.type == mushroom_event:

            x = WINDOW_WIDTH + randint(
                200,
                1000
            )

            # Mushroom on ground
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


        # ====================================================
        # SPAWN ICE CUBE
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
    # COLLECT ICE CUBES
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
# GAME OVER
# ============================================================

game_over_screen()


# ============================================================
# QUIT
# ============================================================

pygame.quit()

sys.exit()