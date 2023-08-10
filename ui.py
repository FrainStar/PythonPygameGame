# class UI
import pygame
from character import *
import sys
from items import *
from button import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Times New Roman", 26)
        self.font_big = pygame.font.SysFont("Times New Roman", 200)

        # HP
        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)

        # Expe
        self.expe_bar_rect = pygame.Rect(10, 35, 200, 20)

        # Money
        self.money = Coin((0, 50), self.display_surface)

    def show_bar_health(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, (128, 128, 128), bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, BLACK, current_rect, 2)

    def show_bar_expe(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, (128, 128, 128), bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, BLACK, current_rect, 2)

    def display(self, player):
        self.show_bar_health(player.health, 100, self.health_bar_rect, (255, 0, 0))
        self.show_bar_health(player.expe, 100, self.expe_bar_rect, BLUE)

        self.money.update()

        num_money = self.font.render(f'x {player.money}', True, (255, 255, 0))
        self.display_surface.blit(num_money, (42, 63))
        num_time = self.font.render(f'{round(player.timer)}', True, (255, 255, 0))
        self.display_surface.blit(num_time, (WIDTH - 100, 10))
