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

# ---------------- STATES ----------------
MENU, GAME, LEADERBOARD, SETTINGS = "menu","game","lb","settings"
state = MENU

game = SnakeGame()

# ---------------- USER ----------------
username = ""
player_id = None
typing_name = True   # ✅ FIX: prevents L/S conflict

settings = load_settings()
snake_color = tuple(settings["snake_color"])

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

                # ✅ START GAME ONLY IF NAME EXISTS
                if e.key == pygame.K_RETURN and username:
                    player_id = get_or_create_player(username)
                    game.reset()
                    state = GAME
                    typing_name = False

                # ✅ ONLY NAVIGATION WHEN NOT TYPING
                elif not typing_name:
                    if e.key == pygame.K_l:
                        state = LEADERBOARD
                    elif e.key == pygame.K_s:
                        state = SETTINGS

                # ✅ TYPING MODE
                else:
                    if e.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif e.unicode.isalnum():
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
                    typing_name = True   # reset typing mode

                if e.key == pygame.K_UP:
                    game.set_direction((0,-1))
                if e.key == pygame.K_DOWN:
                    game.set_direction((0,1))
                if e.key == pygame.K_LEFT:
                    game.set_direction((-1,0))
                if e.key == pygame.K_RIGHT:
                    game.set_direction((1,0))

        # ✅ FIXED SPEED CONTROL
        if game.can_move():
            status = game.update()

            if status == "game_over":
                save_session(player_id, game.score, game.level)
                state = MENU
                typing_name = True
                username = ""

        game.draw(screen, snake_color)

        draw_text(f"Score: {game.score}", 10,10,25)
        draw_text(f"Level: {game.level}", 10,40,25)

    # =================================================
    # LEADERBOARD
    # =================================================
    elif state == LEADERBOARD:
        draw_text("LEADERBOARD", 220, 50, 40)

        data = get_leaderboard()
        y = 120

        for i, row in enumerate(data):
            draw_text(f"{i+1}. {row[0]} | {row[1]} | L{row[2]}", 120, y)
            y += 40

        draw_text("ESC - Back", 240, 520)

        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                state = MENU

    # =================================================
    # SETTINGS
    # =================================================
    elif state == SETTINGS:
        draw_text("SETTINGS", 250, 80, 40)
        draw_text(f"Snake color: {snake_color}", 150, 200)
        draw_text("R / G / B", 150, 240)
        draw_text("ESC - Back", 240, 500)

        for e in events:
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_r:
                    snake_color = (255,0,0)
                elif e.key == pygame.K_g:
                    snake_color = (0,255,0)
                elif e.key == pygame.K_b:
                    snake_color = (0,0,255)

                elif e.key == pygame.K_ESCAPE:
                    settings["snake_color"] = list(snake_color)
                    save_settings(settings)
                    state = MENU

    pygame.display.flip()
    clock.tick(60)

pygame.quit()