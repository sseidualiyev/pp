import pygame
import sys
import json
import os
import random

# ── CONFIG ─────────────────────────────────────────
W, H = 480, 800
FPS = 60

LANES = [120, 240, 360]

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (200,50,50)
GREEN = (50,200,50)
YELLOW= (240,200,50)

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"


# ── PERSISTENCE ────────────────────────────────────
def load_json(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def add_score(name, score, distance, coins):
    data = load_leaderboard()
    data.append({
        "name": name,
        "score": score,
        "distance": int(distance),
        "coins": coins
    })
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_json(LEADERBOARD_FILE, data)


def load_settings():
    return load_json(SETTINGS_FILE, {
        "difficulty": "normal",
        "sound": True
    })


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


# ── GAME ───────────────────────────────────────────
class Game:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        self.lane = 1
        self.speed = self.get_speed()
        self.score = 0
        self.distance = 0
        self.coins = 0
        self.alive = True

    def get_speed(self):
        diff = self.settings["difficulty"]
        if diff == "easy":
            return 150
        elif diff == "hard":
            return 300
        return 220

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane - 1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane + 1)

    def update(self, dt):
        self.distance += self.speed * dt
        self.score = int(self.distance / 10)

        # random coins
        if random.random() < 0.02:
            self.coins += 1

        # simple lose condition (random crash simulation)
        if random.random() < 0.002:
            self.alive = False

    def draw(self, screen):
        x = LANES[self.lane]

        pygame.draw.rect(screen, WHITE, (x, 700, 40, 60))

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10,10))
        screen.blit(font.render(f"Coins: {self.coins}", True, YELLOW), (10,40))
        screen.blit(font.render(f"Speed: {int(self.speed)}", True, GREEN), (10,70))


# ── DRAW ───────────────────────────────────────────
def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    screen.blit(font.render(text, True, color), (x, y))


def draw_menu(screen):
    draw_text(screen, "RACER", 60, 150, 100, YELLOW)
    draw_text(screen, "Click to Play", 30, 150, 300)
    draw_text(screen, "L - Leaderboard", 25, 140, 350)
    draw_text(screen, "S - Settings", 25, 160, 400)


def draw_gameover(screen, score):
    draw_text(screen, "GAME OVER", 50, 130, 200, RED)
    draw_text(screen, f"Score: {score}", 30, 160, 300)
    draw_text(screen, "Click to Menu", 25, 140, 360)


def draw_leaderboard(screen, entries):
    draw_text(screen, "TOP 10", 50, 150, 50, YELLOW)

    y = 150
    for i, e in enumerate(entries):
        text = f"{i+1}. {e.get('name','?')} | {e.get('score',0)} | {e.get('coins',0)}"
        draw_text(screen, text, 24, 40, y)
        y += 40

    draw_text(screen, "ESC to return", 25, 140, 700)


def draw_settings(screen, settings):
    draw_text(screen, "SETTINGS", 50, 140, 100, YELLOW)

    draw_text(screen, f"Difficulty: {settings['difficulty']}", 30, 120, 250)
    draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 30, 150, 300)

    draw_text(screen, "D - Change Difficulty", 25, 100, 400)
    draw_text(screen, "M - Toggle Sound", 25, 120, 440)
    draw_text(screen, "ESC - Back", 25, 150, 500)


# ── MAIN ───────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    state = "menu"
    settings = load_settings()
    game = Game(settings)

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
                    game = Game(settings)
                    state = "game"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        leaderboard = load_leaderboard()
                        state = "leaderboard"
                    if event.key == pygame.K_s:
                        state = "settings"

            elif state == "game":
                game.handle_event(event)

            elif state == "gameover":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "menu"

            elif state == "leaderboard":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

            elif state == "settings":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        save_settings(settings)
                        state = "menu"
                    if event.key == pygame.K_d:
                        # cycle difficulty
                        diff = ["easy", "normal", "hard"]
                        i = diff.index(settings["difficulty"])
                        settings["difficulty"] = diff[(i+1)%3]
                    if event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]

        # ── UPDATE ──
        if state == "game":
            game.update(dt)
            if not game.alive:
                add_score("Player", game.score, game.distance, game.coins)
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

        elif state == "settings":
            draw_settings(screen, settings)

        pygame.display.flip()


if __name__ == "__main__":
    main()