import pygame
from datetime import datetime


# =========================
# FREEHAND (PENCIL)
# =========================
def draw_pencil(surface, color, last_pos, current_pos, size):
    pygame.draw.line(surface, color, last_pos, current_pos, size)


