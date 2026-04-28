import pygame
import tools


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    # STATE
    tool = "brush"
    color = (0, 0, 255)

    brush_size = 5
    eraser_size = 15

    drawing = False
    start_pos = None
    last_pos = None

    # TEXT
    typing = False
    text = ""
    text_pos = None
    font = pygame.font.SysFont("Arial", 24)

    