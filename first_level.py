import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20
L_PADDLE_SPEED = 20
R_PADDLE_SPEED = 4
BALL_SPEED_X, BALL_SPEED_Y = 6, 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")


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
        pygame.draw.rect(screen, WHITE, self.rect)


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
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def draw_score(self, screen):
        font = pygame.font.Font(None, 74)
        left_score = font.render(str(self.score_left), True, WHITE)
        right_score = font.render(str(self.score_right), True, WHITE)
        screen.blit(left_score, (WIDTH // 4, 20))
        screen.blit(right_score, (3 * WIDTH // 4, 20))


paddle1 = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, L_PADDLE_SPEED)
paddle2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT,
                 R_PADDLE_SPEED)
ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_y = pygame.mouse.get_pos()[1]
    paddle1.move(mouse_y)
    paddle2.move(ball.rect.centery)

    ball.move()
    ball.bounce(paddle1, paddle2)
    ball.check_score()

    screen.fill(BLACK)
    paddle1.draw(screen)
    paddle2.draw(screen)
    ball.draw(screen)
    ball.draw_score(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
