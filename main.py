try:
    import pygame
    import sys
    import os

    from settings import *
    from tiles import Tile
    from level import Level
    from main_menu import Menu
    from restart import Restart
    from change_difficulty import Difficulty_menu
    from pygame import mixer
    from take_resourse import resource_path
    from load_game import start_game
    from null_settings import set_null
    from shop import Shop
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)


# set_null()
def change_score(change_score):
    current_score = int(open('score.txt').read())
    f = open('score.txt', 'w')
    current_score += change_score
    f.write(str(current_score))


def game():
    # settings game - настройки игры

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    start_game(screen)
    clock = pygame.time.Clock()
    difficulty_menu = Difficulty_menu(screen)
    shop_menu = Shop(screen)
    menu = Menu(screen, difficulty_menu, shop_menu)
    restart = Restart(screen, menu, difficulty_menu)
    path = resource_path(os.path.join('sprites', 'background', 'parallax-demon-woods-close-trees.png'))
    background_image = pygame.image.load(path).convert_alpha()
    running = True
    level = Level(screen)
    is_finish = False
    while running:
        screen.fill((30, 30, 30))
        screen.blit(background_image, (0, 0))
        if level.die or level.finish:
            change_score(level.score)
        if level.die:
            restart.state = True
            level.die = False
            is_finish = False
        if level.finish:
            restart.state = True
            level.finish = False
            is_finish = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_menu.state:
                    shop_menu.pressed()
                elif menu.state:
                    menu.pressed()
                elif restart.state:
                    restart.pressed()
                elif difficulty_menu.state:
                    none_level = difficulty_menu.pressed()
                    if none_level != None:
                        level = none_level
        if restart.state:
            restart.run(is_finish)
        elif shop_menu.state:
            shop_menu.run()
        elif menu.state:
            menu.run()
        elif difficulty_menu.state:
            difficulty_menu.run()
        else:
            level.run()
        pygame.display.update()
        clock.tick(FPS)


# Start game - начало игры
if __name__ == '__main__':
    game()
