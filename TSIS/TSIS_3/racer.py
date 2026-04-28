import pygame
import random
import math
from ui import (
    W, H, ROAD_LEFT, ROAD_RIGHT, ROAD_W, NUM_LANES, LANE_W,
    lane_center, draw_road, draw_hud, CAR_COLORS,
    BLACK, WHITE, GRAY, RED, GREEN, BLUE, YELLOW, ORANGE, CYAN, PURPLE, DARK,
    TARMAC
)

# ── constants ─────────────────────────────────────────────────────────────────
PLAYER_Y     = H - 130
PLAYER_W, PLAYER_H = 32, 56
COIN_R       = 10
POWERUP_W, POWERUP_H = 28, 28
TRAFFIC_W, TRAFFIC_H = 34, 60
OBS_W, OBS_H = 36, 20
OIL_R        = 22
FINISH_DIST  = 3000     # metres to finish

COIN_WEIGHTS = [(1, 50), (5, 30), (10, 15), (25, 5)]   # (value, weight)

DIFFICULTY_PARAMS = {
    "easy":   {"base_speed": 4,  "traffic_interval": 140, "obs_interval": 180},
    "normal": {"base_speed": 5,  "traffic_interval": 100, "obs_interval": 130},
    "hard":   {"base_speed": 7,  "traffic_interval": 70,  "obs_interval": 90},
}

TRAFFIC_COLORS = [
    (180, 60, 60), (60, 100, 200), (200, 160, 40),
    (80, 180, 80), (180, 80, 200), (200, 120, 60),
]

# ── helpers ───────────────────────────────────────────────────────────────────

def weighted_coin():
    pool = []
    for val, w in COIN_WEIGHTS:
        pool.extend([val] * w)
    return random.choice(pool)


def coin_color(val):
    if val >= 25: return (255, 215, 0)
    if val >= 10: return (200, 200, 200)
    if val >= 5:  return (210, 150, 30)
    return YELLOW


def draw_car(surf, x, y, w, h, color, is_player=False):
    # body
    pygame.draw.rect(surf, color, (x - w//2, y - h//2, w, h), border_radius=6)
    # windshield
    wnd_col = (160, 220, 240) if is_player else (140, 190, 210)
    pygame.draw.rect(surf, wnd_col,
                     (x - w//2 + 4, y - h//2 + 6, w - 8, h//3 - 4), border_radius=3)
    # wheels
    wh_col = (30, 30, 30)
    for wx, wy in [(-w//2 - 3, -h//2 + 4), (w//2 - 1, -h//2 + 4),
                   (-w//2 - 3, h//2 - 14),  (w//2 - 1,  h//2 - 14)]:
        pygame.draw.rect(surf, wh_col, (x + wx, y + wy, 4, 10), border_radius=2)
    # headlights / taillights
    hl = GREEN if is_player else (240, 240, 60)
    tl = RED
    for lx in [x - w//2 + 3, x + w//2 - 7]:
        pygame.draw.rect(surf, hl, (lx, y - h//2 + 1, 4, 4), border_radius=1)
        pygame.draw.rect(surf, tl, (lx, y + h//2 - 5, 4, 4), border_radius=1)


# ── entity classes ─────────────────────────────────────────────────────────────

class Player:
    def __init__(self, lane, color):
        self.lane    = lane
        self.x       = lane_center(lane)
        self.y       = PLAYER_Y
        self.color   = CAR_COLORS.get(color, CAR_COLORS["red"])
        self.target_x = self.x
        self.speed   = 0          # visual forward speed (set by game)
        self.nitro   = False
        self.shield  = False

    def move(self, dx):
        new_lane = self.lane + dx
        if 0 <= new_lane < NUM_LANES:
            self.lane    = new_lane
            self.target_x = lane_center(new_lane)

    def update(self):
        self.x += (self.target_x - self.x) * 0.18

    def draw(self, surf):
        # shield glow
        if self.shield:
            glow = pygame.Surface((PLAYER_W + 20, PLAYER_H + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (40, 210, 210, 80),
                                (0, 0, PLAYER_W + 20, PLAYER_H + 20))
            surf.blit(glow, (self.x - PLAYER_W//2 - 10, self.y - PLAYER_H//2 - 10))
        draw_car(surf, int(self.x), int(self.y), PLAYER_W, PLAYER_H, self.color, True)

    def rect(self):
        return pygame.Rect(int(self.x) - PLAYER_W//2 + 4,
                           int(self.y) - PLAYER_H//2 + 4,
                           PLAYER_W - 8, PLAYER_H - 8)


class Coin:
    def __init__(self, lane, y=None):
        self.lane  = lane
        self.x     = lane_center(lane)
        self.y     = y if y is not None else -20
        self.value = weighted_coin()
        self.color = coin_color(self.value)
        self.alive = True

    def update(self, speed):
        self.y += speed
        if self.y > H + 30:
            self.alive = False

    def draw(self, surf, font):
        if not self.alive: return
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), COIN_R)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), COIN_R, 2)
        lbl = font.render(str(self.value), True, BLACK)
        surf.blit(lbl, lbl.get_rect(center=(int(self.x), int(self.y))))

    def rect(self):
        return pygame.Rect(int(self.x) - COIN_R, int(self.y) - COIN_R, COIN_R*2, COIN_R*2)


class PowerUp:
    ICONS  = {"nitro": "N", "shield": "S", "repair": "R"}
    COLORS = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}
    TIMEOUT = 8.0

    def __init__(self, kind, lane, y=None):
        self.kind  = kind
        self.lane  = lane
        self.x     = lane_center(lane)
        self.y     = y if y is not None else -30
        self.alive = True
        self.timer = self.TIMEOUT
        self.pulse = 0

    def update(self, speed, dt):
        self.y     += speed
        self.timer -= dt
        self.pulse  = (self.pulse + 5) % 360
        if self.y > H + 30 or self.timer <= 0:
            self.alive = False

    def draw(self, surf, font):
        if not self.alive: return
        col = self.COLORS[self.kind]
        alpha = int(180 + 70 * math.sin(math.radians(self.pulse)))
        glow = pygame.Surface((POWERUP_W + 16, POWERUP_H + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*col, alpha // 3),
                         (0, 0, POWERUP_W + 16, POWERUP_H + 16), border_radius=6)
        surf.blit(glow, (int(self.x) - POWERUP_W//2 - 8, int(self.y) - POWERUP_H//2 - 8))
        pygame.draw.rect(surf, col,
                         (int(self.x) - POWERUP_W//2, int(self.y) - POWERUP_H//2,
                          POWERUP_W, POWERUP_H), border_radius=5)
        lbl = font.render(self.ICONS[self.kind], True, BLACK)
        surf.blit(lbl, lbl.get_rect(center=(int(self.x), int(self.y))))

    def rect(self):
        return pygame.Rect(int(self.x) - POWERUP_W//2, int(self.y) - POWERUP_H//2,
                           POWERUP_W, POWERUP_H)


class TrafficCar:
    def __init__(self, lane, y=None):
        self.lane  = lane
        self.x     = lane_center(lane)
        self.y     = y if y is not None else -TRAFFIC_H
        self.color = random.choice(TRAFFIC_COLORS)
        self.alive = True
        self.speed_offset = random.uniform(-0.5, 0.5)

    def update(self, base_speed):
        self.y += base_speed + self.speed_offset
        if self.y > H + 60:
            self.alive = False

    def draw(self, surf):
        if not self.alive: return
        draw_car(surf, int(self.x), int(self.y), TRAFFIC_W, TRAFFIC_H, self.color)

    def rect(self):
        return pygame.Rect(int(self.x) - TRAFFIC_W//2 + 4,
                           int(self.y) - TRAFFIC_H//2 + 4,
                           TRAFFIC_W - 8, TRAFFIC_H - 8)


class Obstacle:
    """Barrier, oil spill, or pothole."""
    TYPES = ["barrier", "oil", "pothole"]

    def __init__(self, lane, y=None):
        self.lane  = lane
        self.x     = lane_center(lane)
        self.y     = y if y is not None else -30
        self.kind  = random.choice(self.TYPES)
        self.alive = True
        self.pulse = 0

    def update(self, speed):
        self.y    += speed
        self.pulse = (self.pulse + 3) % 360
        if self.y > H + 40:
            self.alive = False

    def draw(self, surf, font):
        if not self.alive: return
        ix, iy = int(self.x), int(self.y)
        if self.kind == "barrier":
            pygame.draw.rect(surf, ORANGE,
                             (ix - OBS_W//2, iy - OBS_H//2, OBS_W, OBS_H), border_radius=4)
            pygame.draw.rect(surf, WHITE,
                             (ix - OBS_W//2 + 4, iy - OBS_H//2 + 4, OBS_W - 8, OBS_H - 8), 2, border_radius=2)
        elif self.kind == "oil":
            alpha = int(160 + 60 * math.sin(math.radians(self.pulse)))
            oil = pygame.Surface((OIL_R*2, OIL_R), pygame.SRCALPHA)
            pygame.draw.ellipse(oil, (20, 20, 60, alpha), (0, 0, OIL_R*2, OIL_R))
            surf.blit(oil, (ix - OIL_R, iy - OIL_R//2))
        else:  # pothole
            pygame.draw.ellipse(surf, (25, 25, 25),
                                (ix - OBS_W//2, iy - OBS_H//2, OBS_W, OBS_H))
            pygame.draw.ellipse(surf, (50, 45, 40),
                                (ix - OBS_W//2 + 4, iy - OBS_H//2 + 3, OBS_W - 8, OBS_H - 6))

    def rect(self):
        if self.kind == "oil":
            return pygame.Rect(int(self.x) - OIL_R, int(self.y) - OIL_R//2, OIL_R*2, OIL_R)
        return pygame.Rect(int(self.x) - OBS_W//2, int(self.y) - OBS_H//2, OBS_W, OBS_H)


class NitroStrip:
    """Horizontal boost strip across the road."""
    def __init__(self, y=None):
        self.x     = ROAD_LEFT
        self.y     = y if y is not None else -20
        self.w     = ROAD_W
        self.h     = 12
        self.alive = True
        self.pulse = 0

    def update(self, speed):
        self.y    += speed
        self.pulse = (self.pulse + 4) % 360
        if self.y > H + 20:
            self.alive = False

    def draw(self, surf):
        if not self.alive: return
        alpha = int(120 + 80 * math.sin(math.radians(self.pulse)))
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        s.fill((255, 160, 0, alpha))
        surf.blit(s, (self.x, int(self.y)))

    def rect(self):
        return pygame.Rect(self.x, int(self.y), self.w, self.h)


# ── main Game class ──────────────────────────────────────────────────────────

class Game:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings
        diff = settings.get("difficulty", "normal")
        p = DIFFICULTY_PARAMS.get(diff, DIFFICULTY_PARAMS["normal"])
        self.base_speed       = p["base_speed"]
        self.traffic_interval = p["traffic_interval"]
        self.obs_interval     = p["obs_interval"]

        self.player = Player(1, settings.get("car_color", "red"))
        self.speed  = float(self.base_speed)
        self.scroll_y = 0

        self.coins     = []
        self.powerups  = []
        self.traffic   = []
        self.obstacles = []
        self.nitro_strips = []

        self.coin_count  = 0
        self.score       = 0
        self.distance    = 0.0
        self.finish_dist = FINISH_DIST

        # timers (in frames)
        self.coin_timer    = 0
        self.traffic_timer = 0
        self.obs_timer     = 0
        self.nitro_s_timer = 0
        self.pu_timer      = 0

        # active power-up state
        self.active_powerup  = None
        self.powerup_timer   = 0.0
        self.shield_active   = False

        self.key_cooldown = 0
        self.alive   = True
        self.finished = False
        self.font_sm  = pygame.font.SysFont("consolas", 14, bold=True)
        self.font_med = pygame.font.SysFont("consolas", 20, bold=True)

    # ── input ─────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player.move(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player.move(1)

    # ── update ────────────────────────────────────────────────────────────────
    def update(self, dt):
        if not self.alive or self.finished:
            return

        # speed / difficulty scaling
        prog = min(self.distance / self.finish_dist, 1.0)
        nitro_mult = 1.8 if (self.active_powerup == "nitro") else 1.0
        self.speed = (self.base_speed + prog * 4) * nitro_mult

        # scroll & distance
        self.scroll_y  = (self.scroll_y + self.speed) % 10000
        self.distance  += self.speed * 0.04       # ~metres per frame

        if self.distance >= self.finish_dist:
            self.finished = True
            self._calc_score()
            return

        self.score = int(self.coin_count * 10 + self.distance * 0.5)

        # power-up tick
        if self.active_powerup and self.active_powerup != "shield":
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                self._deactivate_powerup()

        # spawn
        self.coin_timer += 1
        if self.coin_timer >= 30:
            self.coin_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            self.coins.append(Coin(lane))

        self.traffic_timer += 1
        spawn_int = max(40, self.traffic_interval - int(prog * 60))
        if self.traffic_timer >= spawn_int:
            self.traffic_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            # safe spawn check
            safe = all(abs(t.x - lane_center(lane)) > TRAFFIC_W + 10
                       or t.y > 80
                       for t in self.traffic)
            if safe:
                self.traffic.append(TrafficCar(lane))

        self.obs_timer += 1
        obs_int = max(60, self.obs_interval - int(prog * 40))
        if self.obs_timer >= obs_int:
            self.obs_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            self.obstacles.append(Obstacle(lane))

        self.nitro_s_timer += 1
        if self.nitro_s_timer >= 300:
            self.nitro_s_timer = 0
            self.nitro_strips.append(NitroStrip())

        self.pu_timer += 1
        if self.pu_timer >= 200:
            self.pu_timer = 0
            if not self.powerups:
                kind = random.choice(["nitro", "shield", "repair"])
                lane = random.randint(0, NUM_LANES - 1)
                self.powerups.append(PowerUp(kind, lane))

        # update entities
        self.player.update()
        for c in self.coins:     c.update(self.speed)
        for p in self.powerups:  p.update(self.speed, dt)
        for t in self.traffic:   t.update(self.speed * 0.7)
        for o in self.obstacles: o.update(self.speed)
        for n in self.nitro_strips: n.update(self.speed)

        # collisions
        pr = self.player.rect()

        # coins
        for c in self.coins:
            if c.alive and pr.colliderect(c.rect()):
                c.alive = False
                self.coin_count += c.value

        # power-ups
        for p in self.powerups:
            if p.alive and pr.colliderect(p.rect()):
                p.alive = False
                self._activate_powerup(p.kind)

        # nitro strips (just trigger nitro briefly)
        for n in self.nitro_strips:
            if n.alive and pr.colliderect(n.rect()):
                n.alive = False
                self._activate_powerup("nitro")

        # traffic
        for t in self.traffic:
            if t.alive and pr.colliderect(t.rect()):
                self._take_hit()
                t.alive = False

        # obstacles
        for o in self.obstacles:
            if o.alive and pr.colliderect(o.rect()):
                if o.kind == "oil":
                    # oil: slow down briefly
                    self.speed *= 0.5
                else:
                    self._take_hit()
                o.alive = False

        # cull dead
        self.coins       = [c for c in self.coins       if c.alive]
        self.powerups    = [p for p in self.powerups    if p.alive]
        self.traffic     = [t for t in self.traffic     if t.alive]
        self.obstacles   = [o for o in self.obstacles   if o.alive]
        self.nitro_strips = [n for n in self.nitro_strips if n.alive]

    def _take_hit(self):
        if self.shield_active:
            self.shield_active = False
            self.player.shield = False
        else:
            self.alive = False
            self._calc_score()

    def _activate_powerup(self, kind):
        # only one active at a time (shield is separate flag)
        if kind == "shield":
            self.shield_active   = True
            self.player.shield   = True
        elif kind == "repair":
            # repair clears all obstacles from screen
            for o in self.obstacles: o.alive = False
        else:
            self.active_powerup  = kind
            self.powerup_timer   = 4.0 if kind == "nitro" else 999

    def _deactivate_powerup(self):
        self.active_powerup = None
        self.powerup_timer  = 0

    def _calc_score(self):
        self.score = int(self.coin_count * 10 + self.distance * 0.5)

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf):
        draw_road(surf, self.scroll_y)

        for n in self.nitro_strips: n.draw(surf)
        for o in self.obstacles:    o.draw(surf, self.font_sm)
        for c in self.coins:        c.draw(surf, self.font_sm)
        for p in self.powerups:     p.draw(surf, self.font_med)
        for t in self.traffic:      t.draw(surf)
        self.player.draw(surf)

        draw_hud(surf, self.font_sm, self.font_med,
                 self.score, self.distance, self.finish_dist,
                 self.coin_count, self.active_powerup, self.powerup_timer,
                 self.shield_active)