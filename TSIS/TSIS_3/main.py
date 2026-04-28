import pygame
import sys
import os
import random

from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import *

ASSETS = "assets"


def load_img(name, size):
    img = pygame.image.load(os.path.join(ASSETS, name)).convert_alpha()
    return pygame.transform.scale(img, size)


class Game:
    def __init__(self, settings):
        self.settings = settings

        self.player_img = load_img("player.png", (50,80))
        self.enemy_img  = load_img("enemy.png",  (50,80))
        self.coin_img   = load_img("coin.png",   (30,30))

        pygame.mixer.music.load(os.path.join(ASSETS, "bg_music.mp3"))
        self.crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))

        if settings["sound"]:
            pygame.mixer.music.play(-1)

        self.reset()

    def reset(self):
        self.lane = 1
        self.base_speed = {"easy":150,"normal":220,"hard":300}[self.settings["difficulty"]]
        self.speed = self.base_speed

        self.score = 0
        self.distance = 0
        self.coins = 0

        self.enemies = []
        self.coins_list = []
        self.powerups = []

        self.powerup = None
        self.power_timer = 0
        self.shield = False

        self.scroll = 0
        self.alive = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.lane = max(0, self.lane-1)
            if event.key == pygame.K_RIGHT:
                self.lane = min(2, self.lane+1)

    def spawn_enemy(self):
        if len(self.enemies) < 3:
            self.enemies.append({"lane":random.randint(0,2),"y":-100})

    def spawn_coin(self):
        if random.random() < 0.5:
            self.coins_list.append({"lane":random.randint(0,2),"y":-50})

    def spawn_powerup(self):
        if random.random() < 0.005:
            typ = random.choice(["nitro","shield","repair"])
            self.powerups.append({"lane":random.randint(0,2),"y":-50,"type":typ})

    def update(self, dt):
        self.scroll += self.speed * dt
        self.distance += self.speed * dt
        self.score = int(self.distance / 10)

        if random.random() < 0.015:
            self.spawn_enemy()
        if random.random() < 0.02:
            self.spawn_coin()
        self.spawn_powerup()

        player = pygame.Rect(LANES[self.lane], 700, 50, 80)

        for e in self.enemies[:]:
            e["y"] += self.speed * dt
            rect = pygame.Rect(LANES[e["lane"]], e["y"], 50, 80)

            if rect.colliderect(player):
                if self.shield:
                    self.shield = False
                    self.enemies.remove(e)
                else:
                    if self.settings["sound"]:
                        self.crash_sound.play()
                    self.alive = False
            elif e["y"] > H:
                self.enemies.remove(e)

        for c in self.coins_list[:]:
            c["y"] += self.speed * dt
            rect = pygame.Rect(LANES[c["lane"]], c["y"], 30, 30)

            if rect.colliderect(player):
                self.coins += 1
                self.coins_list.remove(c)
            elif c["y"] > H:
                self.coins_list.remove(c)

        for p in self.powerups[:]:
            p["y"] += self.speed * dt
            rect = pygame.Rect(LANES[p["lane"]], p["y"], 30, 30)

            if rect.colliderect(player):
                self.activate(p["type"])
                self.powerups.remove(p)
            elif p["y"] > H:
                self.powerups.remove(p)

        if self.power_timer > 0:
            self.power_timer -= dt
        else:
            self.powerup = None
            self.speed = self.base_speed

    def activate(self, typ):
        self.powerup = typ
        self.power_timer = 5

        if typ == "nitro":
            self.speed = self.base_speed * 1.8
        elif typ == "shield":
            self.shield = True
        elif typ == "repair":
            self.alive = True

    def draw(self, screen):
        draw_road(screen, self.scroll)

        screen.blit(self.player_img, (LANES[self.lane], 700))

        for e in self.enemies:
            screen.blit(self.enemy_img, (LANES[e["lane"]], e["y"]))

        for c in self.coins_list:
            screen.blit(self.coin_img, (LANES[c["lane"]], c["y"]))

        colors = {"nitro":(255,140,0),"shield":(0,200,255),"repair":(0,255,100)}
        for p in self.powerups:
            pygame.draw.circle(screen, colors[p["type"]],
                               (LANES[p["lane"]]+15, int(p["y"])+15), 15)

        draw_hud(screen, self.score, self.coins, self.powerup, self.power_timer)


def draw_text(screen, text, y):
    font = pygame.font.SysFont(None, 40)
    surf = font.render(text, True, WHITE)
    screen.blit(surf, surf.get_rect(center=(W//2, y)))


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    settings = load_settings()
    game = Game(settings)
    leaderboard = load_leaderboard()

    state = "menu"

    while True:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

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
                        diff = ["easy","normal","hard"]
                        i = diff.index(settings["difficulty"])
                        settings["difficulty"] = diff[(i+1)%3]
                    if event.key == pygame.K_m:
                        settings["sound"] = not settings["sound"]

        if state == "game":
            game.update(dt)
            if not game.alive:
                add_score("Player", game.score, game.distance, game.coins)
                pygame.mixer.music.stop()
                state = "gameover"

        screen.fill(BLACK)

        if state == "menu":
            draw_text(screen, "CLICK TO PLAY", 300)
            draw_text(screen, "L - LEADERBOARD", 360)
            draw_text(screen, "S - SETTINGS", 420)

        elif state == "game":
            game.draw(screen)

        elif state == "gameover":
            draw_text(screen, "GAME OVER", 300)

        elif state == "leaderboard":
            draw_text(screen, "TOP 10", 100)
            y = 160
            for i,e in enumerate(leaderboard):
                txt = f"{i+1}. {e['name']} {e['score']} {e['coins']}"
                draw_text(screen, txt, y)
                y += 40

        elif state == "settings":
            draw_text(screen, "SETTINGS", 200)
            draw_text(screen, f"Difficulty: {settings['difficulty']}", 260)
            draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 320)
            draw_text(screen, "D - change difficulty", 400)
            draw_text(screen, "M - toggle sound", 440)

        pygame.display.flip()


if __name__ == "__main__":
    main()