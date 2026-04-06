import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.center = (width // 2, height // 2)

        self.bg = pygame.image.load("images/mickeyclock.png").convert()
        self.bg = pygame.transform.scale(self.bg, (width, height))

        self.left_hand = pygame.image.load("images/mickey_hand2.png").convert_alpha()
        self.right_hand = pygame.image.load("images/mickey_hand1.png").convert_alpha()

        self.left_hand = pygame.transform.scale(self.left_hand, (20, 150))
        self.right_hand = pygame.transform.scale(self.right_hand, (20, 150))

    def get_angles(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = -(minutes * 6) 
        second_angle = -(seconds * 6)

        return minute_angle, second_angle

    def draw_hand(self, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

    def update(self):
        self.minute_angle, self.second_angle = self.get_angles()

    def draw(self):

    self.screen.blit(self.bg, (0, 0))

    self.draw_hand(self.right_hand, self.minute_angle)

    self.draw_hand(self.left_hand, self.second_angle)