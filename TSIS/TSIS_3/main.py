import pygame
import sys

from racer import Game
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import W, H, BLACK, WHITE


# ─────────────────────────────────────────────
# TEXT HELPER
# ─────────────────────────────────────────────
def draw_text(screen, text, y, size=40, color=WHITE):
    font = pygame.font.SysFont("consolas", size, bold=True)
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(W // 2, y)))


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    settings = load_settings()
    leaderboard = load_leaderboard()

    game = None
    state = "menu"

    def apply_sound():
        """Force music state based on settings"""
        if settings["sound"]:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    running = True

    while running:
        dt = clock.tick(60) / 1000

        # ───────────────── EVENTS ─────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ───────── MENU ─────────
            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game = Game(settings)   # difficulty applied here
                    state = "game"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        leaderboard = load_leaderboard()
                        state = "leaderboard"

                    if event.key == pygame.K_s:
                        state = "settings"

            # ───────── GAME ─────────
            elif state == "game":
                game.handle_event(event)

            # ───────── GAMEOVER ─────────
            elif state == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"

            # ───────── LEADERBOARD ─────────
            elif state == "leaderboard":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

            # ───────── SETTINGS ─────────
            elif state == "settings":
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        apply_sound()
                        state = "menu"

                    # change difficulty
                    if event.key == pygame.K_d:
                        order = ["easy", "normal", "hard"]
                        i = order.index(settings["difficulty"])
                        settings["difficulty"] = order[(i + 1) % 3]

                    # toggle sound
                    if event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]
                        apply_sound()

        # ───────────────── UPDATE ─────────────────
        if state == "game":
            game.update(dt)

            # GAME OVER
            if not game.alive:
                add_score("Player", game.score, game.distance, game.coins)
                pygame.mixer.music.stop()
                state = "gameover"

        # ───────────────── DRAW ─────────────────
        screen.fill(BLACK)

        if state == "menu":
            draw_text(screen, "CLICK TO PLAY", 300)
            draw_text(screen, "L - LEADERBOARD", 360, 30)
            draw_text(screen, "S - SETTINGS", 420, 30)

        elif state == "game":
            game.draw(screen)

        elif state == "gameover":
            draw_text(screen, "GAME OVER", 300)

        elif state == "leaderboard":
            draw_text(screen, "TOP 10", 100)

            y = 160
            for i, e in enumerate(leaderboard):
                txt = f"{i+1}. {e['name']}  {e['score']}  {e['coins']}"
                draw_text(screen, txt, y, 30)
                y += 40

        elif state == "settings":
            draw_text(screen, "SETTINGS", 200)
            draw_text(screen, f"Difficulty: {settings['difficulty']}", 260, 30)
            draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 320, 30)
            draw_text(screen, "D - change difficulty", 400, 25)
            draw_text(screen, "M - toggle sound", 440, 25)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()