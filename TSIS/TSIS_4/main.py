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

# ---------------- SOUND INIT ----------------
if sound:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/bg.mp3")
    pygame.mixer.music.play(-1)

running = True
while running:

    screen.fill(BLACK)
    events = pygame.event.get()

    # ================= GLOBAL EVENTS (FIXED QUIT) =================
    for e in events:
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:

            # ESC handling per state
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

            # ---------------- MENU ----------------
            if state == MENU:

                # typing name
                if typing:
                    if e.key == pygame.K_RETURN:
                        player_id = get_or_create_player(username)
                        typing = False

                    elif e.key == pygame.K_BACKSPACE:
                        username = username[:-1]

                    else:
                        username += e.unicode

                # navigation (ONLY after typing done)
                if not typing:
                    if e.key == pygame.K_g:
                        game.reset()
                        state = GAME

                    elif e.key == pygame.K_l:
                        state = LB

                    elif e.key == pygame.K_s:
                        state = SETTINGS

            # ---------------- GAME ----------------
            elif state == GAME:
                if e.key == pygame.K_UP: game.set_direction((0,-1))
                if e.key == pygame.K_DOWN: game.set_direction((0,1))
                if e.key == pygame.K_LEFT: game.set_direction((-1,0))
                if e.key == pygame.K_RIGHT: game.set_direction((1,0))

            # ---------------- SETTINGS ----------------
            elif state == SETTINGS:

                if e.key == pygame.K_r:
                    snake_color = (255,0,0)

                elif e.key == pygame.K_g:
                    snake_color = (0,255,0)

                elif e.key == pygame.K_b:
                    snake_color = (0,0,255)

                elif e.key == pygame.K_f:
                    grid = not grid

                elif e.key == pygame.K_m:
                    sound = not sound
                    if sound:
                        pygame.mixer.init()
                        pygame.mixer.music.load("assets/bg.mp3")
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

    # ================= GAME LOGIC =================
    if state == GAME:

        if game.can_move():
            if game.update() == "game_over":
                save_session(player_id, game.score, game.level)
                state = MENU
                typing = True
                username = ""

        game.draw(screen, snake_color, grid)

    # ================= MENU UI =================
    elif state == MENU:
        text("SNAKE",250,80,50)
        text("Name: " + username,180,220)
        text("ENTER = Save Name",160,280)
        text("G = Play",250,320)
        text("L = Leaderboard",220,360)
        text("S = Settings",240,400)

    # ================= LEADERBOARD =================
    elif state == LB:
        text("LEADERBOARD",200,50,40)
        data = get_leaderboard()

        y=120
        for i,r in enumerate(data):
            text(f"{i+1}. {r[0]} {r[1]} L{r[2]}",150,y)
            y+=40

        text("ESC BACK",240,500)

    # ================= SETTINGS =================
    elif state == SETTINGS:
        text("SETTINGS",240,60,40)
        text(f"Color {snake_color}",180,160)
        text("R/G/B = color",200,200)
        text(f"Grid: {grid}",200,260)
        text(f"Sound: {sound}",200,300)
        text("ESC SAVE & BACK",180,400)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()