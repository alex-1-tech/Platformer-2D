try:
    import pygame
    import sys
    import random
    import os

    from settings import *
    from maps import maps
    from tiles import Tile
    from player import Player
    from coin import Coin
    from score import score
    from pygame import mixer
    from death import Death
    from button import Button
    from level import Level
    from draw_logo import draw_l
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Restart:
    def __init__(self, surface, main_menu, difficulty_menu):
        self.display_surface = surface
        self.restart = Button()
        self.menu = Button()
        self.state = False
        self.main_menu = main_menu
        self.difficulty_menu = difficulty_menu
        font = pygame.font.SysFont('snapitc', 50)
        self.name_game = font.render('The way of the samurai', True, (255, 80, 0))
        font = pygame.font.Font(None, 100)
        self.name_logo = font.render('A', True, (255, 80, 0))

    def pressed(self):
        if self.restart.pressed(pygame.mouse.get_pos()):
            self.state = False
            self.difficulty_menu.state = True
        if self.menu.pressed(pygame.mouse.get_pos()):
            self.state = False
            self.main_menu.state = True

    def run(self, win=False):

        self.display_surface.blit(self.name_game, (350, 100))
        self.menu_button = self.menu.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                   height // 2 - 20, 100, 40, 100,
                                                   'Menu', (0, 255, 255))
        self.display_surface.blit(self.menu_button, (0, 0))
        if not win:
            self.restart_button = self.restart.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                             height // 2 - 100, 100, 40, 100,
                                                             'Restart', (0, 255, 255))
        else:
            font = pygame.font.Font(None, 70)
            text = font.render('You win!', True, (255, 0, 0))
            self.restart_button = self.restart.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                             height // 2 - 100, 100, 40, 100,
                                                             'Again', (0, 255, 255))
            self.display_surface.blit(text, (width // 2 - 75,
                                             height // 2 - 170))
        draw_l(self.display_surface)
