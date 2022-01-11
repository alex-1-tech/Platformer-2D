try:
    import pygame
    import sys
    import random
    import os

    from draw_logo import draw_l
    from settings import *
    from score import score
    from pygame import mixer
    from button import Button
    from level import Level
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Difficulty_menu:
    # create difficulty menu - change difficulty
    def __init__(self, surface):
        self.display_surface = surface
        self.easy = Button()
        self.normal = Button()
        self.hard = Button()
        self.state = False

    def pressed(self):
        col = 0
        if self.easy.pressed(pygame.mouse.get_pos()):
            col = 10
        elif self.normal.pressed(pygame.mouse.get_pos()):
            col = 20
        elif self.hard.pressed(pygame.mouse.get_pos()):
            col = 30
        if col != 0:
            mixer.stop()
            self.state = False
            level = Level(self.display_surface, col)
            return level
        return None

    def run(self):
        # create buttons
        self.first_button = self.easy.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                    height // 2 - 100, 100, 40, 100,
                                                    'Easy', (0, 255, 255))
        self.second_button = self.normal.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                       height // 2 - 50, 100, 40, 100,
                                                       'Normal', (0, 255, 255))
        self.third_button = self.hard.create_button(self.display_surface, (0, 0, 0), width // 2 - 25,
                                                    height // 2, 100, 40, 100,
                                                    'Hard', (0, 255, 255))

        # draw buttons
        self.display_surface.blit(self.first_button, (0, 0))
        self.display_surface.blit(self.second_button, (0, 0))
        self.display_surface.blit(self.third_button, (0, 0))

        draw_l(self.display_surface)
