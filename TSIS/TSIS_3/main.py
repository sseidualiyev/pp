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

    player_name = ""
    typing_name = False

    game = Game(settings)
    leaderboard = load_leaderboard()

    state = "menu"

    while True:
        dt = clock.tick(60) / 1000

        # ───────────────── EVENT HANDLING ─────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ───────────────── MENU ─────────────────
            if state == "menu":

                if event.type == pygame.KEYDOWN:

                    # toggle typing mode
                    if event.key == pygame.K_RETURN:
                        typing_name = not typing_name

                    # typing input
                    elif typing_name:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        elif event.unicode.isprintable() and len(player_name) < 12:
                            player_name += event.unicode

                    # menu shortcuts (only when NOT typing)
                    else:
                        if event.key == pygame.K_l:
                            leaderboard = load_leaderboard()
                            state = "leaderboard"

                        elif event.key == pygame.K_s:
                            state = "settings"

                # start game (SAFE CHECK)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not typing_name and player_name.strip() != "":
                        game = Game(settings)
                        game.player_name = player_name
                        state = "game"

            # ───────────────── GAME ─────────────────
            elif state == "game":
                game.handle_event(event)

            # ───────────────── SETTINGS ─────────────────
            elif state == "settings":
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        state = "menu"

                    elif event.key == pygame.K_d:
                        order = ["easy", "normal", "hard"]
                        i = order.index(settings["difficulty"])
                        settings["difficulty"] = order[(i + 1) % 3]

                    elif event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]
                        game.settings = settings
                        game.update_sound()

            # ───────────────── LEADERBOARD ─────────────────
            elif state == "leaderboard":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"

            # ───────────────── GAME OVER ─────────────────
            elif state == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"

        # ───────────────── UPDATE ─────────────────
        if state == "game":
            game.update(dt)

            if not game.alive:
                add_score(game.player_name, game.score, game.distance, game.coins)
                pygame.mixer.music.stop()
                state = "gameover"

        # ───────────────── DRAW ─────────────────
        screen.fill(BLACK)

        # MENU
        if state == "menu":
            draw_text(screen, "RACING GAME", 140)

            draw_text(screen, "PRESS ENTER TO TOGGLE NAME INPUT", 220)

            if typing_name:
                draw_text(screen, "TYPING NAME:", 260)
                draw_text(screen, player_name + "_", 300)
            else:
                draw_text(screen, "NAME: " + player_name, 300)

            draw_text(screen, "CLICK TO START", 380)
            draw_text(screen, "L - LEADERBOARD", 440)
            draw_text(screen, "S - SETTINGS", 500)

        # GAME
        elif state == "game":
            game.draw(screen)

        # GAME OVER
        elif state == "gameover":
            draw_text(screen, "GAME OVER", 300)

        # LEADERBOARD
        elif state == "leaderboard":
            draw_text(screen, "TOP 10", 100)
            y = 160
            for i, e in enumerate(leaderboard):
                draw_text(screen, f"{i+1}. {e['name']} {e['score']}", y)
                y += 40
            draw_text(screen, "PRESS ESC TO RETURN", 600)

        # SETTINGS
        elif state == "settings":
            draw_text(screen, "SETTINGS", 200)
            draw_text(screen, f"Difficulty: {settings['difficulty']}", 260)
            draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 320)
            draw_text(screen, "D - change difficulty", 400)
            draw_text(screen, "M - toggle sound", 440)
            draw_text(screen, "ESC - back", 500)

        pygame.display.flip()


if __name__ == "__main__":
    main()