import pygame
import random
import time

WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = WIDTH // CELL

BLACK = (0,0,0)
RED = (255,0,0)
DARK_RED = (120,0,0)
CYAN = (0,255,255)

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(5,5),(4,5),(3,5)]
        self.direction = (1,0)

        self.level = 1
        self.speed = 10
        self.score = 0
        self.food_eaten = 0

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()
        self.power = self.spawn_power()

        self.obstacles = self.generate_obstacles()

        self.power_type = None
        self.power_timer = 0

    # ---------------- FOOD ----------------
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

    def food_expired(self):
        return time.time() - self.food["time"] > 5

    # ---------------- OBSTACLES ----------------
    def generate_obstacles(self):
        if self.level < 3:
            return []
        return [(random.randint(0,ROWS-1), random.randint(0,ROWS-1))
                for _ in range(self.level * 3)]

    # ---------------- UPDATE ----------------
    def update(self):
        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        self.snake.insert(0, head)

        # wall / self / obstacle collision
        if (head in self.snake[1:] or
            head in self.obstacles or
            head[0] < 0 or head[1] < 0 or
            head[0] >= ROWS or head[1] >= ROWS):
            return "game_over"

        # FOOD
        if head == self.food["pos"]:
            self.score += self.food["weight"]
            self.food = self.spawn_food()
            self.food_eaten += 1
        else:
            self.snake.pop()

        if self.food_expired():
            self.food = self.spawn_food()

        # LEVEL UP
        if self.food_eaten and self.food_eaten % 5 == 0:
            self.level += 1
            self.speed += 2
            self.obstacles = self.generate_obstacles()

        # POISON
        if head == self.poison:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            self.poison = self.spawn_poison()

            if len(self.snake) <= 1:
                return "game_over"

        # POWERUP TIMER
        if self.power_timer and pygame.time.get_ticks() - self.power_timer > 5000:
            self.speed = 10 + self.level
            self.power_timer = 0

        # POWERUP PICKUP
        if head == self.power:
            self.power_type = random.choice(["speed","slow","shield"])
            if self.power_type == "speed":
                self.speed += 5
            elif self.power_type == "slow":
                self.speed = max(5, self.speed - 5)

            self.power_timer = pygame.time.get_ticks()
            self.power = self.spawn_power()

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
    def draw(self, screen, snake_color):
        for s in self.snake:
            pygame.draw.rect(screen, snake_color,
                (s[0]*CELL, s[1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, RED,
            (self.food["pos"][0]*CELL, self.food["pos"][1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, DARK_RED,
            (self.poison[0]*CELL, self.poison[1]*CELL, CELL, CELL))

        pygame.draw.rect(screen, CYAN,
            (self.power[0]*CELL, self.power[1]*CELL, CELL, CELL))

        for o in self.obstacles:
            pygame.draw.rect(screen, (120,120,120),
                (o[0]*CELL, o[1]*CELL, CELL, CELL))