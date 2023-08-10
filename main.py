import pygame
import sys
from settings import *
from character import *
from level import *
from gui import *


class Game:
    def __init__(self):
        pygame.init()

        self.running = True

        # Screen creation
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GAME')
        self.clock = pygame.time.Clock()

        # Initialization level
        self.level = Level()
        self.init_level_True = True

        # Initialization font
        self.font = pygame.font.SysFont("Times New Roman", 50)

        # Game state
        self.game_state = 0
        self.game_pause = False

        # Start menu
        self.start_menu = StartMenu(self)

        # Pause button
        self.pause_button = Button(WIDTH - 60, 10, pygame.image.load('resources/button_pause.png'), 1)

        # Pause menu
        self.pause_menu = PauseMenu(self)

        # Settings menu
        self.settings_menu = SettingsMenu(self)

        # Win menu
        self.win_menu = EndGameWindow(self)

        # Lose time menu
        self.lose_time_menu = EndGameWindow(self, 'TIME IS UP', BLUE)

        # Lose health menu
        self.lose_health_menu = EndGameWindow(self, 'YOU DIE', RED)

    def run(self):
        global FPS
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.level.player.expe > 0:
                        self.level.player.shoot()
                        self.level.player.expe -= 1

                if self.settings_menu.fps_plus_button.update() and FPS < 90:
                    self.settings_menu.count_fps += 1
                    FPS += 1
                    self.settings_menu.update()

                if self.settings_menu.fps_minus_button.update() and FPS > 10:
                    self.settings_menu.count_fps -= 1
                    FPS -= 1
                    self.settings_menu.update()

            if self.pause_button.update():
                self.game_state = 3

            if self.game_state == 0:
                self.init_level_True = True
                self.level.player.restart()
                self.start_menu.update()

            if self.game_state == 1:
                if self.init_level_True:
                    self.level.__init__()
                    self.init_level_True = False
                self.screen.fill((0, 191, 255))
                self.level.run()
                self.pause_button.draw(self.screen)
                self.pause_button.update()

            if self.game_state == 2:
                self.settings_menu.update()

            if self.game_state == 3:
                self.pause_menu.update()

            if self.level.player.money == 15:
                self.win_menu.update()

            if self.level.player.time_off:
                self.lose_time_menu.update()

            if self.level.player.health <= 0:
                self.lose_health_menu.update()

            for part in self.level.player.experience_part_group:
                pygame.draw.rect(self.screen, RED, part.hitbox)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
