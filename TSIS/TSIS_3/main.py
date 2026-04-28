import pygame
import sys
import json
import os
import random

# ── CONFIG ─────────────────────────────────────────
W, H = 480, 800
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (200,50,50)
GREEN = (50,200,50)
YELLOW= (240,200,50)

LEADERBOARD_FILE = "leaderboard.json"


# ── SIMPLE PERSISTENCE ─────────────────────────────
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_score(name, score, distance, coins):
    data = load_leaderboard()
    data.append({
        "name": name,
        "score": score,
        "distance": int(distance),
        "coins": coins
    })
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(data)


# ── GAME CLASS (VERY SIMPLE) ───────────────────────
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player_x = W // 2
        self.speed = 200
        self.score = 0
        self.distance = 0
        self.coins = 0
        self.alive = True

    def handle_event(self, event):
        pass

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player_x -= 200 * dt
        if keys[pygame.K_RIGHT]:
            self.player_x += 200 * dt

        self.distance += self.speed * dt
        self.score = int(self.distance / 10)

        # random coin
        if random.random() < 0.01:
            self.coins += 1

        # simple lose condition
        if self.player_x < 0 or self.player_x > W:
            self.alive = False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.player_x, 700, 40, 60))

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10,10))
        screen.blit(font.render(f"Coins: {self.coins}", True, YELLOW), (10,40))


# ── DRAW FUNCTIONS ─────────────────────────────────
def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_menu(screen):
    draw_text(screen, "RACER", 60, 150, 100, YELLOW)
    draw_text(screen, "Click to Play", 30, 150, 300)
    draw_text(screen, "L - Leaderboard", 25, 140, 350)


def draw_gameover(screen, score):
    draw_text(screen, "GAME OVER", 50, 130, 200, RED)
    draw_text(screen, f"Score: {score}", 30, 160, 300)
    draw_text(screen, "Click to Menu", 25, 140, 360)


def draw_leaderboard(screen, entries):
    draw_text(screen, "TOP 10", 50, 150, 50, YELLOW)

    y = 150
    for i, e in enumerate(entries):
        name = e.get("name", "Unknown")
        score = e.get("score", 0)
        dist = e.get("distance", 0)
        coins = e.get("coins", 0)

        text = f"{i+1}. {name} | {score} | {dist}m | {coins}"
        draw_text(screen, text, 24, 40, y)
        y += 40

    draw_text(screen, "ESC to return", 25, 140, 700)


# ── MAIN ───────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    state = "menu"
    game = Game()
    username = "Player"

    leaderboard = load_leaderboard()

    while True:
        dt = clock.tick(FPS) / 1000

        # ── EVENTS ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.reset()
                    state = "game"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        leaderboard = load_leaderboard()
                        state = "leaderboard"

            elif state == "game":
                game.handle_event(event)

            elif state == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"

            elif state == "leaderboard":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

        # ── UPDATE ──
        if state == "game":
            game.update(dt)
            if not game.alive:
                add_score(username, game.score, game.distance, game.coins)
                state = "gameover"

        # ── DRAW ──
        screen.fill(BLACK)

        if state == "menu":
            draw_menu(screen)

        elif state == "game":
            game.draw(screen)

        elif state == "gameover":
            draw_gameover(screen, game.score)

        elif state == "leaderboard":
            draw_leaderboard(screen, leaderboard)

        pygame.display.flip()


if __name__ == "__main__":
    main()