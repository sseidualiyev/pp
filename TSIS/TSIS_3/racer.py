import pygame
import os
import random

from ui import (
    W, H, ROAD_LEFT, ROAD_RIGHT, ROAD_W, NUM_LANES,
    lane_center, draw_road, draw_hud,
    BLACK, WHITE, YELLOW, ORANGE, CYAN, GREEN
)

ASSETS = "assets"


def load_img(name, size):
    img = pygame.image.load(os.path.join(ASSETS, name)).convert_alpha()
    return pygame.transform.scale(img, size)


# ─────────────────────────────────────────────
# GAME CLASS
# ─────────────────────────────────────────────
class Game:
    def __init__(self, settings):
        self.settings = settings

        # sprites
        self.player_img = load_img("player.png", (50, 80))
        self.enemy_img  = load_img("enemy.png", (50, 80))
        self.coin_img   = load_img("coin.png", (30, 30))

        # sounds
        self.music_path = os.path.join(ASSETS, "bg_music.mp3")
        self.crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))

        if settings["sound"]:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)

        self.reset()

    # ─────────────────────────────────────────────
    def reset(self):
        self.lane = 1

        base = {
            "easy": 180,
            "normal": 240,
            "hard": 320
        }
        self.base_speed = base[self.settings["difficulty"]]
        self.speed = self.base_speed

        self.scroll = 0
        self.distance = 0
        self.score = 0
        self.coins = 0

        self.lives = 2  # ✅ 2 crash system

        self.enemies = []
        self.coin_list = []
        self.powerups = []

        self.powerup = None
        self.power_timer = 0
        self.shield = 0  # shield absorbs 2 hits total

        self.alive = True

        # spawn control (reduces overcrowding)
        self.enemy_timer = 0
        self.coin_timer = 0
        self.power_timer_spawn = 0

    # ─────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane - 1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane + 1)

    # ─────────────────────────────────────────────
    def spawn_enemy(self):
        self.enemies.append({
            "lane": random.randint(0, 2),
            "y": -100
        })

    def spawn_coin(self):
        self.coin_list.append({
            "lane": random.randint(0, 2),
            "y": -50
        })

    def spawn_powerup(self):
        self.powerups.append({
            "lane": random.randint(0, 2),
            "y": -60,
            "type": random.choice(["nitro", "shield", "repair"])
        })

    # ─────────────────────────────────────────────
    def activate(self, typ):
        self.powerup = typ
        self.power_timer = 5

        if typ == "nitro":
            self.speed = self.base_speed * 1.8

        elif typ == "shield":
            self.shield = 2  # 2 hits protection

        elif typ == "repair":
            self.lives = min(2, self.lives + 1)

    # ─────────────────────────────────────────────
    def update(self, dt):
        if not self.alive:
            return

        self.scroll += self.speed * dt
        self.distance += self.speed * dt
        self.score = int(self.distance / 10)

        player = pygame.Rect(lane_center(self.lane) - 25, 700, 50, 80)

        # ───── spawning (LESS OVERCROWDING FIX) ─────
        self.enemy_timer += 1
        self.coin_timer += 1
        self.power_timer_spawn += 1

        if self.enemy_timer > 80:
            self.enemy_timer = 0
            if len(self.enemies) < 2:  # limit enemies
                self.spawn_enemy()

        if self.coin_timer > 50:
            self.coin_timer = 0
            self.spawn_coin()

        if self.power_timer_spawn > 300:
            self.power_timer_spawn = 0
            self.spawn_powerup()

        # ───── update enemies ─────
        for e in self.enemies[:]:
            e["y"] += self.speed * dt
            rect = pygame.Rect(lane_center(e["lane"]) - 25, e["y"], 50, 80)

            if rect.colliderect(player):
                if self.shield > 0:
                    self.shield -= 1
                    self.enemies.remove(e)
                else:
                    self.lives -= 1
                    self.crash_sound.play()

                    self.enemies.remove(e)

                    if self.lives <= 0:
                        self.alive = False

            elif e["y"] > H:
                self.enemies.remove(e)

        # ───── coins ─────
        for c in self.coin_list[:]:
            c["y"] += self.speed * dt
            rect = pygame.Rect(lane_center(c["lane"]) - 15, c["y"], 30, 30)

            if rect.colliderect(player):
                self.coins += 1
                self.coin_list.remove(c)

            elif c["y"] > H:
                self.coin_list.remove(c)

        # ───── powerups ─────
        for p in self.powerups[:]:
            p["y"] += self.speed * dt
            rect = pygame.Rect(lane_center(p["lane"]) - 20, p["y"], 40, 40)

            if rect.colliderect(player):
                self.activate(p["type"])
                self.powerups.remove(p)

            elif p["y"] > H:
                self.powerups.remove(p)

        # ───── power timer ─────
        if self.power_timer > 0:
            self.power_timer -= dt
        else:
            self.powerup = None
            self.speed = self.base_speed

    # ─────────────────────────────────────────────
    def draw(self, screen):
        draw_road(screen, self.scroll)

        # player
        screen.blit(self.player_img, (lane_center(self.lane) - 25, 700))

        # enemies
        for e in self.enemies:
            screen.blit(self.enemy_img, (lane_center(e["lane"]) - 25, e["y"]))

        # coins
        for c in self.coin_list:
            screen.blit(self.coin_img, (lane_center(c["lane"]) - 15, c["y"]))

        # powerups
        colors = {
            "nitro": ORANGE,
            "shield": CYAN,
            "repair": GREEN
        }

        for p in self.powerups:
            pygame.draw.circle(
                screen,
                colors[p["type"]],
                (lane_center(p["lane"]), int(p["y"])),
                12
            )

        draw_hud(
            screen,
            self.score,
            self.distance,
            self.coins,
            self.powerup,
            self.power_timer,
            self.lives
        )