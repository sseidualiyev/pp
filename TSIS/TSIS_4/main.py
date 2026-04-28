import pygame
from game import SnakeGame
from db import *
from settings import load_settings

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)

game = SnakeGame()
state = "menu"

username = ""
typing = True
player_id = None

settings = load_settings()
snake_color = tuple(settings["snake_color"])

init_db()

# ---------------- MAIN LOOP ----------------
running = True
while running:
    screen.fill(BLACK)

    # ================= MENU =================
    if state == "menu":
        font = pygame.font.SysFont(None, 40)
        screen.blit(font.render("Enter name:", True, WHITE), (200,200))
        screen.blit(font.render(username, True, WHITE), (220,260))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    player_id = get_or_create_player(username)
                    state = "game"
                    game.reset()

                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += e.unicode

    # ================= GAME =================
    elif state == "game":

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
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
            state = "menu"

        game.draw(screen, snake_color)

        font = pygame.font.SysFont(None, 25)
        screen.blit(font.render(
            f"Score:{game.score} Level:{game.level}",
            True, WHITE), (10,10))

    pygame.display.flip()
    clock.tick(game.speed)

pygame.quit()