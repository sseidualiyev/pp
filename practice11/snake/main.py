import pygame, random, time

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Snake
snake = [(5,5)]
direction = (1,0)

# Food with weight + timer
class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.pos = (random.randint(0,29), random.randint(0,29))
        self.weight = random.choice([1,2,3])
        self.spawn_time = time.time()

    def expired(self):
        return time.time() - self.spawn_time > 5  # disappears after 5 sec

food = Food()
score = 0

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: direction=(0,-1)
            if event.key == pygame.K_DOWN: direction=(0,1)
            if event.key == pygame.K_LEFT: direction=(-1,0)
            if event.key == pygame.K_RIGHT: direction=(1,0)

    # Move snake
    head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
    snake.insert(0, head)

    # Food eaten
    if head == food.pos:
        score += food.weight
        food.spawn()
    else:
        snake.pop()

    # Food disappears
    if food.expired():
        food.spawn()

    # Collision with wall
    if head[0] < 0 or head[0] >= 30 or head[1] < 0 or head[1] >= 30:
        running = False

    # Draw snake
    for s in snake:
        pygame.draw.rect(screen, (0,255,0), (s[0]*CELL, s[1]*CELL, CELL, CELL))

    # Draw food (size depends on weight)
    pygame.draw.rect(screen, (255,0,0),
        (food.pos[0]*CELL, food.pos[1]*CELL, CELL + food.weight*5, CELL + food.weight*5))

    # Score
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()