import pygame
import random
from ui import lane_center, draw_road, draw_hud, W, H, ORANGE, CYAN, GREEN

ASSETS = "assets"


def load_img(name, size):
    img = pygame.image.load(f"{ASSETS}/{name}").convert_alpha()
    return pygame.transform.scale(img, size)


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.player_name = "Player"
        self.music_path = f"{ASSETS}/bg_music.mp3"

        # assets
        self.player_img = load_img("player.png", (50, 80))
        self.enemy_img  = load_img("enemy.png", (50, 80))
        self.coin_img   = load_img("coin.png", (30, 30))

        # sound
        self.crash = pygame.mixer.Sound(f"{ASSETS}/crash.wav")

        if self.settings["sound"]:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)

        self.reset()

    # ─────────────────────────────
    def reset(self):
        self.lane = 1

        diff = self.settings["difficulty"]
        self.base_speed = {"easy": 4, "normal": 6, "hard": 8}[diff]
        self.speed = self.base_speed

        self.scroll = 0
        self.distance = 0
        self.score = 0
        self.coins = 0

        self.lives = 2
        self.alive = True

        self.enemies = []
        self.coins_list = []
        self.powerups = []

        self.power = None
        self.power_timer = 0

        self.shield = False

    # ─────────────────────────────
    def update_sound(self):
        if self.settings["sound"]:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    # ─────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane - 1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane + 1)

    # ─────────────────────────────
    def spawn(self):
        if random.random() < 0.02:
            self.enemies.append({"lane": random.randint(0, 2), "y": -80})

        if random.random() < 0.03:
            self.coins_list.append({"lane": random.randint(0, 2), "y": -50})

        if random.random() < 0.004:
            self.powerups.append({
                "lane": random.randint(0, 2),
                "y": -60,
                "type": random.choice(["nitro", "shield", "repair"])
            })

    # ─────────────────────────────
    def activate(self, typ):
        self.power = typ
        self.power_timer = 5

        if typ == "nitro":
            self.speed = self.base_speed * 1.8

        elif typ == "shield":
            self.shield = True

        elif typ == "repair":
            self.lives = min(2, self.lives + 1)

    # ─────────────────────────────
    def update(self, dt):
        if not self.alive:
            return

        self.spawn()

        self.scroll += self.speed
        self.distance += self.speed
        self.score = int(self.distance // 10)

        player = pygame.Rect(lane_center(self.lane), 600, 50, 80)

        # ── enemies ──
        for e in self.enemies[:]:
            e["y"] += self.speed
            rect = pygame.Rect(lane_center(e["lane"]), e["y"], 50, 80)

            if rect.colliderect(player):
                if self.shield:
                    self.shield = False
                else:
                    self.lives -= 1
                    if self.settings["sound"]:
                        self.crash.play()

                    if self.lives <= 0:
                        self.alive = False

                self.enemies.remove(e)

            elif e["y"] > H:
                self.enemies.remove(e)

        # ── coins ──
        for c in self.coins_list[:]:
            c["y"] += self.speed
            rect = pygame.Rect(lane_center(c["lane"]), c["y"], 30, 30)

            if rect.colliderect(player):
                self.coins += 1
                self.coins_list.remove(c)

            elif c["y"] > H:
                self.coins_list.remove(c)

        # ── powerups (ONLY ONE ACTIVE) ──
        for p in self.powerups[:]:
            p["y"] += self.speed
            rect = pygame.Rect(lane_center(p["lane"]), p["y"], 30, 30)

            if rect.colliderect(player):
                self.activate(p["type"])
                self.powerups.remove(p)

            elif p["y"] > H:
                self.powerups.remove(p)

        # ── power timer ──
        if self.power:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power = None
                self.speed = self.base_speed

    # ─────────────────────────────
    def draw(self, screen):
        draw_road(screen, self.scroll)

        screen.blit(self.player_img, (lane_center(self.lane), 600))

        for e in self.enemies:
            screen.blit(self.enemy_img, (lane_center(e["lane"]), e["y"]))

        for c in self.coins_list:
            screen.blit(self.coin_img, (lane_center(c["lane"]), c["y"]))

        for p in self.powerups:
            color = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}[p["type"]]
            pygame.draw.circle(screen, color,
                               (lane_center(p["lane"]) + 20, int(p["y"]) + 20), 15)

        draw_hud(screen,
                 pygame.font.SysFont(None, 28),
                 self.score,
                 self.coins,
                 self.lives,
                 self.power,
                 self.power_timer,
                 self.shield)