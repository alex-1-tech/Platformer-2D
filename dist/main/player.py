try:
    import pygame
    import sys
    import os

    from pygame import mixer
    from support import import_folder
    from settings import *
    from take_resourse import resource_path
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            mixer.init()
            path = resource_path(os.path.join('music', 'jump.mp3'))
            self.music_jump = mixer.Sound(path)
            info = open("character.txt").read().split('\n')
            if info[0].split('=')[1] == 'True':
                self.character = "first_character"
            else:
                self.character = "second_character"
            self.import_character_assest()
            self.frame_index = 0
            self.animation_speed = 0.15
            self.image = self.animations['idle'][self.frame_index]
            self.rect = self.image.get_rect(topleft=pos)

            # player movement - движение игрока
            self.direction = pygame.math.Vector2(0, 0)
            self.speed = 8
            self.gravity = 0.8
            self.jump_speed = -16

            # player states
            self.double_jump = 0
            self.status = 'idle'
            self.facing_right = True
            self.on_ground = False
            self.on_ceiling = False
            self.on_left = False
            self.on_right = False
            self.is_stay = True
        except Exception as err:
            print("Could't create character. %s" % err)
            sys.exit(2)

    def import_character_assest(self):
        character_path = "sprites/player/" + self.character + '/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, state):
        try:
            animation = self.animations[state]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

            self.image = animation[int(self.frame_index)]

            image = animation[int(self.frame_index)]
            if self.facing_right:
                self.image = image
            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image
        except Exception as err:
            print("Could't load animation %s. %s" % err, state)
            sys.exit(2)

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if self.direction.x != 0:
            self.is_stay = False
        else:
            self.is_stay = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.facing_right = True
            if self.direction.x < 1:
                self.direction.x += 0.2

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.facing_right = False
            if self.direction.x > -1:
                self.direction.x -= 0.2
        else:
            self.direction.x = 0

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (self.on_ground or self.double_jump <= 2):
            self.music_jump.play()
            self.double_jump += 1
            self.jump()
        if keys[pygame.K_f]:
            self.direction.x = 5

    def get_status(self):
        if self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):

        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate(self.status)
