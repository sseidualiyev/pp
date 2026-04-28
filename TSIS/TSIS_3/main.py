import pygame
import random

from racer import RacerGame
from ui import UI
from persistence import *

pygame.init()

screen = pygame.display.set_mode((480, 800))
font = pygame.font.SysFont("Verdana", 24)

# assets
assets = {
    "player": pygame.image.load("assets/Player.png").convert_alpha(),
    "enemy": pygame.image.load("assets/Enemy.png").convert_alpha(),
    "coin": pygame.image.load("assets/coin.png").convert_alpha()
}

