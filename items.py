import random

import pygame
from character import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, scale=0.08):
        super().__init__()
        self.money_list = []
        self.money_sheet_image = pygame.image.load('resources/sprite_money.png').convert_alpha()
        for i in range(6):
            image = get_image(self.money_sheet_image, 140, 177, i).convert_alpha()
            image = pygame.transform.rotozoom(image, 0, scale).convert_alpha()
            self.money_list.append(image)
        self.walk_index = list(range(0, 6))
        self.index = 0
        self.image = self.money_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.display_surface = display_surface
        self.hitbox = self.rect.inflate(0, -10)

    def update(self):
        self.index += 1
        if self.index not in self.walk_index:
            self.index = self.walk_index[0]
        self.image = self.money_list[self.index]
        self.display_surface.blit(self.image, self.rect)


class TimeSprite(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, scale=0.5):
        super().__init__()
        self.image = pygame.image.load('resources/sprite_time.png')
        self.image = pygame.transform.rotozoom(self.image, 0, scale).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.display_surface = display_surface
        self.hitbox = self.rect.inflate(0, -10)

    def update(self):
        self.display_surface.blit(self.image, self.rect)


class HpSprite(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, scale=0.08):
        super().__init__()
        self.image = pygame.image.load('resources/sprite_hp.png')
        self.image = pygame.transform.rotozoom(self.image, 0, scale).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.display_surface = display_surface
        self.hitbox = self.rect.inflate(0, -10)

    def update(self):
        self.display_surface.blit(self.image, self.rect)


class ExperienceSpritePart(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
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
        if self.speedx > 0:
            self.speedx -= 0.05
        if self.speedx < 0:
            self.speedx += 0.05
        if self.speedx == 0:
            self.speedx = 0

        if self.speedy > 0:
            self.speedy -= 0.05
        if self.speedy < 0:
            self.speedy += 0.05
        if self.speedy == 0:
            self.speedy = 0


class ExperienceSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.fire_rect = None
        self.fire_image = None
        self.image = pygame.image.load('resources/sprite_experience.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.01)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.speed = 5

    def shoot(self, all_sprite, bullet_group):
        for i in range(random.randint(5, 10)):
            experience = ExperienceSpritePart(self.rect.centerx, self.rect.top,
                                              random.randrange(-5, 5), random.randrange(-5, 5))
            all_sprite.add(experience)
            bullet_group.add(experience)
