import pygame, random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

# Game variables
SPEED = 5
COINS = 0

# Player
player = pygame.Rect(250, 700, 50, 80)

# Enemy
enemy = pygame.Rect(random.randint(0, WIDTH-50), 0, 50, 80)

# Coin class (with weight)
class Coin:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH-30)
        self.y = 0
        self.weight = random.choice([1, 2, 3])  # different weights
        self.size = 15 + self.weight * 5

    def move(self):
        self.y += SPEED

        if self.y > HEIGHT:
            self.reset()

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)

coin = Coin()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.x < WIDTH-50:
        player.x += 5

    # Enemy movement
    enemy.y += SPEED
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(0, WIDTH-50)

    # Coin movement
    coin.move()

    # Collision with coin
    if player.collidepoint(coin.x, coin.y):
        COINS += coin.weight  # add weighted coins
        coin.reset()

        # Increase enemy speed every 10 coins
        if COINS % 10 == 0:
            SPEED += 1

    # Collision with enemy
    if player.colliderect(enemy):
        running = False

    # Draw objects
    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, (0,0,255), enemy)
    coin.draw()

    # Display coins
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Coins: {COINS}", True, (0,0,0))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()