# class Button
import pygame
from settings import *


class Button:
    def __init__(self, x, y, image, scale, rect_width=6, color_rect=GRAY):
        self.show_rect_color = None
        self.show_rect = None
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.focus = False
        self.rect_width = rect_width
        self.color_rect = color_rect

    def draw(self, screen):
        if self.focus:
            pygame.draw.rect(screen, self.show_rect_color, self.show_rect)

        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.show_rect = pygame.Rect(0, 0, self.rect.size[0] + self.rect_width,
                                         self.rect.size[1] + self.rect_width)
            self.show_rect.center = self.rect.center
            self.show_rect_color = self.color_rect
            self.focus = True
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                action = True

            if self.clicked:
                self.show_rect_color = LIGHT_GRAY

        else:
            self.clicked = False
            self.focus = False

        return action
