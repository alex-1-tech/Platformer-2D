try:
    import pygame
    import sys
    import random
    import os

    from settings import *
    from maps import maps
    from score import score
    from button import Button
    from draw_logo import draw_l
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Shop:
    def __init__(self, surface):
        self.display_surface = surface
        self.state = False

        self.first_person = Button()
        self.second_person = Button()
        self.back = Button()

        font = pygame.font.SysFont('snapitc', 50)
        self.name_game = font.render('The way of the samurai', True, (255, 80, 0))
        font = pygame.font.Font(None, 100)
        self.name_logo = font.render('A', True, (255, 80, 0))
        self.first_person_image = pygame.image.load("sprites/player/preview/first_preview_character.png")
        self.second_person_image = pygame.image.load("sprites/player/preview/second_preview_character.png")
        self.info_character = open("character.txt").read().split('\n')

    def pressed(self):
        if self.first_person.pressed(pygame.mouse.get_pos()):
            if self.info_character[0].split('=')[1] == "False":
                self.info_character[0] = self.info_character[0].split('=')[0] + "=" + "True"
                self.info_character[2] = self.info_character[2].split('=')[0] + "=" + "False"
                self.update_info(self.info_character)
        elif self.second_person.pressed(pygame.mouse.get_pos()):
            if self.info_character[2].split('=')[1] == "False" and self.info_character[3].split('=')[1] != '0':
                if int(self.info_character[3].split('=')[1]) <= int(open('score.txt').read()):
                    current_score = int(open('score.txt').read()) - int(self.info_character[3].split('=')[1])
                    f = open('score.txt', 'w')
                    f.write(str(current_score))
                    self.info_character[3] = self.info_character[3].split('=')[0] + "=0"
                    self.info_character[0] = self.info_character[0].split('=')[0] + "=" + "True"
                    self.info_character[2] = self.info_character[2].split('=')[0] + "=" + "False"
                    self.update_info(self.info_character)
            elif self.info_character[2].split('=')[1] == "False":
                self.info_character[2] = self.info_character[2].split('=')[0] + "=" + "True"
                self.info_character[0] = self.info_character[0].split('=')[0] + "=" + "False"
                self.update_info(self.info_character)
        elif self.back.pressed(pygame.mouse.get_pos()):
            self.state = False

    def update_info(self, info):
        f = open("character.txt", 'w')
        for i in info:
            f.write(i + '\n')
        f.close()
        self.info_character = open("character.txt").read().split('\n')

    def run(self):
        score(open("score.txt").read(), self.display_surface)
        if self.info_character[0].split('=')[1] == "True":
            first = "used"
            if self.info_character[3].split('=')[1] == '0':
                second = "use"
            else:
                second = self.info_character[3].split('=')[1]
        else:
            second = "used"
            if self.info_character[1].split('=')[1] == '0':
                first = "use"
            else:
                first = self.info_character[1].split('=')[1]

        # create buttons
        self.first_button = self.first_person.create_button(self.display_surface, (0, 0, 0), 440,
                                                            220 + self.first_person_image.get_rect()[3], 100, 40, 100,
                                                            first, (0, 255, 255))
        self.second_button = self.second_person.create_button(self.display_surface, (0, 0, 0), 780,
                                                              220 + self.first_person_image.get_rect()[3], 100, 40, 100,
                                                              second, (0, 255, 255))
        self.back_button = self.back.create_button(self.display_surface, (0, 0, 0), 600,
                                                   300 + self.first_person_image.get_rect()[3], 100, 40, 100,
                                                   "Back", (0, 255, 255))

        draw_l(self.display_surface)
        # characters
        self.display_surface.blit(self.first_person_image, (400, 200))
        self.display_surface.blit(self.second_person_image, (760, 200))
