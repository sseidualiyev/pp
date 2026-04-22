import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Load assets 
background = pygame.image.load("AnimatedStreet.png").convert()
player_img = pygame.image.load("Player.png").convert_alpha()
enemy_img = pygame.image.load("Enemy.png").convert_alpha()
coin_img = pygame.image.load("coin.png").convert_alpha()
crash_sound = pygame.mixer.Sound("crash.wav")

# Resize images
player_img = pygame.transform.scale(player_img, (60, 100))
enemy_img = pygame.transform.scale(enemy_img, (60, 100))

# Coin sizes depend on weight 

# Font
font = pygame.font.SysFont("Verdana", 25)

# Game variables
ENEMY_SPEED = 5
SPEED = 5
COINS = 0
PLAYER_SPEED = 6

# Player setup
player = player_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-120))

# Enemy setup
enemy = enemy_img.get_rect(center=(random.randint(40, SCREEN_WIDTH-40), -100))

# Coin class with weight
class Coin:
    def __init__(self):
        self.reset()

    def reset(self):
        # Random X position
        self.x = random.randint(40, SCREEN_WIDTH-40)
        self.y = -50

        # Weight (affects value and size)
        self.weight = random.choice([1, 2, 3])

        # Scale coin based on weight
        size = 20 + self.weight * 10
        self.image = pygame.transform.scale(coin_img, (size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.rect.move_ip(0, SPEED)

        # Respawn if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self):
        screen.blit(self.image, self.rect)

coin = Coin()

# Game loop
running = True
while running:

    # Draw background
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement 
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-PLAYER_SPEED, 0)

    if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
        player.move_ip(PLAYER_SPEED, 0)

    if keys[pygame.K_UP] and player.top > 0:
        player.move_ip(0, -PLAYER_SPEED)

    if keys[pygame.K_DOWN] and player.bottom < SCREEN_HEIGHT:
        player.move_ip(0, PLAYER_SPEED)

    # Enemy movement
    enemy.move_ip(0, ENEMY_SPEED)

    # Respawn enemy when off screen
    if enemy.top > SCREEN_HEIGHT:
        enemy.top = -100
        enemy.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    # Move coin
    coin.move()

    # Collision with coin
    if player.colliderect(coin.rect):
        COINS += coin.weight  # add weighted coins
        coin.reset()

        # Increase speed every 10 coins
        if COINS % 10 == 0:
            ENEMY_SPEED += 1

    # Collision with enemy
    if player.colliderect(enemy):
        crash_sound.play()

        pygame.time.delay(1000)
        running = False

    # Draw sprites
    screen.blit(player_img, player)
    screen.blit(enemy_img, enemy)
    coin.draw()

    # Display coin count
    coin_text = font.render(f"Coins: {COINS}", True, (0,0,0))
    screen.blit(coin_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()