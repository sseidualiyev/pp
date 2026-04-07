import pygame

class Ball:
    def __init__(self, width, height):
        self.radius = 25
        self.x = width // 2
        self.y = height // 2
        self.step = 20
        self.width = width
        self.height = height

    def move(self, keys):
        if keys[pygame.K_UP]:
            if self.y - self.step - self.radius >= 0:
                self.y -= self.step

        if keys[pygame.K_DOWN]:
            if self.y + self.step + self.radius <= self.height:
                self.y += self.step

        if keys[pygame.K_LEFT]:
            if self.x - self.step - self.radius >= 0:
                self.x -= self.step

        if keys[pygame.K_RIGHT]:
            if self.x + self.step + self.radius <= self.width:
                self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)