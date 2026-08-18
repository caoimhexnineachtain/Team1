import pygame
import sys
from os.path import join
from random import randint
import math


# ============================================================
# SETTINGS
# ============================================================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500


# ============================================================
# HEART
# ============================================================

class Hearticon(pygame.sprite.Sprite):

    def __init__(self, position):

        super().__init__()

        self.image = pygame.image.load(
            join("caoimhe", "Images", "hearticon1.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (50, 50)
        )

        self.rect = self.image.get_rect(
            topright=position
        )


# ============================================================
# CACTUS
# ============================================================

class Cactus(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):

        super().__init__(groups)

        self.image = surf

        self.rect = self.image.get_rect(
            midbottom=pos
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        self.speed = 600

        self.mask = pygame.mask.from_surface(
            self.image
        )

    def update(self, dt):

        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        if self.rect.right < 0:
            self.kill()


# ============================================================
# ICE CUBE
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

        self.speed = 600

        self.mask = pygame.mask.from_surface(
            self.image
        )

    def update(self, dt):

        self.pos.x -= self.speed * dt

        self.rect.x = round(self.pos.x)

        if self.rect.right < 0:
            self.kill()


# ============================================================
# PLAYER
# ============================================================

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):

        super().__init__(groups)

        self.start_x = WINDOW_WIDTH // 2

        self.ground_y = 450

        # Normal player
        self.normal_surf = pygame.image.load(
            join("caoimhe", "images", "Player.png")
        ).convert_alpha()

        self.normal_surf = pygame.transform.scale(
            self.normal_surf,
            (250, 250)
        )

        # Hit player
        self.hit_surf = pygame.image.load(
            join("caoimhe", "images", "dizzyplayer.png")
        ).convert_alpha()

        self.hit_surf = pygame.transform.scale(
            self.hit_surf,
            (250, 250)
        )

        # Dead player
        self.dead_surf = pygame.image.load(
            join("caoimhe", "Images", "deadplayer.png")
        ).convert_alpha()

        self.dead_surf = pygame.transform.scale(
            self.dead_surf,
            (250, 250)
        )

        self.image = self.normal_surf

        self.rect = self.image.get_rect(
            midbottom=(self.start_x, self.ground_y)
        )

        # Movement
        self.gravity = 1200
        self.jump_speed = -600
        self.velocity_y = 0

        self.on_ground = True

        # Bobbing
        self.animation_time = 0
        self.bob_amount = 5
        self.bob_speed = 12

        # Health
        self.health = 3

        self.damage_cooldown = 500
        self.last_hit_time = 0

        # Flashing
        self.is_flashing = False
        self.flash_time = 0
        self.flash_duration = 450

        # Death
        self.is_dead = False
        self.death_time = 0
        self.death_duration = 1000

        # Collision mask
        self.mask = pygame.mask.from_surface(
            self.image
        )

    def update(self, dt):

        if self.is_dead:

            self.image = self.dead_surf

            return

        keys = pygame.key.get_pressed()

        # ---------------- JUMP ----------------

        if keys[pygame.K_SPACE] and self.on_ground:

            self.velocity_y = self.jump_speed

            self.on_ground = False

        # ---------------- GRAVITY ----------------

        self.velocity_y += self.gravity * dt

        self.rect.y += self.velocity_y * dt

        # ---------------- GROUND ----------------

        if self.rect.bottom >= self.ground_y:

            self.rect.bottom = self.ground_y

            self.velocity_y = 0

            self.on_ground = True

        # Keep player in the middle
        self.rect.centerx = self.start_x

        # Flash timer
        self.flash_timer()

        # ---------------- BOBBING ----------------

        if self.on_ground:

            self.animation_time += dt

            bob_offset = (
                math.sin(
                    self.animation_time * self.bob_speed
                )
                * self.bob_amount
            )

            self.rect.bottom = (
                self.ground_y + bob_offset
            )

        else:

            self.animation_time = 0

    def flash(self):

        self.health -= 1

        if self.health <= 0:

            self.is_dead = True

            self.is_flashing = False

            self.death_time = pygame.time.get_ticks()

            death_position = self.rect.midbottom

            self.image = self.dead_surf

            self.rect = self.image.get_rect(
                midbottom=death_position
            )

            self.mask = pygame.mask.from_surface(
                self.image
            )

        else:

            self.is_flashing = True

            self.flash_time = pygame.time.get_ticks()

            self.image = self.hit_surf

            self.mask = pygame.mask.from_surface(
                self.image
            )

    def flash_timer(self):

        if self.is_flashing:

            if (
                pygame.time.get_ticks()
                - self.flash_time
                >= self.flash_duration
            ):

                self.is_flashing = False

                self.image = self.normal_surf

                self.mask = pygame.mask.from_surface(
                    self.image
                )


# ============================================================
# COWBOY
# ============================================================

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

        self.ground_y = 450

        self.rect = self.image.get_rect(
            midbottom=(pos[0], self.ground_y)
        )

        self.pos = pygame.math.Vector2(
            self.rect.topleft
        )

        self.mode = mode

        self.leaving_speed = -100

        self.rescue_speed = 400

        self.animation_time = 0

        self.bob_amount = 5

        self.bob_speed = 12

    def update(self, dt):

        # Cowboy leaving
        if self.mode == "leaving":

            self.pos.x += (
                self.leaving_speed * dt
            )

            self.rect.x = round(self.pos.x)

            if self.rect.right < 0:

                self.kill()

        # Cowboy coming to player
        elif self.mode == "catch":

            self.pos.x += (
                self.rescue_speed * dt
            )

            self.rect.x = round(self.pos.x)

            if (
                self.rect.centerx
                >= WINDOW_WIDTH // 2
            ):

                self.rect.centerx = (
                    WINDOW_WIDTH // 2
                )

                self.pos.x = self.rect.x

                self.rescue_speed = 0

        # Bobbing
        self.animation_time += dt

        bob_offset = (
            math.sin(
                self.animation_time
                * self.bob_speed
            )
            * self.bob_amount
        )

        self.rect.bottom = (
            self.ground_y + bob_offset
        )


# ============================================================
# LEVEL 2
# ============================================================

def level_2(screen):

    # --------------------------------------------------------
    # LOAD IMAGES
    # --------------------------------------------------------

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

    transition1 = pygame.image.load(
        join(
            "caoimhe",
            "Images",
            "boat-1.png"
        )
    ).convert()

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
    ).convert()

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
    ).convert()

    transition3 = pygame.transform.scale(
        transition3,
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    start_screen_image = pygame.image.load(
        join(
            "caoimhe",
            "images",
            "startscreen.png"
        )
    ).convert()

    start_screen_image = pygame.transform.scale(
        start_screen_image,
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

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

    # --------------------------------------------------------
    # LOAD GAME SPRITES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FONT
    # --------------------------------------------------------

    font = pygame.font.Font(
        join(
            "Leah",
            "Oxanium-Bold.ttf"
        ),
        20
    )

    # --------------------------------------------------------
    # CLOCK
    # --------------------------------------------------------

    clock = pygame.time.Clock()

    # --------------------------------------------------------
    # SPRITE GROUPS
    # --------------------------------------------------------

    all_sprites = pygame.sprite.Group()

    cactus_sprites = pygame.sprite.Group()

    heart_sprites = pygame.sprite.Group()

    ice_cube_sprites = pygame.sprite.Group()

    cowboy_sprites = pygame.sprite.Group()

    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    player = Player(all_sprites)

    # --------------------------------------------------------
    # HEARTS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # COWBOY
    # --------------------------------------------------------

    Cowboy(
        cowboy_surf,
        (250, 550),
        (all_sprites, cowboy_sprites),
        mode="leaving"
    )

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    collectable_score = 0

    bg_x = 0

    scroll_speed = 600

    game_over = False

    game_start = True

    cowboy_spawned = False

    game_start_time = pygame.time.get_ticks()

    level_running = True

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    cactus_event = pygame.event.custom_type()

    ice_cube_event = pygame.event.custom_type()

    pygame.time.set_timer(
        cactus_event,
        1400
    )

    pygame.time.set_timer(
        ice_cube_event,
        2200
    )

    # ========================================================
    # MAIN LEVEL 1 LOOP
    # ========================================================

    while level_running:

        # ----------------------------------------------------
        # START SCREEN
        # ----------------------------------------------------

        if game_start:

            screen.blit(
                start_screen_image,
                (0, 0)
            )

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.time.set_timer(
                        cactus_event,
                        0
                    )

                    pygame.time.set_timer(
                        ice_cube_event,
                        0
                    )

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

            clock.tick(60)

            continue

        # ----------------------------------------------------
        # GAME OVER SCREEN
        # ----------------------------------------------------

        if game_over:

            screen.blit(
                game_over_image,
                (0, 0)
            )

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.time.set_timer(
                        cactus_event,
                        0
                    )

                    pygame.time.set_timer(
                        ice_cube_event,
                        0
                    )

                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    # Restart Level 1
                    if event.key == pygame.K_r:

                        player.health = 3

                        player.is_dead = False

                        player.is_flashing = False

                        player.image = (
                            player.normal_surf
                        )

                        player.rect = (
                            player.image.get_rect(
                                midbottom=(
                                    player.start_x,
                                    player.ground_y
                                )
                            )
                        )

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

                        for sprite in list(
                            cactus_sprites
                        ):

                            sprite.kill()

                        for sprite in list(
                            ice_cube_sprites
                        ):

                            sprite.kill()

                        for sprite in list(
                            cowboy_sprites
                        ):

                            sprite.kill()

                        Cowboy(
                            cowboy_surf,
                            (250, 550),
                            (
                                all_sprites,
                                cowboy_sprites
                            ),
                            mode="leaving"
                        )

                        collectable_score = 0

                        bg_x = 0

                        cowboy_spawned = False

                        game_start_time = (
                            pygame.time.get_ticks()
                        )

                        game_over = False

                    # Quit
                    elif event.key == pygame.K_q:

                        pygame.quit()
                        sys.exit()

            clock.tick(60)

            continue

        # ----------------------------------------------------
        # DELTA TIME
        # ----------------------------------------------------

        dt = clock.tick(60) / 1000

        # ----------------------------------------------------
        # EVENTS
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.time.set_timer(
                    cactus_event,
                    0
                )

                pygame.time.set_timer(
                    ice_cube_event,
                    0
                )

                pygame.quit()
                sys.exit()

            # Cactus
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

            # Ice cube
            elif (
                event.type == ice_cube_event
                and not player.is_dead
            ):

                x = (
                    WINDOW_WIDTH
                    + randint(200, 600)
                )

                y = randint(180, 350)

                IceCube(
                    ice_cube_surf,
                    (x, y),
                    (
                        all_sprites,
                        ice_cube_sprites
                    )
                )

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        if not player.is_dead:

            # Background movement
            bg_x -= (
                scroll_speed * dt
            )

            if bg_x <= -WINDOW_WIDTH:

                bg_x += WINDOW_WIDTH

            # Update sprites
            all_sprites.update(dt)

            # ------------------------------------------------
            # CACTUS COLLISION
            # ------------------------------------------------

            collision_sprites = (
                pygame.sprite.spritecollide(
                    player,
                    cactus_sprites,
                    False,
                    pygame.sprite.collide_mask
                )
            )

            if collision_sprites:

                current_time = (
                    pygame.time.get_ticks()
                )

                if (
                    current_time
                    - player.last_hit_time
                    >= player.damage_cooldown
                ):

                    player.flash()

                    player.last_hit_time = (
                        current_time
                    )

                    if player.health == 2:

                        heart3.kill()

                    elif player.health == 1:

                        heart2.kill()

                    elif player.health <= 0:

                        heart1.kill()

            # ------------------------------------------------
            # ICE CUBE COLLECTION
            # ------------------------------------------------

            collected = (
                pygame.sprite.spritecollide(
                    player,
                    ice_cube_sprites,
                    True,
                    pygame.sprite.collide_mask
                )
            )

            if collected:

                collectable_score += len(
                    collected
                )

        else:

            # Cowboy keeps moving
            cowboy_sprites.update(dt)

        # ----------------------------------------------------
        # DRAW BACKGROUND
        # ----------------------------------------------------

        screen.blit(
            background,
            (bg_x, 0)
        )

        screen.blit(
            background,
            (bg_x + WINDOW_WIDTH, 0)
        )

        # ----------------------------------------------------
        # DRAW SPRITES
        # ----------------------------------------------------

        all_sprites.draw(screen)

        heart_sprites.draw(screen)

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        current_time = (
            pygame.time.get_ticks()
            - game_start_time
        ) // 100

        time_text = font.render(
            str(current_time),
            True,
            (0, 0, 0)
        )

        time_rect = time_text.get_rect(
            topleft=(20, 20)
        )

        pygame.draw.rect(
            screen,
            (240, 240, 240),
            time_rect.inflate(20, 10),
            4,
            10
        )

        screen.blit(
            time_text,
            time_rect
        )

        # Ice cube score
        ice_text = font.render(
            "Ice Cubes: "
            + str(collectable_score),
            True,
            (0, 0, 0)
        )

        ice_rect = ice_text.get_rect(
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

        # ----------------------------------------------------
        # PLAYER DIES
        # ----------------------------------------------------

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

            # Wait before game over
            if (
                pygame.time.get_ticks()
                - player.death_time
                >= player.death_duration
            ):

                game_over = True

        # ----------------------------------------------------
        # LEVEL COMPLETE
        # ----------------------------------------------------

        if (
            collectable_score >= 5
            and not player.is_dead
        ):

            # Stop spawning
            pygame.time.set_timer(
                cactus_event,
                0
            )

            pygame.time.set_timer(
                ice_cube_event,
                0
            )

            # Transition pictures
            pictures = [
                transition1,
                transition2,
                transition3
            ]

            durations = [
                2000,
                2000,
                5000
            ]

            for picture, duration in zip(
                pictures,
                durations
            ):

                start_time = (
                    pygame.time.get_ticks()
                )

                while (
                    pygame.time.get_ticks()
                    - start_time
                    < duration
                ):

                    for event in pygame.event.get():

                        if (
                            event.type
                            == pygame.QUIT
                        ):

                            pygame.quit()
                            sys.exit()

                    screen.blit(
                        picture,
                        (0, 0)
                    )

                    pygame.display.flip()

                    clock.tick(60)

            return

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        pygame.display.flip()

        
    

    return