import pygame
import sys
import json
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
DARK_GREY = (50, 50, 50)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X = WIDTH // 2 - BUTTON_WIDTH // 2

LEVEL_SPEEDS = {
    1: {"ball_x": 6, "ball_y": 6, "paddle_right": 4},
    2: {"ball_x": 8, "ball_y": 8, "paddle_right": 6},
    3: {"ball_x": 10, "ball_y": 10, "paddle_right": 8, "paddle_left": 15}
}
PADDLE_LEFT_SPEED_DEFAULT = 15

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

SAVE_FILE = "progress.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")
clock = pygame.time.Clock()

FONT_TITLE = pygame.font.Font(None, 100)
FONT_BIG = pygame.font.Font(None, 74)
FONT_SMALL = pygame.font.Font(None, 36)
FONT_SCORE = pygame.font.Font(None, 74)


def draw_text(text, font, color, surface, x, y, center=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y)) if center else text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(surface, color, x, y, width, height, text, font, text_color, is_enabled=True, shadow=True):
    button_rect = pygame.Rect(x, y, width, height)
    if shadow and is_enabled:
        shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
        pygame.draw.rect(surface, DARK_GREY, shadow_rect, border_radius=20)
    pygame.draw.rect(surface, color, button_rect, border_radius=20)
    draw_text(text, font, text_color, surface, x + width // 2, y + height // 2)
    return button_rect, is_enabled


def load_progress():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                return json.load(f).get("unlocked_level", 1)
    except Exception as e:
        print(f"Ошибка загрузки прогресса: {e}")
    return 1


def save_progress(unlocked_level):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump({"unlocked_level": unlocked_level}, f)
    except Exception as e:
        print(f"Ошибка сохранения прогресса: {e}")


def reset_progress():
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
    except Exception as e:
        print(f"Ошибка сброса прогресса: {e}")


def show_start_screen(unlocked_level):
    screen.fill(BLACK)
    draw_text("Пинг-Понг", FONT_TITLE, WHITE, screen, WIDTH // 2, 50)
    draw_text("Выберите уровень:", FONT_BIG, WHITE, screen, WIDTH // 2, 120)  # Подняли текст выше

    buttons = []

    buttons.append(draw_button(screen, GREEN, BUTTON_X, 200, BUTTON_WIDTH, BUTTON_HEIGHT, "1 уровень",
                               FONT_SMALL, BLACK, is_enabled=True))
    buttons.append(
        draw_button(screen, BLUE if unlocked_level >= 2 else GREY, BUTTON_X, 270, BUTTON_WIDTH, BUTTON_HEIGHT,
                    "2 уровень",
                    FONT_SMALL, WHITE if unlocked_level >= 2 else GREY, is_enabled=unlocked_level >= 2))
    buttons.append(draw_button(screen, RED if unlocked_level >= 3 else GREY, BUTTON_X, 340, BUTTON_WIDTH, BUTTON_HEIGHT,
                               "3 уровень",
                               FONT_SMALL, WHITE if unlocked_level >= 3 else GREY, is_enabled=unlocked_level >= 3))
    buttons.append(draw_button(screen, (200, 200, 200), BUTTON_X, 410, BUTTON_WIDTH, BUTTON_HEIGHT, "Выход",
                               FONT_SMALL, WHITE, is_enabled=True))

    pygame.display.flip()

    waiting = True
    selected_level = 0
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, (button_rect, is_enabled) in enumerate(buttons):
                    if button_rect.collidepoint(mouse_x, mouse_y) and is_enabled:
                        if i == 3:
                            return -1
                        selected_level = i + 1
                        waiting = False
    return selected_level


def show_round_screen(message):
    screen.fill(BLACK)
    draw_text(message, FONT_BIG, YELLOW, screen, WIDTH // 2, HEIGHT // 4)
    pygame.display.flip()
    pygame.time.delay(2000)


def show_end_screen(message, return_to_menu=False):
    screen.fill(BLACK)
    draw_text(message, FONT_BIG, WHITE, screen, WIDTH // 2, HEIGHT // 4)
    if return_to_menu:
        draw_text("Нажмите любую клавишу для возврата в меню", FONT_SMALL, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    else:
        draw_text("Нажмите любую клавишу для выхода", FONT_SMALL, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    return True


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, target_y):
        if self.rect.centery < target_y:
            self.rect.y += min(self.speed, target_y - self.rect.centery)
        elif self.rect.centery > target_y:
            self.rect.y -= min(self.speed, self.rect.centery - target_y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.score_left = 0
        self.score_right = 0

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1

    def check_score(self):
        if self.rect.left < 0:
            self.score_right += 1
            self.reset()
        elif self.rect.right > WIDTH:
            self.score_left += 1
            self.reset()

    def draw(self, screen):
        pygame.draw.ellipse(screen, GREEN, self.rect)

    def draw_score(self, screen):
        score_y_offset = 40
        draw_text(str(self.score_left), FONT_SCORE, GREEN, screen, WIDTH // 4, 20 + score_y_offset)
        draw_text(str(self.score_right), FONT_SCORE, GREEN, screen, 3 * WIDTH // 4, 20 + score_y_offset)


def run_game(current_level, unlocked_level):
    level_data = LEVEL_SPEEDS.get(current_level)
    if not level_data:
        return False, unlocked_level

    ball_speed_x = level_data["ball_x"]
    ball_speed_y = level_data["ball_y"]
    paddle_right_speed = level_data["paddle_right"]
    paddle_left_speed = level_data.get("paddle_left", PADDLE_LEFT_SPEED_DEFAULT)

    paddle1 = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, paddle_left_speed)
    paddle2 = Paddle(WIDTH - 65, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, paddle_right_speed)
    ball = Ball(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, ball_speed_x, ball_speed_y)

    game_running = True
    while game_running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, unlocked_level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, unlocked_level

        mouse_y = pygame.mouse.get_pos()[1]
        paddle1.move(mouse_y)
        paddle2.move(ball.rect.centery)

        ball.move()
        ball.bounce(paddle1, paddle2)
        ball.check_score()

        if ball.score_left > 7:
            if current_level < 3:
                unlocked_level = max(unlocked_level, current_level + 1)
                save_progress(unlocked_level)
                show_round_screen(f"Переход на {current_level + 1} уровень")
            else:
                show_end_screen("Победа на всех уровнях!", return_to_menu=True)
            game_running = False
        elif ball.score_right > 7:
            show_end_screen("Проигрыш", return_to_menu=True)
            game_running = False

        screen.fill(BLACK)
        paddle1.draw(screen)
        paddle2.draw(screen)
        ball.draw(screen)
        ball.draw_score(screen)

        draw_text("нажмите r для досрочного выхода", FONT_SMALL, WHITE, screen, WIDTH // 2, HEIGHT - 30)

        pygame.display.flip()

    return True, unlocked_level


def main():
    unlocked_level = load_progress()
    current_level = show_start_screen(unlocked_level)

    running = True
    while running:
        if current_level == -1:
            running = False
            continue
        elif current_level == 0:
            current_level = show_start_screen(unlocked_level)
            continue

        running, unlocked_level = run_game(current_level, unlocked_level)
        if running:
            current_level = show_start_screen(unlocked_level)

    reset_progress()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
