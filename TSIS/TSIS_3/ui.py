import pygame

class UI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(img, (x, y))

    # ---------------- MENU ----------------
    def main_menu(self):
        self.screen.fill((200, 200, 200))
        self.draw_text("RACER GAME", 150, 200)
        self.draw_text("1. Play", 180, 300)
        self.draw_text("2. Leaderboard", 180, 350)
        self.draw_text("3. Settings", 180, 400)
        self.draw_text("4. Quit", 180, 450)
        pygame.display.update()

    # ---------------- GAME OVER ----------------
    def game_over(self, score, distance):
        self.screen.fill((255, 200, 200))
        self.draw_text("GAME OVER", 150, 200)
        self.draw_text(f"Score: {score}", 150, 300)
        self.draw_text(f"Distance: {distance}", 150, 350)
        self.draw_text("Press R to Retry", 120, 450)
        pygame.display.update()