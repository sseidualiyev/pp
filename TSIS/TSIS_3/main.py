import pygame
import sys

from persistence import load_settings, save_settings, load_leaderboard, add_score
from racer import Game
from ui import W, H, BLACK


def draw_text(screen, text, y):
    font = pygame.font.SysFont(None, 40)
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, surf.get_rect(center=(W // 2, y)))


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    settings = load_settings()
    game = Game(settings)
    leaderboard = load_leaderboard()

    state = "menu"

    while True:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── MENU ──
            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game = Game(settings)
                    state = "game"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        leaderboard = load_leaderboard()
                        state = "leaderboard"

                    if event.key == pygame.K_s:
                        state = "settings"

            # ── GAME ──
            elif state == "game":
                game.handle_event(event)

            # ── SETTINGS ──
            elif state == "settings":
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        state = "menu"

                    if event.key == pygame.K_d:
                        order = ["easy", "normal", "hard"]
                        i = order.index(settings["difficulty"])
                        settings["difficulty"] = order[(i + 1) % 3]

                    if event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]
                        game.settings = settings
                        game.update_sound()

            # ── GAMEOVER ──
            elif state == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"

        # ── UPDATE ──
        if state == "game":
            game.update(dt)

            if not game.alive:
                add_score("Player", game.score, game.distance, game.coins)
                pygame.mixer.music.stop()
                state = "gameover"

        # ── DRAW ──
        screen.fill(BLACK)

        if state == "menu":
            draw_text(screen, "CLICK TO PLAY", 300)
            draw_text(screen, "L - LEADERBOARD", 360)
            draw_text(screen, "S - SETTINGS", 420)

        elif state == "game":
            game.draw(screen)

        elif state == "gameover":
            draw_text(screen, "GAME OVER", 300)

        elif state == "leaderboard":
            draw_text(screen, "TOP 10", 100)
            y = 160
            for i, e in enumerate(leaderboard):
                draw_text(screen, f"{i+1}. {e['name']} {e['score']}", y)
                y += 40

        elif state == "settings":
            draw_text(screen, "SETTINGS", 200)
            draw_text(screen, f"Difficulty: {settings['difficulty']}", 260)
            draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 320)
            draw_text(screen, "D - difficulty", 400)
            draw_text(screen, "M - sound toggle", 440)

        pygame.display.flip()


if __name__ == "__main__":
    main()