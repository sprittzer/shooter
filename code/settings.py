import pygame
#в данном файле представленные константы для работы программы
#------------------------------------------------------------
WIDTH, HEIGHT = 1200, 800 # размеры ОКНА
FONT = 'EpilepsySansBold.ttf'
width_d, height_d = 240, 160 # размеры происходящего в игре, игрового пространства?, display
TILE_SIZE = 10
FPS = 60
PLAYER_VEL = 1
BACKGROUND = pygame.transform.scale(pygame.image.load("working_sprites/background.png"), (width_d, height_d))
BACKGROUND_1 = pygame.image.load('working_sprites/background0.png')
IMAGE_BULLET = pygame.image.load('working_sprites/bullet.png')
BG_WIDTH = BACKGROUND.get_width()
VOLUME_MUSIC = 0.8
VOLUME_SOUNDS = 0.5
TILES = 1000
SCROLL = 0
SPAWN_ENEMY = pygame.USEREVENT + 1
STOP_GAME = pygame.USEREVENT + 2