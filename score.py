try:
    import pygame
    import sys
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


def score(number, screen):
    font = pygame.font.Font(None, 55)
    text = font.render('  ' + str(number), True, (255, 0, 255))
    image = pygame.image.load('sprites/object/glossy.png').convert_alpha()
    screen.blit(image, (20, 25))
    screen.blit(text, (25, 25))
