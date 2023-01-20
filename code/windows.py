import pygame
from settings import *
from importing import *
from objects import *
from random import randrange, random, randint


class MainWindow:
    def __init__(self, main_window):
        self.status = 'play'
        self.main_screen = main_window
        self.cursor = pygame.Surface((WIDTH, 130))
        self.cursor.fill('black')
        self.cursor.set_alpha(99)
        self.cursor_pos = (0, 245)
        self.background = pygame.transform.scale(pygame.image.load('working_sprites/menu_background.png'), (WIDTH, HEIGHT))

    def draw(self):
        self.main_screen.blit(self.background, (0, 0))
        self.main_screen.blit(self.cursor, self.cursor_pos)
        draw_text(self.main_screen, 'главное меню', 90, WIDTH // 2, 60)
        draw_text(self.main_screen, 'играть', 80, WIDTH // 2, 300)
        draw_text(self.main_screen, 'информация', 80, WIDTH // 2, 430)
        draw_text(self.main_screen, 'выйти', 80, WIDTH // 2, 560)
        draw_text(self.main_screen, 'f/стрелки для использования меню', 30, WIDTH - 280, HEIGHT - 30)

    def update_cursor(self, type):
        if type: # если 1 - клавиша вверх
            if self.status == 'play':
                self.status = 'quit'
                self.cursor_pos = (0, 505)
            elif self.status == 'quit':
                self.status = 'info'
                self.cursor_pos = (0, 375)
            elif self.status == 'info':
                self.status = 'play'
                self.cursor_pos = (0, 245)
        else:
            if self.status == 'play':
                self.status = 'info'
                self.cursor_pos = (0, 375)
            elif self.status == 'quit':
                self.status = 'play'
                self.cursor_pos = (0, 245)
            elif self.status == 'info':
                self.status = 'quit'
                self.cursor_pos = (0, 505)
    
    def update(self):
        self.draw()


class ResultWindow:
    def __init__(self, main_screen, result):
        self.result = result
        self.main_screen = main_screen
        self.background = pygame.transform.scale(pygame.image.load('working_sprites/menu_background.png'), (WIDTH, HEIGHT))

    def draw(self):
        with open('stats.txt', 'r') as file:
            record = file.readline()
        self.main_screen.blit(self.background, (0, 0))
        draw_text(self.main_screen, 'game over', 110, WIDTH // 2, 60)
        draw_text(self.main_screen, 'ваш результат', 100, WIDTH // 2, 350)
        draw_text(self.main_screen, str(self.result), 100, WIDTH // 2, 450)
        draw_text(self.main_screen, 'ваш рекорд', 100, WIDTH // 2, 550)
        draw_text(self.main_screen, record, 100, WIDTH // 2, 650)
        draw_text(self.main_screen, 'нажмите ПРОБЕЛ, чтобы начать заново', 35, WIDTH / 2, HEIGHT - 60)
        draw_text(self.main_screen, 'нажмите ESC, чтобы выйти в главное меню', 35, WIDTH / 2, HEIGHT - 30)

    def update(self):
        self.draw()


class InfoWindow:
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.status = 'description'
        self.background = pygame.transform.scale(pygame.image.load('working_sprites/menu_background.png'), (WIDTH, HEIGHT))

    def draw(self):
        self.main_screen.blit(self.background, (0, 0))
        if self.status == 'description':
            draw_text(self.main_screen, 'описание', 110, WIDTH // 2, 60)
            draw_text(self.main_screen, 'цель игры - выжить и собрать как можно больше ящиков с оружием.', 25, WIDTH // 2, 200)
            draw_text(self.main_screen, 'игру усложняют враги, убивающие с одного касания.', 25, WIDTH // 2, 230)
            draw_text(self.main_screen, 'если они попадают в огонь, то возраждаются уже более быстрыми.', 25, WIDTH // 2, 260)
        else:
            draw_text(self.main_screen, 'управление', 110, WIDTH // 2, 60)
            draw_text(self.main_screen, 'в меню:', 30, WIDTH // 2, 200)
            draw_text(self.main_screen, 'клавиша F - выбор позиции', 30, WIDTH // 2, 240)
            draw_text(self.main_screen, 'стрелки - перемещение между позициями', 30, WIDTH // 2, 270)
            draw_text(self.main_screen, 'в игре:', 30, WIDTH // 2, 350)
            draw_text(self.main_screen, 'стрелки вправо/влево - передвижение игрока по карте', 30, WIDTH // 2, 390)
            draw_text(self.main_screen, 'пробел - прыжок', 30, WIDTH // 2, 420)
            draw_text(self.main_screen, 'клавиша F - стрельба', 30, WIDTH // 2, 450)
            draw_text(self.main_screen, 'клавиша Esc - возращение в предыдущее окно/выход из игры', 30, WIDTH // 2, 500)
        draw_text(self.main_screen, '<', 100, 50, HEIGHT // 2)
        draw_text(self.main_screen, '>', 100, WIDTH - 50, HEIGHT // 2)

    def update_win(self):
        if self.status == 'description':
            self.status = 'management'
        else:
            self.status = 'description'

    def update(self):
        self.draw()


class Level:
    def __init__(self, level_num, main_screen):
        self.stop_game = False
        self.main_screen = main_screen
        self.scroll = 0
        self.display_surface = pygame.Surface((width_d, height_d))
        self.tiles_sprites = import_csv_layout(level_num)
        self.tile_list = import_cut_graphics('working_sprites/tiles.png')
        self.setup_level(self.tiles_sprites)
        self.current_x = 0
        self.box_count = 0
        self.time_for_bullets = pygame.time.get_ticks()
        self.percent_of_enemy = 0.3 # 30%
        self.dust_sprite = pygame.sprite.Group()

    def create_jump_particles(self, pos):
        jump_partical_sprite = ParticaleEffect(pos, 'jump')
        self.dust_sprite.add(jump_partical_sprite)

    def create_boom_particles(self, pos):
        x, y = pos
        for i in range(5):
            rx, ry = randrange(-10, 10), randrange(-2, 2)
            partical = ParticaleEffect((x + rx, y - ry), 'boom')
            self.dust_sprite.add(partical)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.box = pygame.sprite.GroupSingle()
        self.gun = pygame.sprite.GroupSingle()
        self.bullets = pygame.sprite.Group()
        self.fire = pygame.sprite.GroupSingle()
        for row_i, row in enumerate(layout):
            for col_i, value in enumerate(row):
                if value != '-1':
                    x, y = col_i * TILE_SIZE, row_i * TILE_SIZE
                    sprite = Tile(x, y, self.tile_list[int(value)])
                    self.tiles.add(sprite)
        player_sprite = Player(100, 100, self.display_surface, self.create_jump_particles)
        self.player.add(player_sprite)
        self.box.add(Box())
        self.gun.add(Pistol(self.player.sprite))
        self.fire.add(Fire())

    def horizontal_movement_collision(self): # столкновение со сторонами
        player = self.player.sprite 
        player.rect.x += player.direction.x * player.speed
        player.mask = pygame.mask.from_surface(player.image)
        for tile in self.tiles.sprites():
            if pygame.sprite.collide_mask(player, tile):
                if player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                elif player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            self.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            self.on_right = False

    def vertical_movement_collision(self): # столкновение с полом и потолком
        player = self.player.sprite
        player.apply_gravity()

        for tile in self.tiles.sprites():
            if pygame.sprite.collide_mask(player, tile):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceilling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceilling and player.direction.y > 0:
            player.on_ceilling = False

    def player_collision_box(self):
        player = self.player.sprite.rect
        box = self.box.sprite.rect
        if player.colliderect(box):
            self.box.sprite.update_pos()
            gun = new_gun()(self.player.sprite)
            while gun.__class__.__name__ == self.gun.sprite.__class__.__name__:
                gun = new_gun()(self.player.sprite)
            self.gun.add(gun)
            self.box_count += 1
            sound = mixer.Sound('sounds/sound_pickup.wav')
            self.create_boom_particles(player.center)
            sound.set_volume(VOLUME_SOUNDS)
            sound.play()

    def stop_game_f(self):
        player_rect = self.player.sprite.rect
        if not self.display_surface.get_rect().contains(player_rect) or pygame.sprite.spritecollide(self.player.sprite, self.enemies, True):
            self.stop_game = True

    def enemy_collision_reverse(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.tiles, False):
                enemy.speed *= -1

    def enemy_collision_vertical(self):
        for enemy in self.enemies.sprites():
            enemy.apply_gravity()
            tiles = pygame.sprite.spritecollide(enemy, self.tiles, False)
            for tile in tiles:
                if enemy.rect.y > 0:
                    enemy.rect.bottom = tile.rect.top
                    enemy.on_ground = True
    
    def vertical_collision_boxs(self):
        box = self.box.sprite
        box.apply_gravity()
        tiles = pygame.sprite.spritecollide(box, self.tiles, False)
        for tile in tiles:
            if box.rect.y > 0:
                box.rect.bottom = tile.rect.top
                if box.fly:
                    self.create_boom_particles(box.rect.center)
                    box.fly = False

    def enemy_bullet_collision(self):
        for bullet in self.bullets:
            enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in enemies:
                enemy.damage = self.gun.sprite.power
                bullet.kill()

    def bullet_tiles_collision(self):
        for bullet in self.bullets:
            tiles = pygame.sprite.spritecollide(bullet, self.tiles, False)
            if tiles:
                bullet.kill()

    def fire_enemy_collision(self):
        fire = self.fire.sprite
        for enemy in self.enemies.sprites():
            if pygame.sprite.collide_mask(fire, enemy):
                enemy.sprites = load_sprite_sheets('angry_enemy1', 16, 16)
                enemy.speed = 2
                enemy.frame_index = 0
                enemy.rect.topleft = (116, -25)
                enemy.visible = False
                enemy.rect = enemy.image.get_rect(topleft = (116, -25))
                
    def scrolling_the_sky(self):
        for i in range(0, TILES):
            self.display_surface.blit(BACKGROUND, (i * BG_WIDTH + self.scroll, 0))
        self.scroll -= 0.5
        if abs(SCROLL) > BG_WIDTH:
            self.scroll = 0

    def adding_new_bullet(self):
        for bullet in self.gun.sprite.new_bullet():
            self.bullets.add(bullet)
            gun_sound = mixer.Sound('sounds/sound_hit2.wav')
            gun_sound.set_volume(VOLUME_SOUNDS)
            gun_sound.play()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_f]:
            current_time = pygame.time.get_ticks()
            if current_time - self.time_for_bullets > self.gun.sprite.period:
                self.time_for_bullets = current_time
                self.adding_new_bullet()
            
    def adding_enemies(self):
        if random() < self.percent_of_enemy:
            for _ in range(randint(1, 5)):
                direction = choice(['right', 'left'])
                pos = (117, randrange(-500, -25)) if direction == 'right' else (117, randrange(-500, -25))
                self.enemies.add(Enemy(direction, pos))

    def check_enemy_visible(self):
        for enemy in self.enemies:
            if self.display_surface.get_rect().contains(enemy.rect) and enemy.rect.y > 10:
                enemy.visible = True

    def run(self, main_screen):
        if self.gun.sprite.long_press:
            self.get_input()
        if len(self.enemies.sprites()) < 1:
            self.adding_enemies()
        self.check_enemy_visible()
        # первый слой - задний подвижный фон
        self.scrolling_the_sky()
        # второй статичный фон
        self.display_surface.blit(BACKGROUND_1, (0, 0))
        # частицы
        self.dust_sprite.update()
        self.dust_sprite.draw(self.display_surface)
        # коробочки эти
        self.vertical_collision_boxs()
        self.box.draw(self.display_surface)
        # пули
        self.bullets.update()
        self.bullets.draw(self.display_surface)
        self.bullet_tiles_collision()
        # игрок
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player_collision_box()
        self.player.draw(self.display_surface)
        self.stop_game_f()
        # оружие
        self.gun.update()
        self.gun.draw(self.display_surface)
        # блоки
        self.tiles.draw(self.display_surface)
        # враги
        self.enemy_bullet_collision()
        self.enemy_collision_reverse()
        self.enemy_collision_vertical()
        self.enemies.update()
        self.enemies.draw(self.display_surface)
        # огонь
        self.fire_enemy_collision()
        self.fire.update()
        self.fire.draw(self.display_surface)
        # счет
        draw_text(self.display_surface, str(self.box_count), 16, width_d / 2, 20)
        # отображение всего на главном экране
        surface = pygame.transform.scale(self.display_surface, (WIDTH, HEIGHT))
        main_screen.blit(surface, (0, 0))
