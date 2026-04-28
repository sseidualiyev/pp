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


# =========================
# SAVE CANVAS
# =========================
def save_canvas(surface):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(surface, filename)
    print("Saved:", filename)


# =========================
# TEXT RENDER FINAL
# =========================
def render_text(surface, text, font, color, pos):
    img = font.render(text, True, color)
    surface.blit(img, pos)


# =========================
# RECTANGLE
# =========================
def draw_rectangle(surface, color, start, end, size):
    rect = pygame.Rect(start[0], start[1],
                       end[0] - start[0],
                       end[1] - start[1])
    pygame.draw.rect(surface, color, rect, size)


# =========================
# CIRCLE
# =========================
def draw_circle(surface, color, start, end, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    radius = int((dx*2 + dy*2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, size)


