import pygame
import random

from racer import RacerGame
from ui import UI
from persistence import *

pygame.init()

screen = pygame.display.set_mode((480, 800))
font = pygame.font.SysFont("Verdana", 24)

