import pygame

# ── colours ──────────────────────────────────────────────────────────────────
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GRAY    = (160, 160, 160)
DARK    = (30, 30, 30)
RED     = (220, 50, 50)
GREEN   = (50, 200, 80)
BLUE    = (50, 120, 220)
YELLOW  = (240, 200, 40)
ORANGE  = (240, 130, 30)
CYAN    = (40, 210, 210)
PURPLE  = (160, 60, 220)
TARMAC  = (55, 55, 60)
LANE_LN = (200, 180, 40)
GRASS   = (34, 100, 34)
CURB_R  = (210, 40, 40)
CURB_W  = (240, 240, 240)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  100, 220),
    "green":  (50,  180, 60),
    "yellow": (230, 200, 30),
    "white":  (240, 240, 240),
}

W, H = 480, 680
ROAD_LEFT  = 80
ROAD_RIGHT = 400
ROAD_W     = ROAD_RIGHT - ROAD_LEFT
NUM_LANES  = 3
LANE_W     = ROAD_W // NUM_LANES


def lane_center(lane):          # lane 0,1,2
    return ROAD_LEFT + LANE_W * lane + LANE_W // 2


def draw_button(surf, text, rect, font, hover=False,
                color=DARK, hover_color=(60, 60, 70), text_color=WHITE):
    col = hover_color if hover else color
    pygame.draw.rect(surf, col, rect, border_radius=8)
    pygame.draw.rect(surf, GRAY, rect, 2, border_radius=8)
    lbl = font.render(text, True, text_color)
    surf.blit(lbl, lbl.get_rect(center=rect.center))


def draw_road(surf, scroll_y):
    # grass strips
    pygame.draw.rect(surf, GRASS, (0, 0, ROAD_LEFT, H))
    pygame.draw.rect(surf, GRASS, (ROAD_RIGHT, 0, W - ROAD_RIGHT, H))

    # tarmac
    pygame.draw.rect(surf, TARMAC, (ROAD_LEFT, 0, ROAD_W, H))

    # dashed lane lines
    dash_h, gap = 40, 30
    period = dash_h + gap
    for lane in range(1, NUM_LANES):
        x = ROAD_LEFT + LANE_W * lane
        start = -(scroll_y % period)
        y = start
        while y < H:
            pygame.draw.rect(surf, LANE_LN, (x - 2, int(y), 4, dash_h))
            y += period

    # curb stripes
    stripe = 30
    for i in range(H // stripe + 2):
        sy = i * stripe - (scroll_y % stripe)
        col = CURB_R if i % 2 == 0 else CURB_W
        pygame.draw.rect(surf, col, (ROAD_LEFT - 8, int(sy), 8, stripe))
        pygame.draw.rect(surf, col, (ROAD_RIGHT, int(sy), 8, stripe))


def draw_hud(surf, font_sm, font_med, score, distance, finish_dist,
             coins, active_powerup, powerup_timer, shield_active):
    # top bar
    pygame.draw.rect(surf, (20, 20, 25), (0, 0, W, 44))
    surf.blit(font_sm.render(f"Score: {score}", True, WHITE), (8, 6))
    dist_pct = min(distance / finish_dist, 1.0)
    bar_w = 160
    bar_x = W // 2 - bar_w // 2
    pygame.draw.rect(surf, GRAY, (bar_x, 10, bar_w, 14), border_radius=4)
    pygame.draw.rect(surf, GREEN, (bar_x, 10, int(bar_w * dist_pct), 14), border_radius=4)
    surf.blit(font_sm.render(f"{int(distance)}m", True, WHITE), (bar_x + bar_w + 4, 6))
    surf.blit(font_sm.render(f"Coins:{coins}", True, YELLOW), (W - 100, 6))

    # power-up bar
    if active_powerup:
        names = {"nitro": ("NITRO", ORANGE), "shield": ("SHIELD", CYAN), "repair": ("REPAIR", GREEN)}
        label, col = names.get(active_powerup, (active_powerup.upper(), WHITE))
        pu_surf = font_sm.render(f"[{label}] {powerup_timer:.1f}s", True, col)
        surf.blit(pu_surf, (8, H - 28))
    if shield_active:
        s = font_sm.render("🛡 SHIELD", True, CYAN)
        surf.blit(s, (8, H - 50 if active_powerup else H - 28))