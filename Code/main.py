print("MAIN STARTING")
import pygame 
import sys
import os
from os.path import join
from moviepy import VideoFileClip


print("IMPORTING LEVEL 1")
import level_1

print("IMPORTING LEVEL 2")
import level_2

print("IMPORTING LEVEL 3")
import level_3

print("IMPORTING ENDLESS")
import level_endless

print("ALL IMPORTS FINISHED")

pygame.init()
print("PYGAME INITIALISED")
pygame.mixer.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
WIDTH = 1000
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Snow Place like Home")
clock = pygame.time.Clock()
start_screen_image = pygame.image.load(join("assets", "images", "mainmenu.png"))
start_screen_image = pygame.transform.scale(start_screen_image,(WINDOW_WIDTH, WINDOW_HEIGHT))

level_1_button = pygame.Rect(420, 204, 160, 40)
level_2_button = pygame.Rect(420, 246, 160, 40)
level_3_button = pygame.Rect(420, 289, 160, 40)
endless_button = pygame.Rect(420, 333, 160, 40)

intro_image1 = pygame.image.load(join("assets", "images", "startcutscene1.png"))
intro_image1 = pygame.transform.scale(intro_image1, (WINDOW_WIDTH, WINDOW_HEIGHT))
intro_image2 = pygame.image.load(join("assets", "images", "startcutscene2.png"))
intro_image2 = pygame.transform.scale(intro_image2, (WINDOW_WIDTH, WINDOW_HEIGHT))
intro_image3 = pygame.image.load(join("assets", "images", "startcutscene3.png"))
intro_image3 = pygame.transform.scale(intro_image3, (WINDOW_WIDTH, WINDOW_HEIGHT))
intro_image4 = pygame.image.load(join("assets", "images", "startcutscene4.png"))
intro_image4 = pygame.transform.scale(intro_image4, (WINDOW_WIDTH, WINDOW_HEIGHT))

transition1 = pygame.image.load(join("assets", "Images", "boat-1.png"))
transition1 = pygame.transform.scale(transition1, (WINDOW_WIDTH, WINDOW_HEIGHT))
transition2 = pygame.image.load(join("assets", "Images", "boat-2.png"))
transition2 = pygame.transform.scale(transition2,(WINDOW_WIDTH, WINDOW_HEIGHT))
transition3 = pygame.image.load(join("assets", "Images", "boat-3.png"))
transition3 = pygame.transform.scale(transition3,(WINDOW_WIDTH, WINDOW_HEIGHT))

endcredits_background = pygame.image.load(join("assets", "images", "credits.png")).convert()
endcredits_background = pygame.transform.scale(endcredits_background,(WINDOW_WIDTH, WINDOW_HEIGHT))

victoryscreen = pygame.image.load(join("assets", "images", "victory.screen.jpg"))
victoryscreen = pygame.transform.scale(victoryscreen, (WINDOW_WIDTH, WINDOW_HEIGHT))
thanksforplaying = pygame.image.load(join("assets", "images", "thanksforplaying.png"))
thanksforplaying = pygame.transform.scale(thanksforplaying, (WINDOW_WIDTH, WINDOW_HEIGHT))




intro_sound = pygame.mixer.Sound(join("assets", "sounds", "startvideo.flac"))
intro_sound.set_volume(1.0)

intro_sound1 = pygame.mixer.Sound(join("assets", "sounds", "ohnomyiceisgone.mp3"))

intro_sound2 = pygame.mixer.Sound(join("assets", "sounds", "heythatsmyice.mp3"))



transition1_sound = pygame.mixer.Sound(join("assets", "sounds", "almosttherecovermyescape.mp3"))
transition1_sound.set_volume(1.0)
transition2_sound = pygame.mixer.Sound(join("assets", "sounds", "smoothasice.mp3"))
transition2_sound.set_volume(1.0)
transition3_sound = pygame.mixer.Sound(join("assets", "sounds", "theadventure.flac"))
transition3_sound.set_volume(1.0)

thanksforplayer_sound = pygame.mixer.Sound(join("assets", "sounds", "thanksforplaying.flac"))
thanksforplayer_sound.set_volume(0.8)
mainmenu_sound = pygame.mixer.Sound(join("assets", "sounds", "mainmenu.mp3"))
mainmenu_sound.set_volume(0.8)
victory_sound = pygame.mixer.Sound(join("assets", "sounds", "victorymusic.mp3"))
victory_sound.set_volume(0.8)
endcredits_sound = pygame.mixer.Sound(join("assets", "sounds", "credits.mp3"))
endcredits_sound.set_volume(16.0)

def play_intro_video():

    print("PLAYING INTRO VIDEO")

    video = VideoFileClip(join("assets", "images", "stolen-house.mp4"))
    intro_sound.play()
    for frame in video.iter_frames(fps=32):

        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.close()
                pygame.quit()
                sys.exit()

        # Convert MoviePy frame to Pygame surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Resize video to fit your window
        frame_surface = pygame.transform.scale(
            frame_surface,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        clock.tick(30)
    intro_sound.stop()
    print("Sound playing:", pygame.mixer.get_busy())
    video.close()

    print("INTRO VIDEO FINISHED")


def level_1_intro_images():

    images = [
        intro_image1,
        intro_image2,
        intro_image3,
        intro_image4
    ]

    sounds = [
        intro_sound1,
        intro_sound2]
    
    for image, sound in zip(images, sounds):

        # Stop any previous image sound
        pygame.mixer.stop()

        # Play sound for this image
        sound.play()

        # Show image
        screen.blit(image, (0, 0))
        pygame.display.flip()

        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 2000:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    pygame.quit()
                    sys.exit()
            clock.tick(60)

        # Stop the sound before moving to the next image
        sound.stop()

    

def transition_screen():

    # ---------------- IMAGE 1 ----------------
    transition1_sound.play()
    screen.blit(transition1, (0, 0))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 3000:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


    # ---------------- IMAGE 2 ----------------
    transition2_sound.play()
    screen.blit(transition2, (0, 0))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 2000:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


    # ---------------- IMAGE 3 ----------------
    # Stay here until SPACE is pressed
    transition3_sound.play()
    while True:

        # Draw image 3
        screen.blit(transition3, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    print("SPACE PRESSED - LEAVING TRANSITION")
                    return

        clock.tick(60)


def start_screen():
    mainmenu_sound.play()
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    # ---------------- LEVEL 1 ----------------
                    if level_1_button.collidepoint(event.pos):

                        print("Level 1 clicked")
                        mainmenu_sound.stop()
                        play_intro_video()
                        level_1_intro_images()
                        result = level_1.run_level_1()

                        print("LEVEL 1 RETURNED:", repr(result))

                        if result == "level2":

                            print("LEVEL 1 FINISHED")
                            print("STARTING FIRST TRANSITION")

                            transition_screen()

                            print("FIRST TRANSITION FINISHED")
                            print("STARTING LEVEL 2")

                            result = level_2.run_level_2()

                            print("LEVEL 2 RETURNED:", repr(result))

                            if result == "level3":

                                print("LEVEL 2 FINISHED")
                                print("STARTING SECOND TRANSITION")

                                transition_screen()

                                print("SECOND TRANSITION FINISHED")
                                print("STARTING LEVEL 3")

                                result = level_3.run_level_3()

                                print("LEVEL 3 RETURNED:", repr(result))

                                if result == "finished":

                                    print("LEVEL 3 FINISHED")
                                    print("STARTING ENDING SEQUENCE")

                                    ending_screen()

                                    print("ENDING FINISHED")
                                    print("RETURNING TO MAIN MENU")


                    # ---------------- LEVEL 2 ----------------
                    elif level_2_button.collidepoint(event.pos):

                        print("Level 2 clicked")
                        mainmenu_sound.stop()
                        result = level_2.run_level_2()

                        print("LEVEL 2 RETURNED:", repr(result))

                        if result == "level3":

                            print("STARTING TRANSITION")

                            transition_screen()

                            print("STARTING LEVEL 3")

                            result = level_3.run_level_3()

                            print("LEVEL 3 RETURNED:", repr(result))


                    # ---------------- LEVEL 3 ----------------
                    elif level_3_button.collidepoint(event.pos):

                        print("Level 3 clicked")
                        mainmenu_sound.stop()

                        result = level_3.run_level_3()

                        print("LEVEL 3 RETURNED:", repr(result))

                        if result == "finished":

                            print("LEVEL 3 FINISHED")
                            print("STARTING ENDING SEQUENCE")

                            ending_screen()

                            print("ENDING FINISHED")
                            print("RETURNING TO MAIN MENU")


                    # ---------------- ENDLESS ----------------
                    elif endless_button.collidepoint(event.pos):

                        print("Endless Mode clicked")

                        result = level_endless.run_level_endless()

                        print("ENDLESS LEVEL RETURNED:", repr(result))

                        if result == "menu":

                            print("Returning to main menu")


        # ---------------- DRAW MENU ----------------

        screen.blit(start_screen_image, (0, 0))

        pygame.display.flip()

        clock.tick(60)


def end_credits():

    print("END CREDITS STARTED")

    # Stop victory music
    victory_sound.stop()
    endcredits_sound.play(-1)

    
    # Font
    credits_font = pygame.font.Font(
        join("assets", "fonts", "Oxanium-Bold.ttf"), 
        28
    )

    title_font = pygame.font.Font(
        join("assets", "fonts", "Oxanium-Bold.ttf"), 
        45
    )

    # Credits text
    credits = [
        ("SNOW PLACE LIKE HOME", title_font),
        ("", credits_font),
        ("END CREDITS", title_font),
        ("", credits_font),
        ("Scrum Master", credits_font),
        ("Caoimhe Naughton", credits_font),
        ("", credits_font),
        ("Chief Game Coder", credits_font),
        ("Leah Winters", credits_font),
        ("", credits_font),
        ("Main Story & Character Designer", credits_font),
        ("Luke Mcredmond", credits_font),
        ("", credits_font),
        ("Website Designer & Coder", credits_font),
        ("Cillian Gaffey", credits_font),
        ("", credits_font),
        ("THANK YOU FOR PLAYING!", title_font),
    ]

    # Starting position
    y = WINDOW_HEIGHT

    # Optional credits music
    # credits_sound = pygame.mixer.Sound(
    #     join("assets", "sounds", "credits.mp3")
    # )
    # credits_sound.play(-1)

    running_credits = True

    while running_credits:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    running_credits = False

        # Background
        screen.blit(endcredits_background, (0, 0))


        # Draw credits
        current_y = y

        for text, font in credits:

            text_surface = font.render(
                text,
                True,
                (10, 45, 100)
            )

            text_rect = text_surface.get_rect(
                center=(WINDOW_WIDTH // 2, current_y)
            )

            screen.blit(text_surface, text_rect)

            current_y += 55

        # Scroll credits upwards
        y -= 1

        # Stop automatically after all credits have passed
        if y + len(credits) * 55 < 0:
            running_credits = False

        pygame.display.flip()
        clock.tick(60)
     # Stop credits music
    endcredits_sound.stop()

    print("END CREDITS FINISHED")


def ending_screen():

    print("ENDING SCREEN STARTED")

    # ---------------- BOAT IMAGE 1 ----------------
    transition1_sound.play()
    screen.blit(transition1, (0, 0))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 3000:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


    # ---------------- BOAT IMAGE 2 ----------------
    transition2_sound.play()
    screen.blit(transition2, (0, 0))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 3000:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


    # ---------------- THANKS FOR PLAYING ----------------
    thanksforplayer_sound.play()
    screen.blit(thanksforplaying, (0, 0))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 4000:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


    # ---------------- VICTORY SCREEN ----------------
    # Stay here until SPACE is pressed
    pygame.mixer.stop()
    victory_sound.play(-1)
    while True:

        screen.blit(victoryscreen, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                victory_sound.stop()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    print("SPACE PRESSED")
                    victory_sound.stop()
                    end_credits()
                    print("RETURNING TO MAIN MENU")
                    return

        clock.tick(60)

print("STARTING MAIN MENU")
start_screen()

pygame.quit()
sys.exit()
