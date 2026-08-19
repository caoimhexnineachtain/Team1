import pygame
import sys
from os.path import join
from random import randint

def run_level_3():
    print("LEVEL 1 FUNCTION STARTED")
    class Hearticon(pygame.sprite.Sprite):
        def __init__(self, position):
            super().__init__()

            self.image = pygame.image.load(join("assets", "Images", "hearticon1.png")).convert_alpha()

            # Make the hearts a suitable size
            self.image = pygame.transform.scale(self.image,(50, 50))
            # Position
            self.rect = self.image.get_rect(topright=position)


    class Crow (pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups):
            super().__init__(groups)

            self.original_surf = surf
            self.image = surf

            self.rect = self.image.get_rect(midbottom=pos)
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.speed = 600

            # Adjust to match the game's scrolling speed

        def update(self, dt):
            self.pos.x -= self.speed * dt
            self.rect.x = round(self.pos.x)
            if self.rect.right < 0:
                self.kill()

    class Haybale (pygame.sprite.Sprite):
            def __init__(self, surf, pos, groups):
                super().__init__(groups)
    
                self.original_surf = surf
                self.image = surf
    
                self.rect = self.image.get_rect(midbottom=pos)
                self.pos = pygame.math.Vector2(self.rect.topleft)
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
            self.mask = pygame.mask.from_surface(self.image)

            # Position
            self.rect = self.image.get_rect(center=pos)

            self.pos = pygame.math.Vector2(self.rect.topleft)

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
            self.ground_y = 540
            self.duck_stomach_y = 110

            # -----------------------------
            # DUCKING
            # -----------------------------
            self.is_ducking = False

            self.normal_height = 250
            self.duck_height = 150

            # -----------------------------
            # PLAYER IMAGES
            # -----------------------------
            self.normal_surf = pygame.image.load(
                join("assets", "images", "Player.png")
            ).convert_alpha()

            self.normal_surf = pygame.transform.scale(
                self.normal_surf,
                (250, 250)
            )

            self.hit_surf = pygame.image.load(
                join("assets", "images", "dizzyplayer.png")
            ).convert_alpha()

            self.hit_surf = pygame.transform.scale(
                self.hit_surf,
                (250, 250)
            )

            self.dead_surf = pygame.image.load(
                join("assets", "Images", "deadplayer.png")
            ).convert_alpha()

            self.dead_surf = pygame.transform.scale(
                self.dead_surf,
                (250, 250)
            )

            self.duck_surf = pygame.image.load(
                join("assets", "images", "duckplayer.png")
            ).convert_alpha()
            # Remove transparent space around the duck
            bbox = self.duck_surf.get_bounding_rect()
            self.duck_surf = self.duck_surf.subsurface(bbox).copy()

            self.duck_surf = pygame.transform.scale(
                self.duck_surf,
                (70, 35)
            )

            # -----------------------------
            # INITIAL IMAGE / POSITION
            # -----------------------------
            self.image = self.normal_surf

            self.rect = self.image.get_rect(
                midbottom=(self.start_x, self.ground_y)
            )

            # -----------------------------
            # MOVEMENT
            # -----------------------------
            self.velocity_y = 0
            self.gravity = 1200
            self.jump_speed = -600

            self.on_ground = True

            self.jumps = 0
            self.max_jumps = 2

            # -----------------------------
            # ANIMATION
            # -----------------------------
            self.animation_time = 0
            self.bob_amount = 5
            self.bob_speed = 12

            # -----------------------------
            # HEALTH / DAMAGE
            # -----------------------------
            self.health = 3
            self.damage_cooldown = 500
            self.last_hit_time = 0

            self.is_flashing = False
            self.flash_time = 0

            # Increase this to make dizzy last longer
            self.flash_duration = 500

            # -----------------------------
            # DEATH
            # -----------------------------
            self.is_dead = False
            self.death_time = 0
            self.death_duration = 1000

            # -----------------------------
            # COLLISION MASK
            # -----------------------------
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, dt):
            if self.is_dead:
                self.image = self.dead_surf
                return

                        # -----------------------------
            # DUCKING
            # -----------------------------
            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN] and self.on_ground:

                if not self.is_ducking:

                    self.is_ducking = True
                    self.image = self.duck_surf

                    # Put duck's stomach/center where normal feet are
                    self.rect = self.image.get_rect(topleft=(
            self.start_x - self.image.get_width() // 2,
            self.ground_y - self.duck_stomach_y))

                    self.mask = pygame.mask.from_surface(self.image)

            else:

                if self.is_ducking:

                    self.is_ducking = False
                    self.image = self.normal_surf

                    # Put normal player's feet on ground
                    self.rect = self.image.get_rect(
                        midbottom=(self.start_x, self.ground_y)
                    )

                    self.mask = pygame.mask.from_surface(self.image)


            # -----------------------------
            # MOVEMENT / GRAVITY
            # -----------------------------
            if not self.is_ducking:

                self.velocity_y += self.gravity * dt
                self.rect.y += self.velocity_y * dt


            # -----------------------------
            # GROUND POSITION
            # -----------------------------
            if self.is_ducking:

                # Keep stomach at Y = 540
                self.rect.top = self.ground_y - self.duck_stomach_y

                self.velocity_y = 0
                self.on_ground = True
                self.jumps = 0

            else:

                if self.rect.bottom >= self.ground_y:
                    self.rect.bottom = self.ground_y
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumps = 0
                else:
                    self.on_ground = False


            # Keep X position
            self.rect.centerx = self.start_x
            self.flash_timer()

            # -----------------------------
            # BOB ANIMATION
            # -----------------------------
            if self.on_ground and not self.is_ducking and not self.is_flashing:

                self.animation_time += dt

                import math

                bob_offset = (
                    math.sin(self.animation_time * self.bob_speed)
                    * self.bob_amount
                )

                self.rect.bottom = self.ground_y + bob_offset

            else:
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
                self.rect = self.image.get_rect(midbottom=death_position)

                # Keep the player in the same position
                bottom_position = self.rect.midbottom
                self.rect = self.image.get_rect(midbottom=bottom_position)

            else:
                # Player has been hit but still has lives
                self.is_flashing = True
                self.flash_time = pygame.time.get_ticks()
                self.image = self.hit_surf

        def flash_timer(self):

            if self.is_flashing:
                if (pygame.time.get_ticks() - self.flash_time >= self.flash_duration):
                    self.is_flashing = False
                    self.image = self.normal_surf
                    self.mask = pygame.mask.from_surface(self.image)

    class Cowboy(pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups, mode="leaving"):
            super().__init__(groups)
            self.image = surf

            self.ground_y = 570
            self.rect = self.image.get_rect(midbottom=(pos[0], self.ground_y))

            self.pos = pygame.math.Vector2(self.rect.topleft)

            # Cowboy's current behaviour
            self.mode = mode

            # Movement speeds
            self.leaving_speed = -100
            self.catch_speed = 400
            self.has_arrived = False

            # Bobbing
            self.animation_time = 0
            self.bob_amount = 5
            self.bob_speed = 12

        def update(self, dt):

            if self.mode == "leaving":

                # Slowly move left
                self.pos.x += self.leaving_speed * dt
                self.rect.x = round(self.pos.x)

                # Remove when off left side
                if self.rect.right < 0:
                    self.kill()

            elif self.mode == "catch":

                # Move right
                self.pos.x += self.catch_speed * dt

                self.rect.x = round(self.pos.x)

                # Stop in middle of screen
                if self.rect.centerx >= WINDOW_WIDTH // 2:
                    self.rect.centerx = WINDOW_WIDTH // 2
                    self.pos.x = self.rect.x
                    self.catch_speed = 0

                    if not self.has_arrived:
                        self.has_arrived = True
                    

            self.animation_time += dt
            import math
            bob_offset = (
                math.sin(self.animation_time * self.bob_speed) * self.bob_amount)

            self.rect.bottom = (self.ground_y + bob_offset)

    def collisions():
        global game_over

        if player.is_dead:
            return

        # Check mushroom collisions
        haybale_collision = pygame.sprite.spritecollide(
            player,
            haybale_sprites,
            False,
            pygame.sprite.collide_mask
        )

        # Check bird collisions
        crow_collision = pygame.sprite.spritecollide(
            player,
            crow_sprites,
            False,
            pygame.sprite.collide_mask
        )

        # If either one hits the player
        if haybale_collision or crow_collision:

            current_time = pygame.time.get_ticks()

            if current_time - player.last_hit_time >= player.damage_cooldown:

                impact_sound.play()
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
        nonlocal collectable_score

        collected = pygame.sprite.spritecollide(player, ice_cube_sprites, True, pygame.sprite.collide_mask)

        if collected:
            collectable_score += len(collected)
            for ice_cube in collected:
                coin_sound.play()


    def display_score(): 
        
        current_time = (pygame.time.get_ticks() - game_start_time) // 100

        text_surf = font.render(str(current_time), True, (0, 0, 0))

        # Top left position
        text_rect = text_surf.get_frect(topleft=(20, 20))

        screen.blit(text_surf, text_rect)

        pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 10), 4, 10)

        ice_text = font.render("Ice Cubes: " + str(collectable_score), True, (0, 0, 0))
        ice_rect = ice_text.get_frect(topleft=(20, 65))

        pygame.draw.rect(screen, (240, 240, 240), ice_rect.inflate(20, 10), 0, 10)

        pygame.draw.rect(screen, (0, 0, 0), ice_rect.inflate(20, 10), 3, 10)
        screen.blit(ice_text, ice_rect)

    def reset_game():
        nonlocal collectable_score
        nonlocal bg_x
        nonlocal heart1, heart2, heart3
        nonlocal game_start_time
        nonlocal cowboy_spawned
        nonlocal cowboy_spoke 
        nonlocal catch_cowboy
        

        # Reset health
        player.health = 3
        player.is_dead = False
        player.death_time = 0
        player.is_ducking = False
        player.image = player.normal_surf

        # Reset collision mask
        player.mask = pygame.mask.from_surface(player.image)
        heart_sprites.empty()

        heart1 = Hearticon((WINDOW_WIDTH - 10, 10))

        heart2 = Hearticon((WINDOW_WIDTH - 70, 10))

        heart3 = Hearticon((WINDOW_WIDTH - 130, 10))

        heart_sprites.add(heart1, heart2, heart3)

        # Reset player position
        # player.rect.midbottom = (player.start_x, player.ground_y)
        # Reset player position
        player.rect = player.image.get_rect(midbottom=(player.start_x, player.ground_y))

        # Reset jump
        player.velocity_y = 0
        player.on_ground = True

        # Reset score
        collectable_score = 0

        game_start_time = pygame.time.get_ticks()

        # Remove all obstacles completely
        for sprite in list(haybale_sprites):
            sprite.kill()

        for sprite in list(ice_cube_sprites):
            sprite.kill()

        for sprite in list(crow_sprites):
                    sprite.kill()

        # Reset background
        bg_x = 0

        cowboy_spawned = False
        cowboy_spoke =False
        catch_cowboy = None

        for sprite in list(cowboy_sprites):
            sprite.kill()

    def game_over_screen():
        nonlocal game_over

        pygame.mixer.music.stop()

    # Start game over music
        game_over_music.play(-1)

        while game_over:
            for event in pygame.event.get():

                # Quit window
                if event.type == pygame.QUIT:
                    game_over_music.stop()

                    pygame.quit()
                    sys.exit()

                # Keyboard controls
                if event.type == pygame.KEYDOWN:

                    # Restart
                    if event.key == pygame.K_r:
                        game_over_music.stop()
                        reset_game()
                        game_over = False

                        pygame.mixer.music.load(join("assets", "sounds", "farm.mp3"))
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play(-1)

                    elif event.key == pygame.K_q:
                        game_over_music.stop()

                        pygame.quit()
                        sys.exit()

            # Draw game over image
            screen.blit(game_over_image, (0, 0))
            pygame.display.flip()
            clock.tick(60)


    # def level_cutscene():
    #     pictures = [transition1, transition2] 
    #     durations = [2000, 2000, 5000]

    #     for picture, duration in zip(pictures, durations):
    #         start_time = pygame.time.get_ticks()

    #         while (pygame.time.get_ticks() - start_time < duration):

    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.quit()
    #                     sys.exit()

    #             # Show picture
    #             screen.blit(picture, (0, 0))

    #             pygame.display.flip()
    #             clock.tick(60)




    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 500
    WIDTH = 1000
    HEIGHT = 500

    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Snow Place like Home")

    background = pygame.image.load(join("assets", "Images", "farm_background.png")).convert()
    background = pygame.transform.scale(background,(WINDOW_WIDTH, WINDOW_HEIGHT))


    transition1 = pygame.image.load(join("assets", "Images", "boat-1.png"))
    transition1 = pygame.transform.scale(transition1, (WINDOW_WIDTH, WINDOW_HEIGHT))
    transition2 = pygame.image.load(join("assets", "Images", "boat-2.png"))
    transition2 = pygame.transform.scale(transition2,(WINDOW_WIDTH, WINDOW_HEIGHT))
    # transition3 = pygame.image.load(join("assets", "Images", "boat-3.png"))
    # transition3 = pygame.transform.scale(transition3,(WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.mixer.music
    pygame.mixer.music.load(join("assets", "sounds", "farm.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    coin_sound = pygame.mixer.Sound(join("assets", "sounds", "coin.mp3"))
    coin_sound.set_volume(0.5)
    jump_sound = pygame.mixer.Sound(join("assets", "sounds", "jump.mp3"))
    jump_sound.set_volume(0.3)
    cowboydead_sound = pygame.mixer.Sound(join("assets", "sounds", "ohlookhesafterdying.flac"))
    cowboydead_sound.set_volume(0.5)
    game_over_music = pygame.mixer.Sound(join("assets", "sounds", "lossmusic.mp3"))
    game_over_music.set_volume(0.5)
    impact_sound = pygame.mixer.Sound(join("assets", "sounds", "impact.mp3"))
    impact_sound.set_volume(0.7)

    bg_x = 0
    scroll_speed = 600

    # Increase for faster scrolling

    clock = pygame.time.Clock()


    haybale_surf = pygame.image.load(join("assets", "Images", "haybale.png")).convert_alpha()
    haybale_surf = pygame.transform.scale(haybale_surf, (350, 350))
    crow_surf = pygame.image.load(join("assets", "Images", "crow.png")).convert_alpha()
    crow_surf = pygame.transform.scale(crow_surf, (220, 220))
    

    font = pygame.font.Font(join("assets", "fonts", "Oxanium-Bold.ttf"), 20)
    text_surf = font.render("text", True, (240, 240, 240))

    game_over_image = pygame.image.load(join("assets", 'images', "game.over.jpg")).convert_alpha()
    game_over_image = pygame.transform.scale(game_over_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


    ice_cube_surf = pygame.image.load(join("assets", 'images',"ice.cube.png")).convert_alpha()
    ice_cube_surf = pygame.transform.scale(ice_cube_surf,(80, 80))

    cowboy_surf = pygame.image.load(join("assets","Images","cowboy.png")).convert_alpha()
    cowboy_surf = pygame.transform.scale(cowboy_surf,(350, 350))


    #sprites
    all_sprites = pygame.sprite.Group()
    haybale_sprites = pygame.sprite.Group()
    crow_sprites = pygame.sprite.Group()
    heart_sprites = pygame.sprite.Group()
    player = Player(all_sprites)

    heart1 = Hearticon((WINDOW_WIDTH - 10, 10))
    heart2 = Hearticon((WINDOW_WIDTH - 70, 10))
    heart3 = Hearticon((WINDOW_WIDTH - 130, 10))
    heart_sprites.add(heart1, heart2, heart3)

    ice_cube_sprites = pygame.sprite.Group()

    cowboy_sprites = pygame.sprite.Group()
    Cowboy(cowboy_surf, (250, 550),(all_sprites, cowboy_sprites), mode="leaving")


    collectable_score = 0
    game_start_time = pygame.time.get_ticks()

    haybale_event = pygame.event.custom_type()
    pygame.time.set_timer(haybale_event, 1500)

    crow_event = pygame.event.custom_type()
    pygame.time.set_timer(crow_event, 1400)

    ice_cube_event = pygame.event.custom_type()
    pygame.time.set_timer(ice_cube_event, 2200)

    last_haybale_x = WINDOW_WIDTH + 300

    game_over = False
    game_start = True
    running = True
    cowboy_spawned = False
    cowboy_spoke = False
    catch_cowboy = None
    


    while running:
    
        # ---------------- GAME OVER ----------------
        if game_over:
            game_over_screen()
            continue
        # ---------------- DELTA TIME ----------------

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ---------------- JUMP ----------------
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if not player.is_dead and player.jumps < player.max_jumps:

                        player.velocity_y = player.jump_speed
                        player.jumps += 1
                        player.on_ground = False

                        jump_sound.play()
            # ---------------- HAYBALE ----------------
            elif event.type == haybale_event and not player.is_dead:

                # Spawn haybale
                x = WINDOW_WIDTH + randint(200, 400)
                y = 560

                Haybale(
                    haybale_surf,
                    (x, y),
                    (all_sprites, haybale_sprites)
                )

                # Spawn crow BETWEEN this haybale and the next one
                crow_x = x + 700
                crow_y = 470

                Crow(
                    crow_surf,
                    (crow_x, crow_y),
                    (all_sprites, crow_sprites)
    )
            # ---------------- ICE CUBE ----------------
            elif event.type == ice_cube_event and not player.is_dead:

                x = WINDOW_WIDTH + randint(200, 600)
                y = randint(180, 350)

                IceCube(
                    ice_cube_surf,
                    (x, y),
                    (all_sprites, ice_cube_sprites)
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

        if collectable_score >= 5 and not player.is_dead:
            pygame.mixer.music.stop()
            print("LEVEL 3 COMPLETE")
            return "finished"


        # ---------------- DEATH ----------------

        if player.is_dead:

            # Spawn cowboy once
            if not cowboy_spawned:

                catch_cowboy = Cowboy(
                    cowboy_surf,
                    (-100, 600),
                    (
                        all_sprites,
                        cowboy_sprites
                    ),
                    mode="catch"
                )

                cowboy_spawned = True

            # Play cowboy sound when he reaches the penguin
            if catch_cowboy is not None:
                if catch_cowboy.has_arrived and not cowboy_spoke:
                    cowboydead_sound.play()
                    cowboy_spoke = True

            # Wait before showing game over
            if (
                pygame.time.get_ticks()
                - player.death_time
                >= player.death_duration
            ):
                game_over = True

        pygame.display.flip()



if __name__ == "__main__":
    run_level_3()
   
