import pygame


class HeartIcon(pygame.sprite.Sprite):
    def __init__(self):
        super(HeartIcon, self). __init__()
        self.img_heart_01 = pygame.image.load('hearticon1').convert_alpha()
        self.img_heart_02 = pygame.image.load('hearticon1').convert_alpha()
        self.img_heart_03 = pygame.image.load('hearticon1').convert_alpha()
        self.anim_list = [self.img_heart01,
                          self.img_heart02,
                          self.img_heart03]
        self.anim_index = 0
        self.max_index = len(self.anim_list) -1
        self.max_frame_duration = 3
        self.frame_duration = self.max_frame_duration
        self.image = self.anim_list[self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.x = 10
        # self.rect.y = WINDOW_HEIGHT - self.rect.height - 30

    def update(self):
        if self.frame_duration == 0:
            self.anim_index += 1
            if self.anim_index > self.max_index:
                self.anim_index = 0
            self.image = self.anim_list[self.anim_index]
            self.frame_duration = self.max_frame_duration
        self.frame_duration -= 1