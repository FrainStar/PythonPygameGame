# class GUI
import pygame
from settings import *
from ui import *
from button import *


class PauseMenu:
    def __init__(self, game):

        # Text font
        font = pygame.font.SysFont("Comic Sans", 100)
        self.font1 = pygame.font.SysFont("Comic Sans", 50)

        # Buttons
        self.resume_button = Button(1140, 650, pygame.image.load('resources/button_resume.png'), 1)
        self.exit_button = Button(1200, 650, pygame.image.load('resources/button_exit.png'), 1)

        # Texts
        self.game_title = font.render(f'Pause', True, (0, 0, 0))
        self.game_title_rect = self.game_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 300))
        self.health_text = None
        self.health_text_rect = None
        self.money_text = None
        self.money_text_rect = None
        self.time_text = None
        self.time_text_rect = None

        # Background
        self.back_image = pygame.image.load('resources/sprite_background.jpg').convert_alpha()
        self.back_image = pygame.transform.rotozoom(self.back_image, 0, 0.8)

        # Other
        self.game = game
        self.screen = self.game.screen

        # Money
        self.money = Coin((WIDTH / 2, HEIGHT / 2 - 170), self.game.screen, 0.2)

    def update(self):

        # Player health rect update
        bg_rect = pygame.Rect(WIDTH / 2, HEIGHT / 2 - 205, 200, 20)
        current = self.game.level.player.health
        max_amount = 100
        color = (255, 0, 0)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Texts update
        self.health_text = self.font1.render(f'Health: {round(self.game.level.player.health)}', True, (255, 0, 0))
        self.health_text_rect = self.health_text.get_rect(center=(WIDTH / 2 - 150, HEIGHT / 2 - 200))
        self.money_text = self.font1.render(f'Money: {self.game.level.player.money}', True, (255, 255, 0))
        self.money_text_rect = self.money_text.get_rect(center=(WIDTH / 2 - 150, HEIGHT / 2 - 100))
        self.time_text = self.font1.render(f'Time left: {round(self.game.level.player.timer)}', True, BLACK)
        self.time_text_rect = self.time_text.get_rect(center=(WIDTH / 2 - 50, HEIGHT / 2))

        # Click menu
        if self.exit_button.update():
            self.game.game_state = 0

        # Click resume
        if self.resume_button.update():
            self.game.game_state = 1

        self.game.screen.fill((0, 191, 255))
        self.game.screen.blit(self.back_image, (0, 0))

        # Money update
        self.money.update()

        # Player health draw
        pygame.draw.rect(self.game.screen, (128, 128, 128), bg_rect)
        pygame.draw.rect(self.game.screen, color, current_rect)
        pygame.draw.rect(self.game.screen, BLACK, current_rect, 2)

        # Draw texts
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.game.screen.blit(self.health_text, self.health_text_rect)
        self.game.screen.blit(self.money_text, self.money_text_rect)
        self.game.screen.blit(self.time_text, self.time_text_rect)

        # Draw and update buttons
        self.resume_button.draw(self.game.screen)
        self.resume_button.update()
        self.exit_button.draw(self.game.screen)
        self.exit_button.update()

        pygame.display.update()


class StartMenu:
    def __init__(self, game):

        # Text font
        font = pygame.font.SysFont("Comic Sans", 100)
        self.font1 = pygame.font.SysFont("Comic Sans", 100)
        self.font2 = pygame.font.SysFont("Comic Sans", 20)

        # Buttons
        self.start_button = Button(447.5, 270.0, pygame.image.load('resources/button_start.png'), 0.5, 0, BLACK)
        self.music_button = Button(1200, 530, pygame.image.load('resources/button_music_on.png'), 1)
        self.settings_button = Button(1200, 590, pygame.image.load('resources/button_settings.png'), 1)
        self.exit_button = Button(1200, 650, pygame.image.load('resources/button_exit.png'), 1)

        # Texts
        self.game_title = font.render(f'DINO KNIGHT', True, (0, 0, 0))
        self.game_title_rect = self.game_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 200))
        self.rule_text = self.font2.render(
            f'Собери 15 монет за 75 секунд. Получай expe и нажимай ЛКМ для стрельбы', True, RED)
        self.rule_text_rect = self.rule_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))

        # Background
        self.back_image = pygame.image.load('resources/sprite_background.jpg').convert_alpha()
        self.back_image = pygame.transform.rotozoom(self.back_image, 0, 0.8)

        # Other
        self.game = game
        self.screen = self.game.screen

        # Game musics
        pygame.mixer.music.load('resources/music_menu_back.mp3')
        pygame.mixer.music.play(-1)
        self.play_music = True

    def update(self):

        # Click start
        if self.start_button.update():
            self.game.game_state = 1
            self.play_music = False

        # Click settings
        if self.settings_button.update():
            self.game.game_state = 2

        # Click exit
        if self.exit_button.update():
            pygame.quit()
            sys.exit()

        # Pause and unpause music
        if not self.play_music:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        # Click music
        if self.music_button.update():
            self.play_music = not self.play_music

        # Change music image
        if not self.play_music:
            self.music_button = Button(1200, 530, pygame.image.load('resources/button_music_off.png'), 1)
            self.music_button.update()
        else:
            self.music_button = Button(1200, 530, pygame.image.load('resources/button_music_on.png'), 1)
            self.music_button.update()

        self.game.screen.fill((0, 191, 255))
        self.game.screen.blit(self.back_image, (0, 0))

        # Draw texts
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.game.screen.blit(self.rule_text, self.rule_text_rect)

        # Draw and update buttons
        self.start_button.draw(self.game.screen)
        self.start_button.update()
        self.music_button.draw(self.game.screen)
        self.music_button.update()
        self.settings_button.draw(self.game.screen)
        self.settings_button.update()
        self.exit_button.draw(self.game.screen)
        self.exit_button.update()

        pygame.display.update()


class SettingsMenu:
    def __init__(self, game):
        # Text font
        font = pygame.font.SysFont("Comic Sans", 100)
        self.font1 = pygame.font.SysFont("Comic Sans", 50)

        # Buttons
        self.exit_button = Button(1200, 650, pygame.image.load('resources/button_exit.png'), 1)

        self.fps_plus_button_image = pygame.image.load('resources/button_resume.png')
        self.fps_plus_button = Button(WIDTH / 2 + 150, HEIGHT / 2 - 200, self.fps_plus_button_image, 1)

        self.fps_minus_button_image = pygame.transform.flip(self.fps_plus_button_image, True, False)
        self.fps_minus_button = Button(WIDTH / 2 - 200, HEIGHT / 2 - 200, self.fps_minus_button_image, 1)

        # Texts
        self.game_title = font.render(f'Settings', True, (0, 0, 0))
        self.game_title_rect = self.game_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 300))
        self.text_fps = None
        self.text_fps_rect = None

        # Background
        self.back_image = pygame.image.load('resources/sprite_background.jpg').convert_alpha()
        self.back_image = pygame.transform.rotozoom(self.back_image, 0, 0.8)

        # Other
        self.game = game
        self.screen = self.game.screen

        # Count fps
        self.count_fps = 30

    def update(self):

        # Click exit
        if self.exit_button.update():
            self.game.game_state = 0

        # Update text
        self.text_fps = self.font1.render(f'FPS: {self.count_fps}', True, (0, 0, 0))
        self.text_fps_rect = self.text_fps.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 180))

        self.game.screen.fill((0, 191, 255))
        self.game.screen.blit(self.back_image, (0, 0))

        # Draw texts
        self.game.screen.blit(self.game_title, self.game_title_rect)
        self.game.screen.blit(self.text_fps, self.text_fps_rect)

        # Draw and update buttons
        self.exit_button.draw(self.game.screen)
        self.exit_button.update()
        self.fps_plus_button.draw(self.game.screen)
        self.fps_plus_button.update()
        self.fps_minus_button.draw(self.game.screen)
        self.fps_minus_button.update()

        pygame.display.update()


class EndGameWindow:
    def __init__(self, game, text='YOU WIN', color=(255, 255, 0)):
        # Text font
        font = pygame.font.SysFont("Comic Sans", 200)
        self.font1 = pygame.font.SysFont("Comic Sans", 50)

        # Other
        self.game = game
        self.screen = self.game.screen

        # Buttons
        self.exit_button = Button(1200, 650, pygame.image.load('resources/button_exit.png'), 1)

        # Texts
        self.text = font.render(f'{text}', True, color)
        self.text_rect = self.text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 150))
        self.health_text = None
        self.health_text_rect = None
        self.money_text = None
        self.money_text_rect = None
        self.time_text = None
        self.time_text_rect = None

        # Background
        self.back_image = pygame.image.load('resources/sprite_background.jpg').convert_alpha()
        self.back_image = pygame.transform.rotozoom(self.back_image, 0, 0.8)

    def update(self):
        # Stop game
        self.game.level.player.kill()

        # Texts update
        self.health_text = self.font1.render(f'Health: {round(self.game.level.player.health)}', True, (255, 0, 0))
        self.health_text_rect = self.health_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.money_text = self.font1.render(f'Money: {self.game.level.player.money}', True, (255, 255, 0))
        self.money_text_rect = self.money_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60))
        self.time_text = self.font1.render(f'Time: {75 - round(self.game.level.player.timer)}', True, BLACK)
        self.time_text_rect = self.time_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 120))

        # Click exit
        if self.exit_button.update():
            self.game.game_state = 0

        self.game.screen.blit(self.back_image, (0, 0))

        # Draw and update buttons
        self.exit_button.draw(self.game.screen)
        self.exit_button.update()

        # Draw texts
        self.game.screen.blit(self.text, self.text_rect)
        self.game.screen.blit(self.health_text, self.health_text_rect)
        self.game.screen.blit(self.money_text, self.money_text_rect)
        self.game.screen.blit(self.time_text, self.time_text_rect)

        pygame.display.update()
