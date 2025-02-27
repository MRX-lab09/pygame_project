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
