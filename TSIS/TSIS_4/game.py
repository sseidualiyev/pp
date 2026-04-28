import pygame
import random
import time

WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = WIDTH // CELL

RED = (255,0,0)
DARK_RED = (120,0,0)
CYAN = (0,255,255)

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(5,5),(4,5),(3,5)]
        self.direction = (1,0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()
        self.power = self.spawn_power()

        # ⏱ movement control (FIXED SPEED SYSTEM)
        self.move_delay = 150  # ms
        self.last_move_time = pygame.time.get_ticks()

    # ---------------- SPAWNS ----------------
    def spawn_food(self):
        return {
            "pos": (random.randint(0,ROWS-1), random.randint(0,ROWS-1)),
            "weight": random.choice([1,2,3]),
            "time": time.time()
        }

    def spawn_poison(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_power(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    # ---------------- MOVEMENT CONTROL ----------------
    def can_move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move_time >= self.move_delay:
            self.last_move_time = now
            return True
        return False

    # ---------------- UPDATE ----------------
    def update(self):
        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        self.snake.insert(0, head)

        # collisions
        if (head in self.snake[1:] or
            head[0] < 0 or head[1] < 0 or
            head[0] >= ROWS or head[1] >= ROWS):
            return "game_over"

        # food
        if head == self.food["pos"]:
            self.score += self.food["weight"]
            self.food = self.spawn_food()
            self.food_eaten += 1
        else:
            self.snake.pop()

        # poison
        if head == self.poison:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.poison = self.spawn_poison()
            if len(self.snake) <= 1:
                return "game_over"

        # level up
        if self.food_eaten and self.food_eaten % 5 == 0:
            self.level += 1
            self.move_delay = max(60, 150 - self.level * 5)

        return "running"

    # ---------------- INPUT ----------------
    def set_direction(self, d):
        if d == (0,-1) and self.direction != (0,1):
            self.direction = d
        elif d == (0,1) and self.direction != (0,-1):
            self.direction = d
        elif d == (-1,0) and self.direction != (1,0):
            self.direction = d
        elif d == (1,0) and self.direction != (-1,0):
            self.direction = d

    # ---------------- DRAW ----------------
    def draw(self, screen, color):
        for s in self.snake:
            pygame.draw.rect(screen, color,
                (s[0]*CELL, s[1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, RED,
            (self.food["pos"][0]*CELL, self.food["pos"][1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, DARK_RED,
            (self.poison[0]*CELL, self.poison[1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, CYAN,
            (self.power[0]*CELL, self.power[1]*CELL, CELL, CELL))