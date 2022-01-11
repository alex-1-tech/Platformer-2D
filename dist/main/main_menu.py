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
    from take_resourse import resource_path
    from draw_logo import draw_l
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Menu:
    def __init__(self, surface, difficulty_menu, shop_menu):
        self.display_surface = surface
        self.state = True

        self.start = Button()
        self.shop = Button()

        self.difficulty_menu = difficulty_menu
        self.shop_menu = shop_menu

    def pressed(self):
        if self.start.pressed(pygame.mouse.get_pos()):
            mixer.stop()
            self.difficulty_menu.state = True
            self.state = False
        elif self.shop.pressed(pygame.mouse.get_pos()):
            self.shop_menu.state = True

    def run(self):
        if not in_music:
            mixer.music.stop()

        # create buttons
        self.start_button = self.start.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                     height // 2 - 80, 100, 40, 100,
                                                     'start', (0, 255, 255))
        self.shop_button = self.shop.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                   height // 2 - 30, 100, 40, 100,
                                                   'shop', (0, 255, 255))

        # draw buttons
        self.display_surface.blit(self.start_button, (0, 0))
        self.display_surface.blit(self.shop_button, (0, 0))

        draw_l(self.display_surface)
