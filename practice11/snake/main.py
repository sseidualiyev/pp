import pygame
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = WIDTH // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

# Snake setup
snake = [(5,5), (4,5), (3,5)]  # initial body
direction = (1,0)  # moving right

# Food with weight + timer
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.pos = (random.randint(0, ROWS-1), random.randint(0, ROWS-1))
        self.weight = random.choice([1,2,3])
        self.spawn_time = time.time()

    def expired(self):
        return time.time() - self.spawn_time > 5  # disappears after 5 sec

food = Food()
score = 0

running = True
while running:
    screen.fill(BLACK)

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and direction != (0,1):
                direction = (0,-1)
            elif event.key == pygame.K_DOWN and direction != (0,-1):
                direction = (0,1)
            elif event.key == pygame.K_LEFT and direction != (1,0):
                direction = (-1,0)
            elif event.key == pygame.K_RIGHT and direction != (-1,0):
                direction = (1,0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)  # add new head

    if head == food.pos:
        score += food.weight  
        food.spawn()
    else:
        snake.pop()  

    if food.expired():
        food.spawn()


    if head[0] < 0 or head[0] >= ROWS or head[1] < 0 or head[1] >= ROWS:
        running = False

    if head in snake[1:]:
        running = False

    for segment in snake:
        pygame.draw.rect(screen, GREEN,
                         (segment[0]*CELL, segment[1]*CELL, CELL, CELL))

    size = CELL + food.weight * 5
    pygame.draw.rect(screen, RED,
                     (food.pos[0]*CELL, food.pos[1]*CELL, size, size))

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()