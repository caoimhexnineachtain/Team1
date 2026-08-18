import pygame
import sys
from os.path import join
from random import randint


class Hearticon(pygame.sprite.Sprite):

    def __init__(self, position):

        super().__init__()

        self.image = pygame.image.load(
            join("caoimhe", "Images", "hearticon1.png")
        ).convert_alpha()

        # Make the hearts a suitable size
        self.image = pygame.transform.scale(
            self.image,
            (50, 50)
        )

        # Position
        self.rect = self.image.get_rect(
            topright=position
        )


class Cactus(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):

        super().__init__(groups)

        self.original_surf = surf
        self.image = surf

        self.rect = self.image.get_rect(
            midbottom=pos
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        self.speed = 600

        # Adjust to match the game's scrolling speed

    def update(self, dt):

        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        if self.rect.right < 0:
            self.kill()


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

        self.rect.x = round(self.pos.x)

        # Remove when off screen
        if self.rect.right < 0:
            self.kill()


class Player(pygame.sprite.Sprite):

    def __init__(self, groups):

        super().__init__(groups)

        self.start_x = WINDOW_WIDTH // 2
        self.ground_y = 550

        self.normal_surf = pygame.image.load(
            join(
                "caoimhe",
                "images",
                "Player.png"
            )
        ).convert_alpha()

        self.image = self.normal_surf

        self.normal_surf = pygame.transform.scale(
            self.image,
            (250, 250)
        )

        self.rect = self.image.get_rect(
            midtop=(
                self.start_x,
                self.ground_y
            )
        )

        # Same positioning method as the cactus
        self.direction = pygame.Vector2()
        self.speed = 300

        self.hit_surf = pygame.image.load(
            join(
                "caoimhe",
                "images",
                "dizzyplayer.png"
            )
        ).convert_alpha()

        self.hit_surf = pygame.transform.scale(
            self.hit_surf,
            (250, 250)
        )

        self.dead_surf = pygame.image.load(
            join(
                "caoimhe",
                "Images",
                "deadplayer.png"
            )
        )

        self.dead_surf = pygame.transform.scale(
            self.dead_surf,
            (250, 250)
        )

        self.image = self.normal_surf

        self.rect = self.image.get_rect(
            midbottom=(
                self.start_x,
                self.ground_y
            )
        )

        self.animation_time = 0
        self.bob_amount = 5
        self.bob_speed = 12

        # Mask
        self.mask = pygame.mask.from_surface(
            self.image
        )

        self.is_flashing = False
        self.flash_time = 0
        self.flash_duration = 450

        self.health = 3
        self.damage_cooldown = 500

        self.is_dead = False
        self.death_time = 0
        self.death_duration = 1000  # 1 second

        self.last_hit_time = 0

        self.gravity = 1200
        self.jump_speed = -600
        self.velocity_y = 0
        self.on_ground = True

        self.start_x = WINDOW_WIDTH // 2

    def update(self, dt):

        if self.is_dead:

            self.image = self.dead_surf

            return

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

        # Only animate when on the ground
        if self.on_ground:

            self.animation_time += dt

            # Small up/down movement bob
            bob = (
                pygame.math.Vector2(
                    0,
                    pygame.math.Vector2(
                        0,
                        self.bob_amount
                    ).y
                )
            )

            # Use sine wave for smooth bobbing
            import math

            bob_offset = (
                math.sin(
                    self.animation_time * self.bob_speed
                ) * self.bob_amount
            )

            # Keep the bottom of the penguin
            # on the ground while bobbing
            self.rect.bottom = (
                self.ground_y + bob_offset
            )

        else:

            # When jumping, don't bob
            self.animation_time = 0

    def flash(self):

        self.health -= 1

        if self.health <= 0:

            # Player has died
            self.is_dead = True
            self.is_flashing = False

            self.death_time = pygame.time.get_ticks()

            # Remember exactly where the player died
            death_position = self.rect.midbottom

            # Change to dead image
            self.image = self.dead_surf

            # Put dead image in exactly the same place
            self.rect = self.image.get_rect(
                midbottom=death_position
            )

            # Keep the player in the same position
            bottom_position = self.rect.midbottom

            self.rect = self.image.get_rect(
                midbottom=bottom_position
            )

        else:

            # Player has been hit but still has lives
            self.is_flashing = True

            self.flash_time = pygame.time.get_ticks()

            self.image = self.hit_surf

    def flash_timer(self):

        if self.is_flashing:

            if (
                pygame.time.get_ticks()
                - self.flash_time
                >= self.flash_duration
            ):

                self.is_flashing = False

                self.image = self.normal_surf


class Cowboy(pygame.sprite.Sprite):

    def __init__(
        self,
        surf,
        pos,
        groups,
        mode="leaving"
    ):

        super().__init__(groups)

        self.image = surf

        self.ground_y = 590

        self.rect = self.image.get_rect(
            midbottom=(
                pos[0],
                self.ground_y
            )
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        # Cowboy's current behaviour
        self.mode = mode

        # Movement speeds
        self.leaving_speed = -100
        self.rescue_speed = 400

        # Bobbing
        self.animation_time = 0
        self.bob_amount = 5
        self.bob_speed = 12

    def update(self, dt):

        # --------------------------------
        # COWBOY LEAVING AT START
        # --------------------------------

        if self.mode == "leaving":

            # Slowly move left
            self.pos.x += self.leaving_speed * dt

            self.rect.x = round(self.pos.x)

            # Remove when off left side
            if self.rect.right < 0:
                self.kill()

        # --------------------------------
        # COWBOY COMING TO PLAYER AFTER DEATH
        # --------------------------------

        elif self.mode == "catch":

            # Move right
            self.pos.x += self.rescue_speed * dt

            self.rect.x = round(self.pos.x)

            # Stop in middle of screen
            if self.rect.centerx >= WINDOW_WIDTH // 2:

                self.rect.centerx = WINDOW_WIDTH // 2

                self.pos.x = self.rect.x

                self.rescue_speed = 0

        # --------------------------------
        # BOBBING
        # --------------------------------

        self.animation_time += dt

        import math

        bob_offset = (
            math.sin(
                self.animation_time * self.bob_speed
            ) * self.bob_amount
        )

        self.rect.bottom = (
            self.ground_y + bob_offset
        )


def collisions():

    global game_over

    if player.is_dead:
        return

    collision_sprites = pygame.sprite.spritecollide(
        player,
        cactus_sprites,
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

            # Remove one heart
            if player.health == 2:

                heart3.kill()

            elif player.health == 1:

                heart2.kill()

            elif player.health <= 0:

                heart1.kill()


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


def display_score():

    current_time = (
        pygame.time.get_ticks()
        - game_start_time
    ) // 100

    text_surf = font.render(
        str(current_time),
        True,
        (0, 0, 0)
    )

    # Top left position
    text_rect = text_surf.get_frect(
        topleft=(20, 20)
    )

    screen.blit(
        text_surf,
        text_rect
    )

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        text_rect.inflate(20, 10),
        4,
        10
    )

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


def reset_game():

    global collectable_score
    global bg_x
    global heart1, heart2, heart3
    global game_start_time
    global cowboy_spawned

    # Reset health
    player.health = 3

    player.is_dead = False

    player.death_time = 0

    player.image = player.normal_surf

    heart_sprites.empty()

    heart1 = Hearticon(
        (WINDOW_WIDTH - 10, 10)
    )

    heart2 = Hearticon(
        (WINDOW_WIDTH - 70, 10)
    )

    heart3 = Hearticon(
        (WINDOW_WIDTH - 130, 10)
    )

    heart_sprites.add(
        heart1,
        heart2,
        heart3
    )

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

    game_start_time = pygame.time.get_ticks()

    # Remove all obstacles completely
    for sprite in list(cactus_sprites):

        sprite.kill()

    for sprite in list(ice_cube_sprites):

        sprite.kill()

    # Reset background
    bg_x = 0

    cowboy_spawned = False

    for sprite in list(cowboy_sprites):

        sprite.kill()


def game_over_screen():

    global game_over
    global game_start
    global game_start_time

    while game_over:

        for event in pygame.event.get():

            # Quit window
            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # Keyboard controls
            if event.type == pygame.KEYDOWN:

                # Restart
                if event.key == pygame.K_r:

                    reset_game()

                    game_over = False

                # Quit
                elif event.key == pygame.K_q:

                    pygame.quit()
                    sys.exit()

        # Draw game over image
        screen.blit(
            game_over_image,
            (0, 0)
        )

        pygame.display.flip()

        clock.tick(60)


def level_cutscene():

    pictures = [
        transition1,
        transition2,
        transition3
    ]

    # How long each picture stays on screen
    # (milliseconds)
    durations = [
        2000,
        2000,
        5000
    ]

    for picture, duration in zip(
        pictures,
        durations
    ):

        start_time = pygame.time.get_ticks()

        while (
            pygame.time.get_ticks()
            - start_time
            < duration
        ):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            # Show picture
            screen.blit(
                picture,
                (0, 0)
            )

            pygame.display.flip()

            clock.tick(60)

    # End the game after the third picture
    pygame.quit()
    sys.exit()


def start_screen():

    global game_start
    global game_start_time

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                game_start = False

                game_start_time = (
                    pygame.time.get_ticks()
                )

            elif event.key == pygame.K_q:

                pygame.quit()
                sys.exit()

    screen.blit(
        start_screen_image,
        (0, 0)
    )

    pygame.display.flip()


# ============================================================
# INITIALISE PYGAME
# ============================================================

pygame.init()


# ============================================================
# SCREEN SETTINGS
# ============================================================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

WIDTH = 1000
HEIGHT = 500

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Snow Place like Home"
)


# ============================================================
# LOAD BACKGROUND
# ============================================================

background = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "desert_background.png.png"
    )
).convert()

background = pygame.transform.scale(
    background,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


# ============================================================
# TRANSITION IMAGES
# ============================================================

transition1 = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "boat-1.png"
    )
)

transition1 = pygame.transform.scale(
    transition1,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


transition2 = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "boat-2.png"
    )
)

transition2 = pygame.transform.scale(
    transition2,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


transition3 = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "boat-3.png"
    )
)

transition3 = pygame.transform.scale(
    transition3,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


# ============================================================
# START SCREEN
# ============================================================

start_screen_image = pygame.image.load(
    join(
        "caoimhe",
        "images",
        "startscreen.png"
    )
)

start_screen_image = pygame.transform.scale(
    start_screen_image,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


# ============================================================
# BACKGROUND SCROLLING
# ============================================================

bg_x = 0

scroll_speed = 600

# Increase for faster scrolling

clock = pygame.time.Clock()


# ============================================================
# CACTUS
# ============================================================

cactus_surf = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "Cactus.png"
    )
).convert_alpha()

cactus_surf = pygame.transform.scale(
    cactus_surf,
    (250, 250)
)


# ============================================================
# FONT
# ============================================================

font = pygame.font.Font(
    join(
        "Leah",
        "Oxanium-Bold.ttf"
    ),
    20
)

text_surf = font.render(
    "text",
    True,
    (240, 240, 240)
)


# ============================================================
# GAME OVER
# ============================================================

game_over_image = pygame.image.load(
    join(
        "Leah",
        "game.over.jpg"
    )
).convert_alpha()

game_over_image = pygame.transform.scale(
    game_over_image,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)


# ============================================================
# ICE CUBE
# ============================================================

ice_cube_surf = pygame.image.load(
    join(
        "Leah",
        "ice.cube.png"
    )
).convert_alpha()

ice_cube_surf = pygame.transform.scale(
    ice_cube_surf,
    (80, 80)
)


# ============================================================
# COWBOY
# ============================================================

cowboy_surf = pygame.image.load(
    join(
        "caoimhe",
        "Images",
        "cowboy.png"
    )
).convert_alpha()

cowboy_surf = pygame.transform.scale(
    cowboy_surf,
    (350, 350)
)


# ============================================================
# SPRITES
# ============================================================

all_sprites = pygame.sprite.Group()

cactus_sprites = pygame.sprite.Group()

heart_sprites = pygame.sprite.Group()

player = Player(
    all_sprites
)


# ============================================================
# HEARTS
# ============================================================

heart1 = Hearticon(
    (WINDOW_WIDTH - 10, 10)
)

heart2 = Hearticon(
    (WINDOW_WIDTH - 70, 10)
)

heart3 = Hearticon(
    (WINDOW_WIDTH - 130, 10)
)

heart_sprites.add(
    heart1,
    heart2,
    heart3
)


# ============================================================
# ICE CUBES / COWBOY
# ============================================================

ice_cube_sprites = pygame.sprite.Group()

cowboy_sprites = pygame.sprite.Group()


Cowboy(
    cowboy_surf,
    (250, 550),
    (
        all_sprites,
        cowboy_sprites
    ),
    mode="leaving"
)


# ============================================================
# GAME VARIABLES
# ============================================================

collectable_score = 0

cactus_event = pygame.event.custom_type()

pygame.time.set_timer(
    cactus_event,
    1400
)

ice_cube_event = pygame.event.custom_type()

pygame.time.set_timer(
    ice_cube_event,
    2200
)

game_over = False

game_start = True

running = True

cowboy_spawned = False


# ============================================================
# MAIN GAME LOOP
# ============================================================

while running:

    # ---------------- START SCREEN ----------------

    if game_start:

        start_screen()

        clock.tick(60)

        continue


    # ---------------- GAME OVER ----------------

    if game_over:

        game_over_screen()

        continue


    # ---------------- DELTA TIME ----------------

    dt = clock.tick(60) / 1000


    # ---------------- EVENTS ----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif (
            event.type == cactus_event
            and not player.is_dead
        ):

            x = (
                WINDOW_WIDTH
                + randint(200, 400)
            )

            y = 500

            Cactus(
                cactus_surf,
                (x, y),
                (
                    all_sprites,
                    cactus_sprites
                )
            )

        elif (
            event.type == ice_cube_event
            and not player.is_dead
        ):

            x = (
                WINDOW_WIDTH
                + randint(200, 600)
            )

            y = randint(
                180,
                350
            )

            IceCube(
                ice_cube_surf,
                (x, y),
                (
                    all_sprites,
                    ice_cube_sprites
                )
            )


    # ---------------- UPDATE GAME ----------------

    if not player.is_dead:

        # Background movement
        bg_x -= scroll_speed * dt

        if bg_x <= -WINDOW_WIDTH:

            bg_x += WINDOW_WIDTH

        # Update sprites
        all_sprites.update(dt)

        # Collisions
        collisions()

        # Collect ice cubes
        collect_ice_cubes()

    else:

        # Keep cowboy moving after player dies
        cowboy_sprites.update(dt)


    # ---------------- DRAW ----------------

    screen.blit(
        background,
        (bg_x, 0)
    )

    screen.blit(
        background,
        (
            bg_x + WINDOW_WIDTH,
            0
        )
    )

    all_sprites.draw(
        screen
    )

    heart_sprites.draw(
        screen
    )

    display_score()


    # ---------------- LEVEL COMPLETE ----------------

    if (
        collectable_score >= 1
        and not player.is_dead
    ):

        level_cutscene()


    # ---------------- DEATH ----------------

    if player.is_dead:

        # Spawn cowboy once
        if not cowboy_spawned:

            Cowboy(
                cowboy_surf,
                (-100, 600),
                (
                    all_sprites,
                    cowboy_sprites
                ),
                mode="catch"
            )

            cowboy_spawned = True

        # Wait before showing game over
        if (
            pygame.time.get_ticks()
            - player.death_time
            >= player.death_duration
        ):

            game_over = True


    pygame.display.flip()


pygame.quit()
sys.exit()
