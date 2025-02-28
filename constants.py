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
