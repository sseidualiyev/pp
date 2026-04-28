import pygame
import random

WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = WIDTH // CELL

RED = (255,0,0)
DARK_RED = (120,0,0)

ORANGE = (255,165,0)
CYAN = (0,255,255)
GREEN = (0,255,0)

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
        self.power_active_until = 0

        self.shield = False

        self.obstacles = []
        self.last_move = pygame.time.get_ticks()
        self.move_delay = 150

    # ---------------- SPAWN ----------------
    def spawn_food(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_poison(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_power(self):
        return (random.randint(0,ROWS-1), random.randint(0,ROWS-1))

    def spawn_obstacles(self):
        if self.level < 3:
            return []

        obs = []
        snake_set = set(self.snake)

        for _ in range(self.level * 4):
            while True:
                pos = (random.randint(0,ROWS-1), random.randint(0,ROWS-1))
                if pos not in snake_set:
                    obs.append(pos)
                    break
        return obs

    # ---------------- MOVEMENT ----------------
    def can_move(self):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_delay:
            self.last_move = now
            return True
        return False

    # ---------------- UPDATE ----------------
    def update(self):
        head = (self.snake[0][0]+self.direction[0],
                self.snake[0][1]+self.direction[1])

        # obstacle / self / wall
        if head in self.snake[1:] or head in self.obstacles:
            if self.shield:
                self.shield = False
            else:
                return "game_over"

        if head[0]<0 or head[1]<0 or head[0]>=ROWS or head[1]>=ROWS:
            if self.shield:
                self.shield = False
            else:
                return "game_over"

        self.snake.insert(0, head)

        # FOOD
        if head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            self.food_eaten += 1
        else:
            self.snake.pop()

        # LEVEL
        if self.food_eaten and self.food_eaten % 5 == 0:
            self.level += 1
            self.move_delay = max(60, self.move_delay - 10)
            self.obstacles = self.spawn_obstacles()

        # POISON
        if head == self.poison:
            for _ in range(2):
                if len(self.snake)>1:
                    self.snake.pop()
            self.poison = self.spawn_poison()

            if len(self.snake)<=1:
                return "game_over"

        # POWERUP EXPIRY
        now = pygame.time.get_ticks()

        if self.power and now - self.power_spawn_time > 8000:
            self.power = None
            self.power_type = None

        if self.power_type in ["speed","slow"] and now > self.power_active_until:
            self.move_delay = 150 - self.level*5
            self.power_type = None

        # POWERUP PICKUP
        if self.power and head == self.power:

            self.power_type = random.choice(["speed","slow","shield"])

            if self.power_type == "speed":
                self.move_delay = max(40, self.move_delay - 60)
                self.power_active_until = now + 5000

            elif self.power_type == "slow":
                self.move_delay += 60
                self.power_active_until = now + 5000

            elif self.power_type == "shield":
                self.shield = True

            self.power = None

        return "running"

    # ---------------- INPUT ----------------
    def set_direction(self, d):
        if d==(0,-1) and self.direction!=(0,1):
            self.direction=d
        elif d==(0,1) and self.direction!=(0,-1):
            self.direction=d
        elif d==(-1,0) and self.direction!=(1,0):
            self.direction=d
        elif d==(1,0) and self.direction!=(-1,0):
            self.direction=d

    # ---------------- DRAW ----------------
    def draw(self, screen, color, grid=False):

        if grid:
            for x in range(ROWS):
                for y in range(ROWS):
                    pygame.draw.rect(screen, (20,20,20),
                        (x*CELL,y*CELL,CELL,CELL),1)

        for s in self.snake:
            pygame.draw.rect(screen, color,
                (s[0]*CELL,s[1]*CELL,CELL,CELL))

        pygame.draw.rect(screen, RED,
            (self.food[0]*CELL,self.food[1]*CELL,CELL,CELL))

        pygame.draw.rect(screen, DARK_RED,
            (self.poison[0]*CELL,self.poison[1]*CELL,CELL,CELL))

        if self.power:
            col = ORANGE if self.power_type=="speed" else CYAN if self.power_type=="slow" else GREEN
            pygame.draw.rect(screen, col,
                (self.power[0]*CELL,self.power[1]*CELL,CELL,CELL))

        for o in self.obstacles:
            pygame.draw.rect(screen, (120,120,120),
                (o[0]*CELL,o[1]*CELL,CELL,CELL))