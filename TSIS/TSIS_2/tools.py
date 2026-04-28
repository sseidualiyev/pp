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


# =========================
# SQUARE
# =========================
def draw_square(surface, color, start, end, size):
    side = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], side, side)
    pygame.draw.rect(surface, color, rect, size)


# =========================
# RIGHT TRIANGLE
# =========================
def draw_rtriangle(surface, color, start, end, size):
    points = [start, (end[0], start[1]), end]
    pygame.draw.polygon(surface, color, points, size)


# =========================
# EQUILATERAL TRIANGLE
# =========================
def draw_etriangle(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    base_mid = ((x1 + x2)//2, y1)
    height = abs(x2 - x1) * (3 ** 0.5) / 2
    top = (base_mid[0], int(y1 - height))

    pygame.draw.polygon(surface, color, [start, end, top], size)


# =========================
# RHOMBUS
# =========================
def draw_rhombus(surface, color, start, end, size):
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2)//2
    cy = (y1 + y2)//2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    pygame.draw.polygon(surface, color, points, size)

