import pygame.image

try:
    import os
    from os import walk
    import sys
    from take_resourse import resource_path
    import pygame
    from pygame.constants import QUIT, K_ESCAPE, KEYDOWN
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


def import_folder(path):
    surface_list = []
    a, b = 0, 0
    for _, __, img_file in walk(path):
        for image in img_file:
            ful_path = resource_path(os.path.join(path, image))
            image_surf = pygame.image.load(ful_path).convert_alpha()
            a = max(image_surf.get_rect()[2], a)
            b = max(image_surf.get_rect()[3], b)
            surface_list.append(image_surf)
    return surface_list
