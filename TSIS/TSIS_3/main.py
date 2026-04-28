import pygame
import random

from racer import RacerGame
from ui import UI
from persistence import *

pygame.init()

screen = pygame.display.set_mode((480, 800))
font = pygame.font.SysFont("Verdana", 24)

PLAYER_SIZE = (60, 100)
ENEMY_SIZE = (60, 100)
COIN_SIZE = (30, 30)

assets = {
    "player": pygame.transform.scale(
        pygame.image.load("assets/Player.png").convert_alpha(),
        PLAYER_SIZE
    ),

    "enemy": pygame.transform.scale(
        pygame.image.load("assets/Enemy.png").convert_alpha(),
        ENEMY_SIZE
    ),

    "coin": pygame.transform.scale(
        pygame.image.load("assets/coin.png").convert_alpha(),
        COIN_SIZE
    )
}

game = RacerGame(assets)
ui = UI(screen, font)

settings = load_settings()

state = "menu"
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # MENU
    if state == "menu":
        ui.main_menu()
        if keys[pygame.K_1]:
            state = "game"

    # GAME
    elif state == "game":

        if keys[pygame.K_LEFT]:
            game.move_player("left")
        if keys[pygame.K_RIGHT]:
            game.move_player("right")

        status = game.update()

        screen.fill((255, 255, 255))
        screen.blit(assets["player"], game.player)

        if status == "game_over":
            add_score("PLAYER", game.coins, game.distance)
            state = "game_over"

    # GAME OVER
    elif state == "game_over":
        ui.game_over(game.coins, game.distance)

        if keys[pygame.K_r]:
            game = RacerGame(assets)
            state = "game"

    pygame.display.update()