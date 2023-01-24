import pygame
from csv import reader
from settings import TILE_SIZE, FONT
from os import listdir
from os.path import isfile, join


def import_csv_layout(num_of_level):
    tiles_map = []
    with open(f'levels/level{num_of_level}.csv') as map:
        level = reader(map, delimiter=',')
        for row in level:
            tiles_map.append(list(row))
    return tiles_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_y = int(surface.get_size()[1] / TILE_SIZE)
    cur_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            new_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cur_tiles.append(new_surface)
    return cur_tiles


def flip(sprite):
    return pygame.transform.flip(sprite, True, False)


def load_sprite_sheets(dir1, width, height):
    path = join('working_sprites', dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))] # список с названиями изображений
    all_sprites = {} # словарь движение_сторона - конкретное изображение
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() # исходное общее изображение
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            surface1 = pygame.Surface(surface.get_bounding_rect().size, pygame.SRCALPHA, 32)
            surface1.blit(surface, (0, 0), surface.get_bounding_rect())
            sprites.append(surface1)
        all_sprites[image.replace('.png', '')] = sprites
    return all_sprites


def draw_text(display, text, size, x, y):
    font = pygame.font.Font(FONT, size)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    display.blit(text_surface, text_rect)