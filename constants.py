import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
COLOR = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20
L_PADDLE_SPEED = 15
R_PADDLE_SPEED = 4
BALL_SPEED_X, BALL_SPEED_Y = 6, 6

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")
