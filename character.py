# class Player and class PlayerCamera
import random
import pygame
import math
from settings import *
from enemy import *


def get_image(sheet, width, height, frame, scale=4, color=BLACK):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image


class BulletPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/sprite_explosion.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = speedx
        self.speedy = speedy
        self.hitbox = self.rect.inflate(0, 0)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.hitbox.x += self.speedx
        self.hitbox.y += self.speedy
        if self.rect.bottom == 0 or self.rect.top == 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_group, coin_group, bullet_group,
                 mob_group, all_group, time_group, hp_group, experience_group):

        super().__init__()
        self.pos = pos
        self.image_list = []

        sprite_sheet_image = pygame.image.load('resources/sprite_player.png').convert_alpha()
        for i in range(14):
            image = get_image(sprite_sheet_image, 24, 24, i)
            self.image_list.append(image)
        self.walk_index = list(range(0, 14))
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(-45, -40)

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.head_left = None

        # Sprite groupes
        self.collision_sprite = collision_group
        self.coin_sprite = coin_group
        self.bullet_group = bullet_group
        self.mob_group = mob_group
        self.all_sprite = all_group
        self.time_group = time_group
        self.hp_group = hp_group
        self.experience_group = experience_group
        self.experience_part_group = pygame.sprite.Group()
        self.bullet_player_group = pygame.sprite.Group()

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Info about player
        self.health = 100
        self.money = 0
        self.expe = 0

        # Time
        self.clock = pygame.time.Clock()
        self.timer = 75
        self.dt = 30 / 1000
        self.time_off = False

        # Sounds
        self.coin_sound = pygame.mixer.Sound('resources/music_coin.mp3')
        self.coin_sound.set_volume(0.1)
        self.damage_sound = pygame.mixer.Sound('resources/music_damage.mp3')
        self.damage_sound.set_volume(0.2)
        self.time_sound = pygame.mixer.Sound('resources/music_timesprite.mp3')
        self.hp_sound = pygame.mixer.Sound('resources/music_hp.mp3')
        self.expe_sound = pygame.mixer.Sound('resources/music_expe.mp3')
        self.expe_sound.set_volume(0.2)
        self.mob_kill_sound = pygame.mixer.Sound('resources/music_mob_kill.mp3')

    def input(self):
        keys = pygame.key.get_pressed()

        if self.direction == (0, 0) and self.head_left == False:
            self.index = self.walk_index[0]
            self.image = self.image_list[self.index]
        elif self.direction == (0, 0) and self.head_left == True:
            self.index = self.walk_index[0]
            self.image = pygame.transform.flip(self.image_list[self.index], True, False).convert_alpha()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.index += 1
            if self.index not in self.walk_index:
                self.index = self.walk_index[0]
            self.image = self.image_list[self.index]
            if self.head_left:
                self.image = pygame.transform.flip(self.image_list[self.index], True, False).convert_alpha()

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.index += 1
            if self.index not in self.walk_index:
                self.index = self.walk_index[0]
            self.image = self.image_list[self.index]
            if self.head_left:
                self.image = pygame.transform.flip(self.image_list[self.index], True, False).convert_alpha()
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.head_left = False
            self.direction.x = 1
            self.index += 1
            if self.index not in self.walk_index:
                self.index = self.walk_index[0]
            self.image = self.image_list[self.index]

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.head_left = True
            self.direction.x = -1
            self.index += 1
            if self.index not in self.walk_index:
                self.index = self.walk_index[0]
            self.image = pygame.transform.flip(self.image_list[self.index], True, False).convert_alpha()
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
            for coin in self.coin_sprite:
                if coin.hitbox.colliderect(self.hitbox):
                    self.money += 1
                    self.coin_sound.play()
                    coin.kill()
            for bullet in self.bullet_group:
                if bullet.hitbox.colliderect(self.hitbox):
                    self.health -= random.randint(4, 20)
                    self.damage_sound.play()
                    bullet.kill()
            for mob in self.mob_group:
                if mob.hitbox.colliderect(self.hitbox):
                    self.health -= 0.1
            for time in self.time_group:
                if time.hitbox.colliderect(self.hitbox):
                    self.time_sound.play()
                    self.timer += 3
                    time.kill()
            for hp in self.hp_group:
                if hp.hitbox.colliderect(self.hitbox):
                    self.hp_sound.play()
                    self.health += 5
                    hp.kill()
            for expe in self.experience_group:
                if expe.hitbox.colliderect(self.hitbox):
                    expe.shoot(self.all_sprite, self.experience_part_group)
                    self.expe_sound.play()
                    expe.kill()
            for part in self.experience_part_group:
                if part.hitbox.colliderect(self.hitbox) and (-1 < part.speedx < 1) and (-1 < part.speedy < 1):
                    self.expe += random.randint(1, 3)
                    self.expe_sound.play()
                    part.kill()
            for b in self.bullet_player_group:
                for m in self.mob_group:
                    if b.hitbox.colliderect(m.hitbox):
                        self.mob_kill_sound.play()
                        m.kill()
                        b.kill()

        if direction == 'vertical':
            for sprite in self.collision_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
            for coin in self.coin_sprite:
                if coin.hitbox.colliderect(self.hitbox):
                    self.coin_sound.play()
                    self.money += 1
                    coin.kill()
            for bullet in self.bullet_group:
                if bullet.hitbox.colliderect(self.hitbox):
                    self.health -= random.randint(4, 20)
                    self.damage_sound.play()
                    bullet.kill()
            for mob in self.mob_group:
                if mob.hitbox.colliderect(self.hitbox):
                    self.damage_sound.play()
                    self.health -= 0.1
            for time in self.time_group:
                if time.hitbox.colliderect(self.hitbox):
                    self.time_sound.play()
                    self.timer += 3
                    time.kill()
            for hp in self.hp_group:
                if hp.hitbox.colliderect(self.hitbox):
                    self.hp_sound.play()
                    self.health += 5
                    hp.kill()
            for expe in self.experience_group:
                if expe.hitbox.colliderect(self.hitbox):
                    expe.shoot(self.all_sprite, self.experience_part_group)
                    self.expe_sound.play()
                    expe.kill()
            for part in self.experience_part_group:
                if part.hitbox.colliderect(self.hitbox) and (-1 < part.speedx < 1) and (-1 < part.speedy < 1):
                    self.expe += random.randint(1, 3)
                    self.expe_sound.play()
                    part.kill()
            for b in self.bullet_player_group:
                for m in self.mob_group:
                    if b.hitbox.colliderect(m.hitbox):
                        self.mob_kill_sound.play()
                        m.kill()
                        b.kill()

    def restart(self):
        self.timer = 75
        self.time_off = False
        self.money = 0
        self.health = 100
        self.money = 0
        self.expe = 0

    def shoot(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]

        if pos_x > 637 and pos_y < 356:
            a = pos_x - 637
            b = 356 - pos_y
            c = math.sqrt(a ** 2 + b ** 2)
            t = c / 10
            speedx = a / t
            speedy = -b / t
            bullet = BulletPlayer(self.rect.centerx, self.rect.centery, speedx, speedy)
            self.all_sprite.add(bullet)
            self.bullet_player_group.add(bullet)

        elif pos_x < 637 and pos_y < 356:
            a = 637 - pos_x
            b = 356 - pos_y
            c = math.sqrt(a ** 2 + b ** 2)
            t = c / 10
            speedx = -a / t
            speedy = -b / t
            bullet = BulletPlayer(self.rect.centerx, self.rect.centery, speedx, speedy)
            self.all_sprite.add(bullet)
            self.bullet_player_group.add(bullet)

        elif pos_x < 637 and pos_y > 356:
            a = 637 - pos_x
            b = pos_y - 356
            c = math.sqrt(a ** 2 + b ** 2)
            t = c / 10
            speedx = -a / t
            speedy = b / t
            bullet = BulletPlayer(self.rect.centerx, self.rect.centery, speedx, speedy)
            self.all_sprite.add(bullet)
            self.bullet_player_group.add(bullet)

        elif pos_x > 637 and pos_y > 356:
            a = pos_x - 637
            b = pos_y - 356
            c = math.sqrt(a ** 2 + b ** 2)
            t = c / 10
            speedx = a / t
            speedy = b / t
            bullet = BulletPlayer(self.rect.centerx, self.rect.centery, speedx, speedy)
            self.all_sprite.add(bullet)
            self.bullet_player_group.add(bullet)

    def update(self):

        # Amount time
        self.timer -= self.dt
        if self.timer <= 0:
            self.time_off = True
            self.timer = 0
            self.kill()

        # Player update
        self.input()
        self.move(self.speed)


class PlayerCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load('resources/sprite_map.jpg').convert()
        self.floor_surf = pygame.transform.rotozoom(self.floor_surf, 0, 2).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
