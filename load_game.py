import os
import time

from pygame.rect import Rect

try:
    import pygame
    import sys

    from settings import screen_size, height
    from take_resourse import resource_path
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', 'start', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_game(screen):
    FPS = 60
    clock = pygame.time.Clock()
    a = 0
    size_of_gas_cloud = 30
    fon = pygame.transform.scale(load_image('logo.png'), (452, 700))
    font = pygame.font.Font(None, 100)
    name_logo = font.render('A', True, (255, 80, 0))
    font = pygame.font.SysFont('snapitc', 50)
    name_game = font.render('The way of the samurai', True, (255, 80, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        if a <= 760:
            a += 2
        else:
            break
        screen.fill((30, 30, 30))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, '#000000', (450, 300, 780, 30))
        pygame.draw.rect(screen, '#FF0000', (460, 305, a, 20))
        screen.blit(name_game, (500, 200))

        # logo
        pygame.draw.rect(screen, '#000000', (1180, height - 100, 80, 80))
        screen.blit(name_logo, (1195, height - 90))

        pygame.display.flip()
        clock.tick(FPS)
