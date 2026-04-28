import pygame
from game import SnakeGame
from db import *
from settings import load_settings, save_settings

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

init_db()

# ---------------- STATE ----------------
MENU, GAME, LEADERBOARD, SETTINGS = "menu","game","lb","settings"
state = MENU

game = SnakeGame()

# ---------------- USER ----------------
username = ""
player_id = None

settings = load_settings()
snake_color = tuple(settings["snake_color"])

# ---------------- HELPERS ----------------
def draw_text(text, x, y, size=30):
    font = pygame.font.SysFont(None, size)
    screen.blit(font.render(text, True, WHITE), (x,y))

# ================= MAIN LOOP =================
running = True
while running:
    screen.fill(BLACK)

    events = pygame.event.get()

    # =================================================
    # MENU
    # =================================================
    if state == MENU:
        draw_text("SNAKE GAME", 200, 100, 50)
        draw_text("Enter name: " + username, 180, 250)
        draw_text("ENTER - Play", 200, 320)
        draw_text("L - Leaderboard", 200, 360)
        draw_text("S - Settings", 200, 400)

        for e in events:
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and username:
                    player_id = get_or_create_player(username)
                    game.reset()
                    state = GAME

                elif e.key == pygame.K_l:
                    state = LEADERBOARD

                elif e.key == pygame.K_s:
                    state = SETTINGS

                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += e.unicode

    # =================================================
    # GAME
    # =================================================
    elif state == GAME:

        for e in events:
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    state = MENU

                if e.key == pygame.K_UP:
                    game.set_direction((0,-1))
                if e.key == pygame.K_DOWN:
                    game.set_direction((0,1))
                if e.key == pygame.K_LEFT:
                    game.set_direction((-1,0))
                if e.key == pygame.K_RIGHT:
                    game.set_direction((1,0))

        status = game.update()

        if status == "game_over":
            save_session(player_id, game.score, game.level)
            state = MENU

        game.draw(screen, snake_color)

        draw_text(f"Score: {game.score}", 10,10,25)
        draw_text(f"Level: {game.level}", 10,40,25)

    # =================================================
    # LEADERBOARD
    # =================================================
    elif state == LEADERBOARD:
        draw_text("LEADERBOARD (TOP 10)", 150, 50, 30)

        data = get_leaderboard()

        y = 120
        for i, row in enumerate(data):
            draw_text(f"{i+1}. {row[0]} | {row[1]} | L{row[2]}", 120, y)
            y += 40

        draw_text("ESC - Back", 220, 520)

        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                state = MENU

    # =================================================
    # SETTINGS
    # =================================================
    elif state == SETTINGS:
        draw_text("SETTINGS", 250, 80, 40)

        draw_text(f"Snake color: {snake_color}", 150, 200)
        draw_text("R - Red, G - Green, B - Blue", 150, 240)

        draw_text("ESC - Back", 220, 500)

        for e in events:
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_r:
                    snake_color = (255,0,0)

                if e.key == pygame.K_g:
                    snake_color = (0,255,0)

                if e.key == pygame.K_b:
                    snake_color = (0,0,255)

                if e.key == pygame.K_ESCAPE:
                    settings["snake_color"] = list(snake_color)
                    save_settings(settings)
                    state = MENU

    pygame.display.flip()
    BASE_FPS = 60
    clock.tick(BASE_FPS)

pygame.quit()