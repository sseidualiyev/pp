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
        self.spawn()

    def spawn(self):
        self.type = random.choice(["nitro", "shield", "repair"])
        self.rect = self.image.get_rect(center=(random.choice(LANES), random.randint(-800, -200)))
        self.base_speed = 2.0

    def update(self, global_speed):
        self.rect.y += self.base_speed * global_speed

        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- OBSTACLES ----------------
class Obstacle:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.lane = random.choice(LANES)
        self.rect = pygame.Rect(self.lane, random.randint(-800, -200), 50, 80)
        self.base_speed = random.uniform(3.0, 4.5)

    def update(self, global_speed):
        self.rect.y += self.base_speed * global_speed

        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- TRAFFIC ----------------
class TrafficCar:
    def __init__(self, image):
        self.image = image
        self.base_speed = random.uniform(2.5, 4.0)
        self.spawn()

    def spawn(self):
        self.lane = random.choice(LANES)
        self.rect = self.image.get_rect(center=(self.lane, random.randint(-800, -200)))

    def update(self, global_speed):
        self.rect.y += self.base_speed * global_speed

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

        self.base_speed = 0.1
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
            self.ENEMY_SPEED += 0.05
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

        global_speed = 1.2 + min(self.distance * 0.0002, 1.0)

        # traffic
        for t in self.traffic:
            t.update(global_speed)

            if self.player.colliderect(t.rect):
                if not self.shield:
                    return "game_over"
                self.shield = False

        # obstacles
        for o in self.obstacles:
            o.update(global_speed)

            if self.player.colliderect(o.rect):
                if not self.shield:
                    return "game_over"
                self.shield = False

        # powerups
        for p in self.powerups:
            p.update(global_speed)

            if self.player.colliderect(p.rect):
                self.apply_powerup(p.type)
                p.spawn()

        return "running"