try:
    import pygame
    import sys

    from support import import_folder
    from settings import *
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('sprites/object/glossy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
