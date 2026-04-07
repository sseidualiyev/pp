import pygame
import sys
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)

player = MusicPlayer("music/")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill((30, 30, 30))

    text = font.render(f"Track: {player.get_current_track_name()}", True, (255, 255, 255))
    screen.blit(text, (20, 100))

    pygame.display.flip()
    clock.tick(30)