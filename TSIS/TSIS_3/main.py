import pygame
import sys
from racer import Game
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import (W, H, BLACK, WHITE, GRAY, DARK, RED, GREEN, BLUE,
                YELLOW, ORANGE, CYAN, PURPLE, CAR_COLORS, draw_button)

FPS = 60

# ── colours ───────────────────────────────────────────────────────────────────
BG       = (15, 15, 20)
ACCENT   = (240, 130, 30)
TITLE_C  = (240, 200, 50)

# ── screen helpers ────────────────────────────────────────────────────────────

def screen_title(surf, font_big, font_med, text, subtitle=""):
    title = font_big.render(text, True, TITLE_C)
    surf.blit(title, title.get_rect(centerx=W//2, y=40))
    if subtitle:
        s = font_med.render(subtitle, True, GRAY)
        surf.blit(s, s.get_rect(centerx=W//2, y=90))


def get_mouse_hover(rects):
    mx, my = pygame.mouse.get_pos()
    return [r.collidepoint(mx, my) for r in rects]


# ── screens ───────────────────────────────────────────────────────────────────

def run_main_menu(surf, clock, fonts):
    font_big, font_med, font_sm = fonts
    btns = [pygame.Rect(W//2 - 100, 180 + i*70, 200, 48) for i in range(4)]
    labels = ["▶  Play", "🏆  Leaderboard", "⚙  Settings", "✕  Quit"]

    while True:
        dt = clock.tick(FPS) / 1000
        surf.fill(BG)

        # decorative road strip
        pygame.draw.rect(surf, (40, 40, 45), (W//2 - 60, 0, 120, H))
        for i in range(10):
            y = (i * 80 + pygame.time.get_ticks() // 20) % H
            pygame.draw.rect(surf, (200, 180, 40, 100), (W//2 - 4, y, 8, 40))

        screen_title(surf, font_big, font_med, "RACER", "TSIS 3 Edition")

        hovers = get_mouse_hover(btns)
        for i, (btn, lbl) in enumerate(zip(btns, labels)):
            draw_button(surf, lbl, btn, font_med, hovers[i],
                        color=(30, 30, 35), hover_color=(60, 50, 20))

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                for i, btn in enumerate(btns):
                    if btn.collidepoint(mx, my):
                        return ["play", "leaderboard", "settings", "quit"][i]


def run_username_screen(surf, clock, fonts):
    font_big, font_med, font_sm = fonts
    name = ""
    cursor_timer = 0
    btn = pygame.Rect(W//2 - 80, 360, 160, 44)
    input_rect = pygame.Rect(W//2 - 120, 280, 240, 44)
    error = ""

    while True:
        clock.tick(FPS)
        cursor_timer = (cursor_timer + 1) % 60
        surf.fill(BG)
        screen_title(surf, font_big, font_med, "ENTER NAME", "")
        prompt = font_med.render("Your name:", True, WHITE)
        surf.blit(prompt, prompt.get_rect(centerx=W//2, y=240))

        pygame.draw.rect(surf, (40, 40, 50), input_rect, border_radius=6)
        pygame.draw.rect(surf, ACCENT, input_rect, 2, border_radius=6)
        display = name + ("|" if cursor_timer < 30 else "")
        txt = font_med.render(display, True, WHITE)
        surf.blit(txt, txt.get_rect(centerx=W//2, centery=302))

        if error:
            e = font_sm.render(error, True, RED)
            surf.blit(e, e.get_rect(centerx=W//2, y=335))

        hover = btn.collidepoint(*pygame.mouse.get_pos())
        draw_button(surf, "Start Race", btn, font_med, hover)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()
                    error = "Name cannot be empty!"
                elif ev.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and ev.unicode.isprintable():
                    name += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn.collidepoint(*ev.pos):
                    if name.strip():
                        return name.strip()
                    error = "Name cannot be empty!"


def run_game_screen(surf, clock, fonts, username, settings):
    font_big, font_med, font_sm = fonts
    game = Game(username, settings)

    while True:
        dt = clock.tick(FPS) / 1000

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "menu", 0, 0, 0
            game.handle_event(ev)

        game.update(dt)
        surf.fill(BLACK)
        game.draw(surf)

        if game.finished:
            add_score(username, game.score, game.distance, game.coin_count)
            return "finished", game.score, int(game.distance), game.coin_count

        if not game.alive:
            add_score(username, game.score, game.distance, game.coin_count)
            return "dead", game.score, int(game.distance), game.coin_count

        pygame.display.flip()


def run_gameover_screen(surf, clock, fonts, reason, score, distance, coins):
    font_big, font_med, font_sm = fonts
    title = "FINISH! 🏁" if reason == "finished" else "GAME OVER"
    title_col = GREEN if reason == "finished" else RED

    retry_btn = pygame.Rect(W//2 - 110, 420, 100, 44)
    menu_btn  = pygame.Rect(W//2 + 10,  420, 100, 44)

    while True:
        clock.tick(FPS)
        surf.fill(BG)

        t = font_big.render(title, True, title_col)
        surf.blit(t, t.get_rect(centerx=W//2, y=80))

        lines = [
            (f"Score:     {score}", YELLOW),
            (f"Distance:  {distance} m", WHITE),
            (f"Coins:     {coins}", ORANGE),
        ]
        for i, (txt, col) in enumerate(lines):
            s = font_med.render(txt, True, col)
            surf.blit(s, s.get_rect(centerx=W//2, y=200 + i*60))

        hovers = [r.collidepoint(*pygame.mouse.get_pos()) for r in [retry_btn, menu_btn]]
        draw_button(surf, "Retry",      retry_btn, font_med, hovers[0], color=(40,80,40))
        draw_button(surf, "Main Menu",  menu_btn,  font_med, hovers[1])

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if retry_btn.collidepoint(*ev.pos): return "retry"
                if menu_btn.collidepoint(*ev.pos):  return "menu"


def run_leaderboard_screen(surf, clock, fonts):
    font_big, font_med, font_sm = fonts
    entries = load_leaderboard()
    back_btn = pygame.Rect(W//2 - 60, H - 60, 120, 40)

    while True:
        clock.tick(FPS)
        surf.fill(BG)
        screen_title(surf, font_big, font_med, "TOP 10", "")

        # header
        hdr = font_sm.render(f"{'#':<3} {'Name':<16} {'Score':>7} {'Dist':>6} {'Coins':>5}", True, ACCENT)
        surf.blit(hdr, (20, 100))
        pygame.draw.line(surf, GRAY, (20, 118), (W - 20, 118), 1)

        for i, e in enumerate(entries):
            row_col = YELLOW if i == 0 else (GRAY if i >= 3 else WHITE)
            row = font_sm.render(
                f"{i+1:<3} {e['name']:<16} {e['score']:>7} {e['distance']:>5}m {e['coins']:>5}",
                True, row_col
            )
            surf.blit(row, (20, 126 + i * 26))

        if not entries:
            no = font_med.render("No scores yet!", True, GRAY)
            surf.blit(no, no.get_rect(centerx=W//2, y=200))

        hover = back_btn.collidepoint(*pygame.mouse.get_pos())
        draw_button(surf, "← Back", back_btn, font_med, hover)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if back_btn.collidepoint(*ev.pos): return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return


def run_settings_screen(surf, clock, fonts, settings):
    font_big, font_med, font_sm = fonts
    s = settings.copy()

    car_colors    = list(CAR_COLORS.keys())
    difficulties  = ["easy", "normal", "hard"]

    back_btn = pygame.Rect(W//2 - 60, H - 65, 120, 40)

    def cycle(lst, val, d=1):
        return lst[(lst.index(val) + d) % len(lst)]

    options = [
        ("Sound",       "sound",      "toggle"),
        ("Car Color",   "car_color",  car_colors),
        ("Difficulty",  "difficulty", difficulties),
    ]
    row_rects = [pygame.Rect(20, 140 + i * 80, W - 40, 60) for i in range(len(options))]

    while True:
        clock.tick(FPS)
        surf.fill(BG)
        screen_title(surf, font_big, font_med, "SETTINGS", "")

        for i, (label, key, vals) in enumerate(options):
            r = row_rects[i]
            pygame.draw.rect(surf, (30, 30, 38), r, border_radius=8)
            pygame.draw.rect(surf, (60, 60, 70), r, 1, border_radius=8)

            lbl = font_med.render(label, True, WHITE)
            surf.blit(lbl, (r.x + 12, r.y + 16))

            # value display
            val = s[key]
            if vals == "toggle":
                disp_col = GREEN if val else RED
                disp = "ON" if val else "OFF"
            else:
                disp_col = ACCENT
                disp = str(val).capitalize()

            disp_surf = font_med.render(disp, True, disp_col)
            surf.blit(disp_surf, (r.right - disp_surf.get_width() - 60, r.y + 16))

            # arrows
            arr_l = pygame.Rect(r.right - disp_surf.get_width() - 90, r.y + 10, 24, 38)
            arr_r = pygame.Rect(r.right - 34, r.y + 10, 24, 38)
            hover_l = arr_l.collidepoint(*pygame.mouse.get_pos())
            hover_r = arr_r.collidepoint(*pygame.mouse.get_pos())
            draw_button(surf, "◀", arr_l, font_sm, hover_l, color=(50,50,60))
            draw_button(surf, "▶", arr_r, font_sm, hover_r, color=(50,50,60))

        hover = back_btn.collidepoint(*pygame.mouse.get_pos())
        draw_button(surf, "✓ Save", back_btn, font_med, hover, color=(30,70,30))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if back_btn.collidepoint(mx, my):
                    save_settings(s)
                    return s

                for i, (label, key, vals) in enumerate(options):
                    r = row_rects[i]
                    arr_l = pygame.Rect(r.right - 120, r.y + 10, 24, 38)
                    arr_r = pygame.Rect(r.right - 34,  r.y + 10, 24, 38)
                    val = s[key]
                    if vals == "toggle":
                        if arr_l.collidepoint(mx, my) or arr_r.collidepoint(mx, my):
                            s[key] = not val
                    else:
                        if arr_l.collidepoint(mx, my):
                            s[key] = cycle(vals, val, -1)
                        elif arr_r.collidepoint(mx, my):
                            s[key] = cycle(vals, val, 1)

            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                save_settings(s)
                return s


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    pygame.init()
    surf  = pygame.display.set_mode((W, H))
    pygame.display.set_caption("RACER – TSIS 3")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("consolas", 42, bold=True)
    font_med = pygame.font.SysFont("consolas", 22, bold=True)
    font_sm  = pygame.font.SysFont("consolas", 14, bold=True)
    fonts    = (font_big, font_med, font_sm)

    settings = load_settings()
    username = None

    state = "menu"
    last_score = last_dist = last_coins = 0
    last_reason = "dead"

    while True:
        if state == "menu":
            choice = run_main_menu(surf, clock, fonts)
            if choice == "quit":
                pygame.quit(); sys.exit()
            elif choice == "play":
                username = run_username_screen(surf, clock, fonts)
                state = "game"
            elif choice == "leaderboard":
                run_leaderboard_screen(surf, clock, fonts)
            elif choice == "settings":
                settings = run_settings_screen(surf, clock, fonts, settings)

        elif state == "game":
            reason, score, dist, coins = run_game_screen(
                surf, clock, fonts, username, settings)
            last_score, last_dist, last_coins, last_reason = score, dist, coins, reason
            state = "gameover"

        elif state == "gameover":
            result = run_gameover_screen(
                surf, clock, fonts, last_reason, last_score, last_dist, last_coins)
            if result == "retry":
                state = "game"
            else:
                state = "menu"


if __name__ == "__main__":
    main()