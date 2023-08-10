# class Level
import random

import pygame
from settings import *
from character import *
from weapon import *
from ui import *
from enemy import *
from items import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, size):
        super().__init__()
        self.image = image
        self.image = pygame.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)


class Level:
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite groupes
        self.all_sprite = PlayerCamera()
        self.collision_sprite = pygame.sprite.Group()
        self.coin_sprite = pygame.sprite.Group()
        self.mob_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.time_group = pygame.sprite.Group()
        self.hp_group = pygame.sprite.Group()
        self.experience_group = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()

        # Fire cooldown
        self.fire_clock = pygame.time.Clock()
        self.fire_timer = 10
        self.fire_dt = FPS / 1000

    def create_map(self):
        for row_index, row in enumerate(map_plan):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 1:
                    tile = Tile((x, y), pygame.image.load('resources/sprite_water.png').convert_alpha(), 0.07)
                    self.all_sprite.add(tile)
                    self.collision_sprite.add(tile)

                elif col == 2:
                    self.player = Player((x, y), self.collision_sprite, self.coin_sprite,
                                         self.bullet_group, self.mob_group, self.all_sprite,
                                         self.time_group, self.hp_group,self.experience_group)
                    self.all_sprite.add(self.player)

                elif col == 3:
                    mob = Mob((x, y))
                    self.all_sprite.add(mob)
                    self.mob_group.add(mob)

                elif col == 4:
                    coin = Coin((x, y), self.display_surface)
                    self.all_sprite.add(coin)
                    self.coin_sprite.add(coin)

                elif col == 5:
                    time_sprite = TimeSprite((x, y), self.display_surface)
                    self.all_sprite.add(time_sprite)
                    self.time_group.add(time_sprite)

                elif col == 6:
                    hp_sprite = HpSprite((x, y), self.display_surface)
                    self.all_sprite.add(hp_sprite)
                    self.hp_group.add(hp_sprite)

                elif col == 7:
                    expe = ExperienceSprite((x, y))
                    self.all_sprite.add(expe)
                    self.experience_group.add(expe)
                    # self.mob_group.add(expe)

        for i in range(15):
            tile = Tile((random.randint(20, 3100), random.randint(20, 1500)),
                        pygame.image.load('resources/sprite_flower.png').convert_alpha(),
                        1)
            self.all_sprite.add(tile)

            stone = Tile((random.randint(20, 3100), random.randint(20, 1500)),
                         pygame.image.load('resources/sprite_stone.png').convert_alpha(),
                         1)
            self.all_sprite.add(stone)

    def run(self):
        self.fire_timer -= self.fire_dt
        if self.fire_timer <= 0:
            self.fire_timer = 8

        if self.fire_timer % 8 == 0:
            for sprite in self.mob_group:
                sprite.shoot(self.all_sprite, self.bullet_group)

        self.all_sprite.custom_draw(self.player)
        self.all_sprite.update()
        self.ui.display(self.player)
