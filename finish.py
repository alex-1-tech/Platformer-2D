try:
    import pygame
    import sys

    from settings import *
    from maps import *
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Finish(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        try:
            super().__init__()
            self.image = pygame.Surface((size, size))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect(topleft=pos)
        except Exception as error:
            print("Error create Death:", error)
            sys.exit(2)

    def update(self, x_shift):
        self.rect.x += x_shift
