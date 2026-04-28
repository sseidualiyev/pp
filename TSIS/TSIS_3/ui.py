import pygame

# ── screen ─────────────────────────────
W, H = 480, 680

# ── road layout ────────────────────────
ROAD_LEFT  = 80
ROAD_RIGHT = 400
ROAD_W     = ROAD_RIGHT - ROAD_LEFT
NUM_LANES  = 3
LANE_W     = ROAD_W // NUM_LANES

def lane_center(lane):
    return ROAD_LEFT + LANE_W * lane + LANE_W // 2

# ── colors ─────────────────────────────
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (160, 160, 160)
RED   = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE  = (50, 120, 220)
ORANGE = (240, 140, 30)
CYAN   = (0, 200, 255)
YELLOW = (240, 210, 60)

TARMAC = (50, 50, 55)
GRASS  = (30, 110, 40)
LINE   = (220, 200, 80)

# ── drawing road ───────────────────────
def draw_road(screen, scroll):
    screen.fill(GRASS)

    pygame.draw.rect(screen, TARMAC, (ROAD_LEFT, 0, ROAD_W, H))

    # lane lines
    dash = 40
    gap = 25
    period = dash + gap

    for i in range(1, NUM_LANES):
        x = ROAD_LEFT + i * LANE_W
        y = -(scroll % period)
        while y < H:
            pygame.draw.rect(screen, LINE, (x - 2, y, 4, dash))
            y += period

# ── HUD ────────────────────────────────
def draw_hud(screen, font, score, coins, lives, power, timer, shield):
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, W, 60))

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Coins: {coins}", True, YELLOW), (150, 10))
    screen.blit(font.render(f"Lives: {lives}", True, RED), (300, 10))

    if power:
        screen.blit(font.render(f"{power.upper()} {timer:.1f}s", True, ORANGE), (10, 35))

    if shield:
        screen.blit(font.render("SHIELD ON", True, CYAN), (250, 35))