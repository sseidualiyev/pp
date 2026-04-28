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

        self.base_speed = 4
        self.ENEMY_SPEED = self.base_speed

        self.traffic = [TrafficCar(assets["enemy"]) for _ in range(2)]
        self.obstacles = [Obstacle() for _ in range(3)]
        self.powerups = [PowerUp(assets["coin"])]

        self.active_powerup = None
        self.powerup_end_time = 0

        self.shield = False

    # ---------------- PLAYER ----------------
    def move_player(self, direction):
        if direction == "left" and self.lane_index > 0:
            self.lane_index -= 1
        if direction == "right" and self.lane_index < 2:
            self.lane_index += 1

        self.player.centerx = LANES[self.lane_index]

    # ---------------- POWERUPS ----------------
    def apply_powerup(self, ptype):
        if ptype == "nitro":
            self.ENEMY_SPEED += 4
            self.active_powerup = "NITRO"
            self.powerup_end_time = time.time() + 4

        elif ptype == "shield":
            self.shield = True
            self.active_powerup = "SHIELD"

        elif ptype == "repair":
            self.coins += 5

    # ---------------- UPDATE ----------------
    def update(self):
        self.distance += 1

        # traffic
        for t in self.traffic:
            t.update()
            if self.player.colliderect(t.rect):
                if self.shield:
                    self.shield = False
                else:
                    return "game_over"

        # obstacles
        for o in self.obstacles:
            o.update()
            if self.player.colliderect(o.rect):
                if self.shield:
                    self.shield = False
                else:
                    return "game_over"

        # powerups
        for p in self.powerups:
            p.update()
            if self.player.colliderect(p.rect):
                self.apply_powerup(p.type)
                p.spawn()

        # powerup timer
        if self.active_powerup == "NITRO":
            if time.time() > self.powerup_end_time:
                self.ENEMY_SPEED = max(6, self.ENEMY_SPEED - 4)
                self.active_powerup = None

        # difficulty scaling
        self.ENEMY_SPEED = 6 + self.coins // 15

        return "running"