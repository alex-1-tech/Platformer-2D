try:
    import sys
    from maps import *
except ImportError as err:
    print("Could't load module. %s" % err)
    sys.exit(2)

vertical_tile_number = 11
tile_size = 64
screen_size = width, height = 1280, 704
in_music = True
FPS = 60
