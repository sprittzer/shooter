import pygame, sys
from os import listdir
from os.path import isfile, join
from settings import *
from windows import *
from pygame import mixer

# инициализация модуля pygame
pygame.init()
pygame.display.set_caption('')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def main_menu():
    menu = MainWindow(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_f:
                    status = menu.status
                    if status == 'play':
                        level()
                    elif status == 'settings':
                        settings()
                    elif status == 'quit':
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_UP:
                    menu.update_cursor(1)
                elif event.key == pygame.K_DOWN:
                    menu.update_cursor(0)
        screen.fill('black')
        menu.update()

        pygame.display.update()
        clock.tick(FPS)


def settings():
    menu = Settings(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_f:
                    menu.get_input()
                elif event.key == pygame.K_UP:
                    menu.update_cursor()
                elif event.key == pygame.K_DOWN:
                    menu.update_cursor()
        screen.fill('black')
        menu.update()

        pygame.display.update()
        clock.tick(FPS)


def result_window(result):
    sound = mixer.Sound('sounds/game over.wav')
    sound.set_volume(VOLUME_SOUNDS)
    sound.play()
    window = ResultWindow(screen, result)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_SPACE:
                    level()
        screen.fill('black')
        window.update()
        pygame.display.update()
        clock.tick(FPS)
    

def level():
    level = Level(1, screen)
    mixer.music.load('sounds/menu_music.mp3') 
    mixer.music.set_volume(VOLUME_MUSIC)
    mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == SPAWN_ENEMY:
                level.adding_enemies()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    mixer.music.stop()
                    main_menu()
                elif event.key == pygame.K_f and not level.gun.sprite.long_press:
                    level.adding_new_bullet()
        screen.fill('black')
        level.run(screen)
        if level.stop_game:
            result = level.box_count
            with open('stats.txt', 'r') as file:
                record = file.readline()
                if record == '' or (int(record) < result):
                    with open('stats.txt', 'w') as file1:
                        file1.write(str(result))
                running = False
                mixer.music.stop()
            result_window(result)

        pygame.display.update()
        clock.tick(FPS)

main_menu()