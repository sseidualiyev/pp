import pygame
import sys
import os
import random

from persistence import load_settings, save_settings, load_leaderboard, add_score

# ── CONFIG ─────────────────────────────────────────
W, H = 480, 800
FPS = 60
LANES = [120, 240, 360]

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (200,50,50)
YELLOW= (240,200,50)

ASSETS = "assets"


# ── LOADERS ────────────────────────────────────────
def load_img(name, size=None):
    img = pygame.image.load(os.path.join(ASSETS, name)).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img


# ── GAME ───────────────────────────────────────────
class Game:
    def __init__(self, settings):
        self.settings = settings

        # load images
        self.player_img = load_img("player.png", (50, 80))
        self.enemy_img  = load_img("enemy.png",  (50, 80))
        self.coin_img   = load_img("coin.png",   (30, 30))

        # sounds
        pygame.mixer.music.load(os.path.join(ASSETS, "bg_music.m4a"))
        self.crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))

        if self.settings["sound"]:
            pygame.mixer.music.play(-1)

        self.reset()

    def reset(self):
        self.lane = 1
        self.speed = self.get_speed()
        self.score = 0
        self.distance = 0
        self.coins = 0
        self.alive = True

        self.enemies = []
        self.coins_list = []

    def get_speed(self):
        diff = self.settings["difficulty"]
        return {"easy":150, "normal":220, "hard":320}[diff]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane - 1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane + 1)

    def spawn_enemy(self):
        self.enemies.append({
            "lane": random.randint(0,2),
            "y": -100
        })

    def spawn_coin(self):
        self.coins_list.append({
            "lane": random.randint(0,2),
            "y": -50
        })

    def update(self, dt):
        self.distance += self.speed * dt
        self.score = int(self.distance / 10)

        # spawn
        if random.random() < 0.03:
            self.spawn_enemy()
        if random.random() < 0.02:
            self.spawn_coin()

        player_rect = pygame.Rect(LANES[self.lane], 700, 50, 80)

        # enemies
        for e in self.enemies[:]:
            e["y"] += self.speed * dt
            rect = pygame.Rect(LANES[e["lane"]], e["y"], 50, 80)

            if rect.colliderect(player_rect):
                self.alive = False
                if self.settings["sound"]:
                    self.crash_sound.play()

            if e["y"] > H:
                self.enemies.remove(e)

        # coins
        for c in self.coins_list[:]:
            c["y"] += self.speed * dt
            rect = pygame.Rect(LANES[c["lane"]], c["y"], 30, 30)

            if rect.colliderect(player_rect):
                self.coins += 1
                self.coins_list.remove(c)

            elif c["y"] > H:
                self.coins_list.remove(c)

    def draw(self, screen):
        # draw player
        screen.blit(self.player_img, (LANES[self.lane], 700))

        # enemies
        for e in self.enemies:
            screen.blit(self.enemy_img, (LANES[e["lane"]], e["y"]))

        # coins
        for c in self.coins_list:
            screen.blit(self.coin_img, (LANES[c["lane"]], c["y"]))

        # UI
        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10,10))
        screen.blit(font.render(f"Coins: {self.coins}", True, YELLOW), (10,40))


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
        text = f"{i+1}. {e['name']} | {e['score']} | {e['coins']}"
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
    pygame.mixer.init()

    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    state = "menu"
    settings = load_settings()
    game = Game(settings)
    leaderboard = load_leaderboard()

    while True:
        dt = clock.tick(FPS) / 1000

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
                        pygame.mixer.music.stop()
                        game = Game(settings)
                        state = "menu"

                    if event.key == pygame.K_d:
                        diff = ["easy", "normal", "hard"]
                        i = diff.index(settings["difficulty"])
                        settings["difficulty"] = diff[(i+1)%3]

                    if event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]

        # UPDATE
        if state == "game":
            game.update(dt)
            if not game.alive:
                add_score("Player", game.score, game.distance, game.coins)
                pygame.mixer.music.stop()
                state = "gameover"

        # DRAW
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