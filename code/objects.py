import pygame 
from importing import *
from settings import *
from random import choice, randrange
from pygame import mixer


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, surface, create_jump_particals):
        super().__init__()
        self.display_surface = surface
        self.direction = pygame.math.Vector2(0, 0) # направление, изменение положения
        self.sprites = load_sprite_sheets('player1', 16, 16)
        self.image = self.sprites['idle'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (x, y))

        # движение игрока
        self.speed = 2
        self.gravity = 0.2
        self.jump_speed = -3.5 # высота прыжка
        self.on_ground = False
        self.status = 'idle'

        self.on_ceilling = False
        self.on_left = False
        self.on_right = False
        # все, что касается анимации
        self.frame_index = 0
        self.animation_speed = 0.1
        self.facing_right = True
        self.facing_left = False

        self.create_jump_particals = create_jump_particals

    def update_sprites(self):
        name = self.status
        sprites = self.sprites[name]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(sprites):
            self.frame_index = 0
        image = sprites[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = flip(image)
        self.mask = pygame.mask.from_surface(self.image)

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceilling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceilling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceilling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()
        # обработка клавиш для изменения положения по x
        if keys[pygame.K_RIGHT]:
            self.direction.x = PLAYER_VEL
            self.facing_right = True
            self.facing_left = False
        elif keys[pygame.K_LEFT]:
            self.direction.x = -PLAYER_VEL
            self.facing_right = False
            self.facing_left = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            jump_sound = mixer.Sound('sounds/sound_jump.wav')
            jump_sound.set_volume(VOLUME_SOUNDS)
            jump_sound.play()
            x, y = self.rect.midbottom
            self.create_jump_particals((x, y - 3))

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
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
        self.frame_index = 0

    def update(self):
        self.get_input()
        self.get_status()
        self.update_sprites()
        
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = (110, 160)
        self.sprites = load_sprite_sheets('fire', 20, 16)['fires']
        self.animation_speed = 0.2
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(bottomleft = self.pos)
        self.frame_index = 0

    def update_sprites(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        self.image = self.sprites[int(self.frame_index)]
        self.rect = self.image.get_rect(bottomleft = self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.update_sprites()


class Box(Tile):
    def __init__(self):
        self.fly = True
        x, y = choice([(randrange(15, 190), 15), (randrange(15, 190), randrange(91, 96))])
        image = pygame.image.load('working_sprites/box.png').convert_alpha()
        self.rect = image.get_rect(topleft = (x, y))
        super().__init__(x, y, image)
        self.gravify = 3

    def update_pos(self):
        self.rect.x, self.rect.y = choice([(randrange(15, 190), 15), (randrange(15, 190), randrange(91, 96))])
        self.fly = True

    def apply_gravity(self):
        self.rect.y += self.gravify


class Enemy(pygame.sprite.Sprite):
    def __init__(self, direction, pos):
        super().__init__()
        self.sprites = load_sprite_sheets('enemy1', 16, 16)
        self.speed = 1
        self.animation_speed = 0.6
        self.hp = 30
        self.gravify = 2
        self.text_direction = direction
        self.image = self.sprites['run'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = self.speed if direction == 'right' else -self.speed
        self.on_ground = False
        self.frame_index = 0
        self.damage = 0
        self.visible = False
        pygame.time.set_timer(SPAWN_ENEMY, choice([1000, 2000, 3000]))

    def hp_check(self):
        if self.hp < 1:
            self.kill()

    def update_sprites(self):
        name = 'run'
        if self.damage:
            name = 'death'
            self.hp -= self.damage
            self.damage = 0
        elif not self.on_ground:
            name = 'flight'
        elif self.on_ground:
            name = 'run'
        sprites = self.sprites[name]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(sprites):
            self.frame_index = 0
        self.image = sprites[int(self.frame_index)]
        if self.speed < 0:
            self.image = flip(self.image)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.visible:
            self.rect.x += self.speed

    def apply_gravity(self):
        self.rect.y += self.gravify

    def update(self):
        self.hp_check()
        self.update_sprites()
        self.move()


class ParticaleEffect(pygame.sprite.Sprite): # генерация частиц с помощью спрайтов
    def __init__(self, pos, type):
        super().__init__()
        self.type = type
        self.frame_index = 0
        self.animation_speed = 0.2
        self.all_frames = load_sprite_sheets('particales', 16, 16)
        if type == 'boom':
            self.frames = self.all_frames['boom']
            self.frame_index = randrange(0, 1)
            self.x_force = randrange(-5, 30) / 1000
            self.y_force = randrange(-10, 10) / 1000
        elif type == 'jump':
            self.frames = self.all_frames['jump']
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def move(self):
        self.rect.x += self.x_force
        self.rect.y += self.y_force

    def update(self):
        if self.type == 'boom':
            self.move()
        self.animate()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, coords, x, y):
        super().__init__()
        self.image = IMAGE_BULLET
        self.rect = self.image.get_rect(center=coords)
        self.speed_x = x
        self.speed_y = y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def update(self):
        self.move()


class Gun(pygame.sprite.Sprite):
    def __init__(self, gun, player, x_update, y_update):
        super().__init__()
        path = join('working_sprites', 'guns', gun + '.png')
        self.player = player
        self.start_image = pygame.image.load(path).convert_alpha()
        self.image = self.start_image
        self.rect = self.image.get_rect(center=self.image.get_rect().center)
        self.x_update, self.y_update = x_update, y_update
        
    def update(self):
        if self.player.facing_right:
            self.image = flip(self.start_image)
            self.rect.center = self.player.rect.midright
            self.rect.x += self.x_update
            self.rect.y += self.y_update
        else:
            self.image = self.start_image
            self.rect.center = self.player.rect.midleft
            self.rect.x -= self.x_update
            self.rect.y += self.y_update


class Pistol(Gun):
    def __init__(self, player):
        super().__init__('pistol', player, 1, 0)
        self.player = player
        self.power = 15
        self.speed_x = 5
        self.speed_y = 0
        self.long_press = False

    def new_bullet(self):
        if self.player.facing_left:
            bullet = Bullet(self.rect.midleft, -self.speed_x, self.speed_y)
        else:
            bullet = Bullet(self.rect.midright, self.speed_x, self.speed_y)
        return [bullet]


class Shotgun(Gun):
    def __init__(self, player):
        super().__init__('shotgun', player, -1, 2)
        self.player = player
        self.power = 1
        self.speed_x = 5
        self.speed_y = 0
        self.long_press = False


class Bazooka(Gun):
    def __init__(self, player):
        super().__init__('bazooka', player, -2, 1)
        self.player = player
        self.power = 1
        self.speed_x = 5
        self.speed_y = 0
        self.long_press = True
        self.period = 1000

    def new_bullet(self):
        pass


class DualPistols(Gun):
    def __init__(self, player):
        super().__init__('dual pistols', player, -5, 1)
        self.player = player
        self.power = 15
        self.speed_x = 5
        self.speed_y = 0
        self.long_press = False

    def new_bullet(self):
        bullet1 = Bullet(self.rect.midright, -self.speed_x, self.speed_y)
        bullet2 = Bullet(self.rect.midleft, self.speed_x, self.speed_y)
        return [bullet1, bullet2]


class MachineGun(Gun):
    def __init__(self, player):
        super().__init__('machine gun', player, -2, 1)
        self.player = player
        self.power = 5
        self.speed_x = 6
        self.speed_y = 0
        self.long_press = True
        self.period = 170

    def new_bullet(self):
        if self.player.facing_left:
            x, y = self.rect.midleft
            x += 2
            y += 2
            bullet = Bullet(self.rect.midleft, -self.speed_x, self.speed_y)
        else:
            bullet = Bullet(self.rect.midright, self.speed_x, self.speed_y)
        return [bullet]


class Revolver(Gun):
    def __init__(self, player):
        super().__init__('revolver', player, -2, 1)
        self.player = player
        self.power = 30
        self.speed_x = 6
        self.speed_y = 0
        self.long_press = False

    def new_bullet(self):
        if self.player.facing_left:
            bullet = Bullet(self.rect.midleft, -self.speed_x, self.speed_y)
        else:
            bullet = Bullet(self.rect.midright, self.speed_x, self.speed_y)
        return [bullet]


def new_gun():
    all_guns = [Pistol, DualPistols, MachineGun, Revolver]
    return choice(all_guns)