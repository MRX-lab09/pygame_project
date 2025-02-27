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
