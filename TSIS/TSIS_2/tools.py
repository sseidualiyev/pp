import pygame
from datetime import datetime


# =========================
# FREEHAND (PENCIL)
# =========================
def draw_pencil(surface, color, last_pos, current_pos, size):
    pygame.draw.line(surface, color, last_pos, current_pos, size)


# =========================
# LINE TOOL
# =========================
def draw_line(surface, color, start_pos, end_pos, size):
    pygame.draw.line(surface, color, start_pos, end_pos, size)


# =========================
# FLOOD FILL
# =========================
def flood_fill(surface, x, y, target_color, replacement_color):
    if target_color == replacement_color:
        return

    width, height = surface.get_size()
    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()

        if cx < 0 or cy < 0 or cx >= width or cy >= height:
            continue

        if surface.get_at((cx, cy)) != target_color:
            continue

        surface.set_at((cx, cy), replacement_color)

        stack.append((cx+1, cy))
        stack.append((cx-1, cy))
        stack.append((cx, cy+1))
        stack.append((cx, cy-1))


