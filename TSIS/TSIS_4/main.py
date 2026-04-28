import pygame
from game import SnakeGame
from db import *
from settings import load_settings, save_settings

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

init_db()

MENU, GAME, LB, SETTINGS = "menu","game","lb","settings"
state = MENU

game = SnakeGame()

username = ""
player_id = None
typing = True

settings = load_settings()
snake_color = tuple(settings["snake_color"])
grid = settings.get("grid", True)
sound = settings.get("sound", False)

def text(t,x,y,s=30):
    f = pygame.font.SysFont(None,s)
    screen.blit(f.render(t,True,WHITE),(x,y))

# SOUND
if sound:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/bg.mp3")
    pygame.mixer.music.play(-1)

running = True
while running:

    screen.fill(BLACK)
    events = pygame.event.get()

    # ---------------- GLOBAL QUIT ----------------
    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:

            # ESC NAVIGATION
            if e.key == pygame.K_ESCAPE:
                if state == GAME:
                    state = MENU
                    typing = True

                elif state == LB:
                    state = MENU

                elif state == SETTINGS:
                    settings["snake_color"] = list(snake_color)
                    settings["grid"] = grid
                    settings["sound"] = sound
                    save_settings(settings)
                    state = MENU

            # MENU
            if state == MENU:

                if typing:
                    if e.key == pygame.K_RETURN:
                        player_id = get_or_create_player(username)
                        typing = False

                    elif e.key == pygame.K_BACKSPACE:
                        username = username[:-1]

                    else:
                        username += e.unicode

                else:
                    if e.key == pygame.K_g:
                        game.reset()
                        state = GAME

                    elif e.key == pygame.K_l:
                        state = LB

                    elif e.key == pygame.K_s:
                        state = SETTINGS

            # GAME INPUT
            elif state == GAME:
                if e.key == pygame.K_UP: game.set_direction((0,-1))
                if e.key == pygame.K_DOWN: game.set_direction((0,1))
                if e.key == pygame.K_LEFT: game.set_direction((-1,0))
                if e.key == pygame.K_RIGHT: game.set_direction((1,0))

            # SETTINGS
            elif state == SETTINGS:
                if e.key == pygame.K_r: snake_color=(255,0,0)
                if e.key == pygame.K_g: snake_color=(0,255,0)
                if e.key == pygame.K_b: snake_color=(0,0,255)
                if e.key == pygame.K_f: grid = not grid
                if e.key == pygame.K_m:
                    sound = not sound
                    if sound:
                        pygame.mixer.init()
                        pygame.mixer.music.load("assets/bg.mp3")
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

    # ---------------- GAME ----------------
    if state == GAME:

        if game.can_move():
            if game.update() == "game_over":
                save_session(player_id, game.score, game.level)
                state = MENU
                typing = True
                username = ""

        game.draw(screen, snake_color, grid)

        # SCORE + LEVEL (FIXED)
        text(f"Score: {game.score}",10,10,25)
        text(f"Level: {game.level}",10,35,25)

    # ---------------- MENU ----------------
    elif state == MENU:
        text("SNAKE",250,80,50)
        text("Name: " + username,180,220)
        text("ENTER = Save",160,280)
        text("G Play | L LB | S Settings",120,340)

    # ---------------- LB ----------------
    elif state == LB:
        text("LEADERBOARD",200,50,40)
        data = get_leaderboard()

        y=120
        for i,r in enumerate(data):
            text(f"{i+1}. {r[0]} {r[1]} L{r[2]}",150,y)
            y+=40

    # ---------------- SETTINGS ----------------
    elif state == SETTINGS:
        text("SETTINGS",240,60,40)
        text(f"Color {snake_color}",180,160)
        text("R/G/B color",200,200)
        text(f"Grid {grid}",200,260)
        text(f"Sound {sound}",200,300)
        text("ESC save",220,380)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()