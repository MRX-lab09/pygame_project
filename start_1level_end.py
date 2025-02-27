import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X = WIDTH // 2 - BUTTON_WIDTH // 2

BALL_SPEED_X = 6
BALL_SPEED_Y = 6
PADDLE_LEFT_SPEED = 15
PADDLE_RIGHT_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")
clock = pygame.time.Clock()


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(surface, color, x, y, width, height, text, font, text_color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect, border_radius=20)
    draw_text(text, font, text_color, surface, x + width // 2, y + height // 2)
    return button_rect


def show_start_screen():
    screen.fill(BLACK)
    font_title = pygame.font.Font(None, 100)
    font_big = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    draw_text("Пинг-Понг", font_title, WHITE, screen, WIDTH // 2, 50)
    draw_text("Выберите уровень:", font_big, WHITE, screen, WIDTH // 2, 150)

    button1 = draw_button(screen, GREEN, BUTTON_X, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "1 уровень",
                          font_small, BLACK)
    button2 = draw_button(screen, BLUE, BUTTON_X, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "2 уровень",
                          font_small, WHITE)
    button3 = draw_button(screen, RED, BUTTON_X, 450, BUTTON_WIDTH, BUTTON_HEIGHT, "3 уровень",
                          font_small, WHITE)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button1.collidepoint(mouse_x, mouse_y):
                    waiting = False


def show_end_screen(message):
    screen.fill(BLACK)
    draw_text(message, pygame.font.Font(None, 74), WHITE, screen, WIDTH // 2, HEIGHT // 4)
    draw_text("Нажмите любую клавишу для выхода", pygame.font.Font(None, 36), WHITE, screen, WIDTH // 2,
              HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, target_y):
        if self.rect.centery < target_y:
            self.rect.y += min(self.speed, target_y - self.rect.centery)
        elif self.rect.centery > target_y:
            self.rect.y -= min(self.speed, self.rect.centery - target_y)
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

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
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
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
        font = pygame.font.Font(None, 74)
        left_score = font.render(str(self.score_left), True, GREEN)
        right_score = font.render(str(self.score_right), True, GREEN)
        screen.blit(left_score, (WIDTH // 4, 20))
        screen.blit(right_score, (3 * WIDTH // 4, 20))


paddle1 = Paddle(50, HEIGHT // 2 - 50, 15, 100, PADDLE_LEFT_SPEED)
paddle2 = Paddle(WIDTH - 65, HEIGHT // 2 - 50, 15, 100, PADDLE_RIGHT_SPEED)
ball = Ball(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, BALL_SPEED_X, BALL_SPEED_Y)

show_start_screen()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_y = pygame.mouse.get_pos()[1]
    paddle1.move(mouse_y)
    paddle2.move(ball.rect.centery)

    ball.move()
    ball.bounce(paddle1, paddle2)
    ball.check_score()

    if ball.score_right >= 10:
        show_end_screen("Победа!")
        running = False
    elif ball.score_left >= 10:
        show_end_screen("Проигрыш!")
        running = False

    screen.fill(BLACK)
    paddle1.draw(screen)
    paddle2.draw(screen)
    ball.draw(screen)
    ball.draw_score(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
