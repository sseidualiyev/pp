import pygame

# ── COLORS ─────────────────────────────────────────
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY  = (160,160,160)

GREEN  = (50,200,80)
RED    = (220,50,50)
YELLOW = (240,200,40)

ROAD = (55,55,60)
LANE = (200,180,40)

# ── SCREEN ─────────────────────────────────────────
W, H = 480, 800
LANES = [120, 240, 360]


# ── ROAD ───────────────────────────────────────────
def draw_road(screen, scroll):
    screen.fill((30,30,30))

    # road
    pygame.draw.rect(screen, ROAD, (80, 0, 320, H))

    # lane lines
    for x in [200, 320]:
        for y in range(-40, H, 80):
            pygame.draw.rect(screen, LANE, (x, y + scroll % 80, 4, 40))


# ── HUD ────────────────────────────────────────────
def draw_hud(screen, score, coins, powerup, timer):
    font = pygame.font.SysFont(None, 28)

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
    screen.blit(font.render(f"Coins: {coins}", True, YELLOW), (10,40))

    if powerup:
        screen.blit(
            font.render(f"{powerup.upper()} {timer:.1f}s", True, WHITE),
            (10, 70)
        )