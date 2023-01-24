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
esc_sound = mixer.Sound('sounds/esc.wav')
press_sound = mixer.Sound('sounds/press.wav')
choice_sound = mixer.Sound('sounds/choice.wav')
esc_sound.set_volume(VOLUME_SOUNDS)
press_sound.set_volume(VOLUME_SOUNDS)
choice_sound.set_volume(VOLUME_SOUNDS)


# функция для отображения главного окна
def main_menu():
    menu = MainWindow(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_f:
                    press_sound.play()
                    status = menu.status
                    if status == 'play':
                        level()
                    elif status == 'info':
                        info()
                    elif status == 'quit':
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_UP:
                    choice_sound.play()
                    menu.update_cursor(1)
                elif event.key == pygame.K_DOWN:
                    choice_sound.play()
                    menu.update_cursor(0)
        screen.fill('black')
        menu.update()

        pygame.display.update()
        clock.tick(FPS)


# функция для отображения окна с описанием
def info():
    menu = InfoWindow(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    menu.status = 'description'
                    main_menu()
                elif event.key == pygame.K_LEFT:
                    choice_sound.play()
                    menu.update_win()
                elif event.key == pygame.K_RIGHT:
                    choice_sound.play()
                    menu.update_win()
        screen.fill('black')
        menu.update()

        pygame.display.update()
        clock.tick(FPS)


# функция для отображения окна с результатом игры
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
                    esc_sound.play()
                    main_menu()
                elif event.key == pygame.K_SPACE:
                    press_sound.play()
                    level()
        screen.fill('black')
        window.update()
        pygame.display.update()
        clock.tick(FPS)
    

# функция для отображения игры
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
                    esc_sound.play()
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
                mixer.music.stop()
            result_window(result)

        pygame.display.update()
        clock.tick(FPS)

main_menu()