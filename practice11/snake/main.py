import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
ROWS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self, snake):
        self.position = self.random_position(snake)

    def random_position(self, snake):
        while True:
            pos = (random.randint(0, ROWS-1), random.randint(0, ROWS-1))
            if pos not in snake.body:
                return pos

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to show Game Over screen with restart option
def game_over_screen():
    while True:
        screen.fill(BLACK)

        game_over_text = big_font.render("Game Over", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(restart_text, (WIDTH//2 - 110, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - 100, HEIGHT//2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main game loop wrapped in function for restarting
def game_loop():
    snake = Snake()
    food = Food(snake)
    score = 0
    level = 1
    speed = 10

    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)

        snake.move()
        head = snake.body[0]

        # Border collision
        if head[0] < 0 or head[0] >= ROWS or head[1] < 0 or head[1] >= ROWS:
            return  # End game loop

        # Self collision
        if head in snake.body[1:]:
            return

        # Food collision
        if head == food.position:
            snake.grow = True
            score += 1
            food = Food(snake)

            if score % 4 == 0:
                level += 1
                speed += 2

        snake.draw()
        food.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.update()
        clock.tick(speed)

# Main control loop (handles restart)
while True:
    game_loop()
    restart = game_over_screen()
    if not restart:
        break

pygame.quit()