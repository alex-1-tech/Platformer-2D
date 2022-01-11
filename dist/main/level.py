try:
    import pygame
    import sys
    import random
    import os

    from settings import *
    from maps import maps, finish_map
    from tiles import Tile
    from player import Player
    from finish import Finish
    from coin import Coin
    from score import score
    from pygame import mixer
    from death import Death
    from take_resourse import resource_path
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


class Level:
    def __init__(self, surface, col=0):
        mixer.init()
        path_money = resource_path(os.path.join('music', 'take_money.mp3'))

        mixer.music.load(
            os.path.join(os.path.join('music', 'phone'), random.choice(os.listdir(os.path.join('music', 'phone')))))
        self.music_take_money = mixer.Sound(path_money)
        path_jump = resource_path(os.path.join('music', 'jump.mp3'))
        self.music_jump = mixer.Sound(path_jump)
        mixer.music.play()
        # настройки уровня
        self.display_surface = surface
        self.die = False
        self.finish = False
        self.word_shift = 0
        self.current_x = 0
        self.score = 0
        self.last_coord = 0
        self.col_levels = 0
        self.setup_level(maps[0])
        self.col = col
        for i in range(col):
            self.create_level(random.choice(maps[1:]))
        self.create_level(finish_map)

    def setup_level(self, layout):
        # create level - создания уровня
        self.tiles_group = pygame.sprite.Group()
        self.deaths_groups = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.finish_group = pygame.sprite.Group()
        self.create_level(layout)

    def create_level(self, layout):
        self.col_levels = 0

        last_coord = 0
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile(self.get_coords(row_index, col_index), tile_size)
                    self.tiles_group.add(tile)
                elif cell == 'P':
                    player_sprite = Player(self.get_coords(row_index, col_index))
                    self.player_group.add(player_sprite)
                elif cell == 'C':
                    if random.randint(0, 2) == 0:
                        coin_sprite = Coin(self.get_coords(row_index, col_index))
                        self.coins_group.add(coin_sprite)
                elif cell == 'D':
                    if random.randint(0, 2) == 0:
                        death = Death(self.get_coords(row_index, col_index), tile_size)
                        self.deaths_groups.add(death)
                    else:
                        tile = Tile(self.get_coords(row_index, col_index), tile_size)
                        self.tiles_group.add(tile)
                elif cell == 'F':
                    finish = Finish(self.get_coords(row_index, col_index), tile_size)
                    self.finish_group.add(finish)
                last_coord = max(last_coord, self.last_coord + col_index * tile_size)
        self.last_coord = last_coord

    def get_coords(self, row_index, col_index):
        return col_index * tile_size + self.last_coord, row_index * tile_size

    def scroll_x(self):
        player = self.player_group.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < width / 4 and direction_x < 0:
            self.word_shift = 8
            player.speed = 0
        elif player_x > width * 0.75 and direction_x > 0:
            self.word_shift = -8
            player.speed = 0
        else:
            self.word_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player_group.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 and not player.is_stay:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 and not player.is_stay:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player_group.sprite
        player.apply_gravity()

        for sprite in self.tiles_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.double_jump = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if (player.on_ground and player.direction.y < 0) or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def col_money(self):
        player = self.player_group.sprite

        for sprite in self.coins_group.sprites():
            if sprite.rect.colliderect(player.rect):
                self.coins_group.remove(sprite)
                self.music_take_money.play()
                self.score += 1

    def is_death(self):
        player = self.player_group.sprite

        for sprite in self.deaths_groups.sprites():
            if sprite.rect.colliderect(player.rect):
                self.die = True

    def is_finish(self):
        player = self.player_group.sprite

        for sprite in self.finish_group.sprites():
            if sprite.rect.colliderect(player.rect):
                self.score += (self.col // 2)
                self.finish = True

    def is_die(self):
        player = self.player_group.sprite
        if player.rect.y > height:
            self.die = True

    def run(self):
        if not in_music:
            mixer.music.stop()

        # level tiles  - построение уровня
        self.tiles_group.update(self.word_shift)
        self.tiles_group.draw(self.display_surface)
        # finish - выйгрышь
        self.finish_group.update(self.word_shift)
        self.finish_group.draw(self.display_surface)
        self.is_finish()
        # coin - монеты
        self.col_money()
        self.coins_group.update(self.word_shift)
        self.coins_group.draw(self.display_surface)
        score(self.score, self.display_surface)
        # death
        self.deaths_groups.update(self.word_shift)
        self.deaths_groups.draw(self.display_surface)
        self.is_death()
        # player - игрок
        self.player_group.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player_group.draw(self.display_surface)
        self.is_die()

        self.scroll_x()
