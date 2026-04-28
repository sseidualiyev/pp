import pygame
import random
import time

WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = WIDTH // CELL

RED = (255,0,0)
DARK_RED = (120,0,0)
ORANGE = (255,165,0)
CYAN = (0,255,255)
GREEN = (0,255,0)
GRAY = (130,130,130)

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

        self.power = None
        self.power_type = None
        self.power_spawn_time = 0
        self.power_end_time = 0

        self.shield = False

        self.obstacles = []

        self.move_delay = 150
        self.last_move = pygame.time.get_ticks()

    # ---------------- SPAWN ----------------
    def spawn_food(self):
        return {
            "pos": (random.randint(0,ROWS-1), random.randint(0,ROWS-1)),
            "size": random.randint(1,3)
        }

    def spawn_poison(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_power(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_obstacles(self):
        if self.level < 3:
            return []

        obs = []
        snake_set = set(self.snake)

        for _ in range(self.level * 5):
            while True:
                p = (random.randint(0,ROWS-1), random.randint(0,ROWS-1))
                if p not in snake_set:
                    obs.append(p)
                    break
        return obs

    # ---------------- MOVEMENT ----------------
    def can_move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_delay:
            self.last_move = now
            return True
        return False

    # ---------------- LEVEL SYSTEM ----------------
    def update_level(self):
        if self.score >= 20:
            self.level = 2
        if self.score >= 50:
            self.level = 3
            self.obstacles = self.spawn_obstacles()

    # ---------------- UPDATE ----------------
    def update(self):

        self.update_level()

        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        # ---------------- COLLISION ----------------
        if head in self.snake[1:] or head in self.obstacles:
            if self.shield:
                self.shield = False
            else:
                return "game_over"

        if head[0] < 0 or head[1] < 0 or head[0] >= ROWS or head[1] >= ROWS:
            if self.shield:
                self.shield = False
            else:
                return "game_over"

        self.snake.insert(0, head)

        # ---------------- FOOD ----------------
        if head == self.food["pos"]:
            self.score += self.food["size"]
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # ---------------- POISON (FIXED) ----------------
        if head == self.poison:
            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()

            self.poison = self.spawn_poison()

            if len(self.snake) <= 1:
                return "game_over"

        # ---------------- POWER SPAWN ----------------
        if self.power is None:
            if random.randint(1,120) == 1:
                self.power = self.spawn_power()
                self.power_type = random.choice(["speed","slow","shield"])
                self.power_spawn_time = pygame.time.get_ticks()

        # expire power
        if self.power and pygame.time.get_ticks() - self.power_spawn_time > 8000:
            self.power = None
            self.power_type = None

        # ---------------- PICK POWER ----------------
        if self.power and head == self.power:

            now = pygame.time.get_ticks()

            if self.power_type == "speed":
                self.move_delay = 70
                self.power_end_time = now + 5000

            elif self.power_type == "slow":
                self.move_delay = 250
                self.power_end_time = now + 5000

            elif self.power_type == "shield":
                self.shield = True

            self.power = None

        # reset timed effects
        if self.power_end_time and pygame.time.get_ticks() > self.power_end_time:
            self.move_delay = 150
            self.power_end_time = 0

        return "running"

    # ---------------- INPUT ----------------
    def set_direction(self, d):
        if d == (0,-1) and self.direction != (0,1): self.direction = d
        if d == (0,1) and self.direction != (0,-1): self.direction = d
        if d == (-1,0) and self.direction != (1,0): self.direction = d
        if d == (1,0) and self.direction != (-1,0): self.direction = d

    # ---------------- DRAW ----------------
    def draw(self, screen, color, grid=False):

        if grid:
            for x in range(ROWS):
                for y in range(ROWS):
                    pygame.draw.rect(screen,(25,25,25),
                        (x*CELL,y*CELL,CELL,CELL),1)

        for s in self.snake:
            pygame.draw.rect(screen, color,
                (s[0]*CELL,s[1]*CELL,CELL,CELL))

        # FOOD (variable size)
        size = self.food["size"] * CELL
        pygame.draw.rect(screen, RED,
            (self.food["pos"][0]*CELL,self.food["pos"][1]*CELL,size,size))

        # POISON
        pygame.draw.rect(screen, DARK_RED,
            (self.poison[0]*CELL,self.poison[1]*CELL,CELL,CELL))

        # POWER
        if self.power:
            col = ORANGE if self.power_type=="speed" else CYAN if self.power_type=="slow" else GREEN
            pygame.draw.rect(screen, col,
                (self.power[0]*CELL,self.power[1]*CELL,CELL,CELL))

        # OBSTACLES
        for o in self.obstacles:
            pygame.draw.rect(screen, GRAY,
                (o[0]*CELL,o[1]*CELL,CELL,CELL))