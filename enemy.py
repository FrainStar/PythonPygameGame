import pygame
import random
from settings import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.fire_rect = None
        self.fire_image = None
        self.image = pygame.image.load('resources/sprite_enemy.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.name_sprite = 'Mob'
        self.speed = 5

    def shoot(self, all_sprite, bullet_group):
        for i in range(5):
            bullet = Bullet(self.rect.centerx, self.rect.top, random.randrange(-10, 10), random.randrange(-10, 10))
            all_sprite.add(bullet)
            bullet_group.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/sprite_slime.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
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

