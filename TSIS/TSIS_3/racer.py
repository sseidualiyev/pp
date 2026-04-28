import pygame
import random
import time

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

LANES = [120, 240, 360]


# ---------------- POWER UPS ----------------
class PowerUp:
    def __init__(self, image):
        self.image = image
        self.type = random.choice(["nitro", "shield", "repair"])
        self.spawn()

    def spawn(self):
        self.lane = random.choice(LANES)
        self.rect = self.image.get_rect(center=(self.lane, -100))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- OBSTACLES ----------------
class Obstacle:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.lane = random.choice(LANES)
        self.rect = pygame.Rect(self.lane, -100, 50, 80)
        self.speed = random.randint(6, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- TRAFFIC ----------------
class TrafficCar:
    def __init__(self, image):
        self.image = image
        self.spawn()

    def spawn(self):
        self.lane = random.choice(LANES)
        self.rect = self.image.get_rect(center=(self.lane, -200))
        self.speed = random.randint(7, 12)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- GAME CORE ----------------
class RacerGame:
    def __init__(self, assets):
        self.assets = assets

        self.player = assets["player"].get_rect(center=(240, 700))
        self.lane_index = 1

        self.coins = 0
        self.distance = 0
        self.score = 0

        self.ENEMY_SPEED = 6

        self.traffic = [TrafficCar(assets["enemy"]) for _ in range(2)]
        self.obstacles = [Obstacle() for _ in range(3)]
        self.powerups = [PowerUp(assets["coin"])]

        self.active_powerup = None
        self.powerup_end_time = 0

        self.shield = False

