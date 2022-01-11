from settings import height
import pygame


def draw_l(display_surface):
    font = pygame.font.SysFont('snapitc', 50)
    name_game = font.render('The way of the samurai', True, (255, 80, 0))
    font = pygame.font.Font(None, 100)
    name_logo = font.render('A', True, (255, 80, 0))

    display_surface.blit(name_game, (350, 100))

    # logo
    pygame.draw.rect(display_surface, '#000000', (1180, height - 100, 80, 80))
    display_surface.blit(name_logo, (1195, height - 90))
