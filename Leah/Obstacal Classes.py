import pygame 

class Cloud(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)