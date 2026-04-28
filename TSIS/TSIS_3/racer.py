import pygame
import random
from ui import *

PLAYER_Y = H - 120


# ─────────────────────────────────────────────
# MAIN GAME CLASS
# ─────────────────────────────────────────────
class Game:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        # difficulty tuning
        diff = settings.get("difficulty", "normal")
        self.difficulty_map = {
            "easy":   {"speed": 4, "enemy_rate": 90},
            "normal": {"speed": 6, "enemy_rate": 70},
            "hard":   {"speed": 8, "enemy_rate": 50},
        }
        cfg = self.difficulty_map.get(diff, self.difficulty_map["normal"])

        self.base_speed = cfg["speed"]
        self.enemy_rate = cfg["enemy_rate"]

        # player state
        self.lane = 1
        self.lives = 2

        # game stats
        self.score = 0
        self.distance = 0
        self.coins = 0

        # world speed
        self.speed = self.base_speed

        # entities
        self.enemies = []
        self.coins_list = []
        self.powerups = []

        # power-up system (ONLY ONE ACTIVE)
        self.active_powerup = None
        self.power_timer = 0.0

        # shield is separate safety state
        self.shield = False

        # timers
        self.enemy_timer = 0
        self.coin_timer = 0
        self.power_timer_spawn = 0

        # state
        self.alive = True
        self.finished = False

        self.font_sm = pygame.font.SysFont("consolas", 16, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 20, bold=True)

    # ─────────────────────────────────────────────
    # INPUT
    # ─────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane - 1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane + 1)

    # ─────────────────────────────────────────────
    # SPAWNING (CONTROLLED = NO SPAWN CHAOS)
    # ─────────────────────────────────────────────
    def spawn_enemy(self):
        if len(self.enemies) < 2:  # LIMIT = fair gameplay
            self.enemies.append({"lane": random.randint(0, 2), "y": -100})

    def spawn_coin(self):
        if random.random() < 0.35:
            self.coins_list.append({"lane": random.randint(0, 2), "y": -50})

    def spawn_powerup(self):
        if random.random() < 0.008 and not self.active_powerup:
            self.powerups.append({
                "lane": random.randint(0, 2),
                "y": -50,
                "type": random.choice(["nitro", "shield", "repair"])
            })

    # ─────────────────────────────────────────────
    # POWERUP SYSTEM (ONLY ONE ACTIVE)
    # ─────────────────────────────────────────────
    def activate_powerup(self, ptype):
        self.active_powerup = ptype
        self.power_timer = 5.0

        if ptype == "shield":
            self.shield = True

        elif ptype == "repair":
            self.lives = min(2, self.lives + 1)

        elif ptype == "nitro":
            self.speed = self.base_speed * 1.8

    def update_powerup(self, dt):
        if self.active_powerup:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.active_powerup = None
                self.shield = False
                self.speed = self.base_speed

    # ─────────────────────────────────────────────
    # GAME UPDATE
    # ─────────────────────────────────────────────
    def update(self, dt):
        if not self.alive:
            return

        # speed scaling
        self.speed = self.base_speed

        self.distance += self.speed
        self.score = int(self.distance * 0.5 + self.coins * 10)

        # spawn logic
        self.enemy_timer += 1
        if self.enemy_timer >= self.enemy_rate:
            self.enemy_timer = 0
            self.spawn_enemy()

        self.coin_timer += 1
        if self.coin_timer >= 40:
            self.coin_timer = 0
            self.spawn_coin()

        self.power_timer_spawn += 1
        if self.power_timer_spawn >= 250:
            self.power_timer_spawn = 0
            self.spawn_powerup()

        # update powerup timer
        self.update_powerup(dt)

        player_rect = pygame.Rect(lane_center(self.lane) - 18, PLAYER_Y - 30, 36, 60)

        # ── ENEMIES ─────────────────────────────
        for e in self.enemies[:]:
            e["y"] += self.speed

            rect = pygame.Rect(lane_center(e["lane"]) - 18, e["y"], 36, 60)

            if rect.colliderect(player_rect):
                if self.shield:
                    self.shield = False
                else:
                    self.lives -= 1

                    if self.lives <= 0:
                        self.alive = False

                self.enemies.remove(e)

            elif e["y"] > H:
                self.enemies.remove(e)

        # ── COINS ───────────────────────────────
        for c in self.coins_list[:]:
            c["y"] += self.speed

            rect = pygame.Rect(lane_center(c["lane"]) - 10, c["y"], 20, 20)

            if rect.colliderect(player_rect):
                self.coins += 1
                self.coins_list.remove(c)

            elif c["y"] > H:
                self.coins_list.remove(c)

        # ── POWERUPS ────────────────────────────
        for p in self.powerups[:]:
            p["y"] += self.speed

            rect = pygame.Rect(lane_center(p["lane"]) - 14, p["y"], 28, 28)

            if rect.colliderect(player_rect):
                if not self.active_powerup:
                    self.activate_powerup(p["type"])

                self.powerups.remove(p)

            elif p["y"] > H:
                self.powerups.remove(p)

    # ─────────────────────────────────────────────
    # DRAW
    # ─────────────────────────────────────────────
    def draw(self, surf):
        draw_road(surf, self.distance)

        # draw player
        pygame.draw.rect(
            surf,
            BLUE if self.shield else RED,
            (lane_center(self.lane) - 18, PLAYER_Y - 30, 36, 60),
            border_radius=6
        )

        # enemies
        for e in self.enemies:
            pygame.draw.rect(
                surf, DARK,
                (lane_center(e["lane"]) - 18, e["y"], 36, 60)
            )

        # coins
        for c in self.coins_list:
            pygame.draw.circle(
                surf, YELLOW,
                (lane_center(c["lane"]), int(c["y"])), 10
            )

        # powerups
        colors = {
            "nitro": ORANGE,
            "shield": CYAN,
            "repair": GREEN
        }

        for p in self.powerups:
            pygame.draw.rect(
                surf,
                colors[p["type"]],
                (lane_center(p["lane"]) - 12, p["y"], 24, 24)
            )

        # HUD (UPDATED with LIVES)
        self.draw_hud(surf)

    # ─────────────────────────────────────────────
    # HUD (score + distance + power + lives)
    # ─────────────────────────────────────────────
    def draw_hud(self, surf):
        pygame.draw.rect(surf, (20, 20, 20), (0, 0, W, 60))

        surf.blit(self.font_sm.render(f"Score: {self.score}", True, WHITE), (10, 5))
        surf.blit(self.font_sm.render(f"Dist: {int(self.distance)}", True, WHITE), (10, 25))

        surf.blit(self.font_sm.render(f"Coins: {self.coins}", True, YELLOW), (150, 5))

        # lives (IMPORTANT PART YOU ASKED)
        surf.blit(self.font_sm.render(f"Lives: {self.lives}", True, GREEN), (150, 25))

        # power-up
        if self.active_powerup:
            txt = f"{self.active_powerup.upper()} {self.power_timer:.1f}s"
            surf.blit(self.font_sm.render(txt, True, CYAN), (300, 5))