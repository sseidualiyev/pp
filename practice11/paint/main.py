import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    # Canvas (important for persistent drawing)
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    eraser_radius = 15
    radius = 5
    color = (0, 0, 255)
    tool = 'brush'

    drawing = False
    start_pos = None

    running = True
    while running:
        for event in pygame.event.get():

            # Exit conditions
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Tool selection (OLD + NEW)
                if event.key == pygame.K_1:
                    tool = 'brush'
                elif event.key == pygame.K_2:
                    tool = 'rectangle'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_4:
                    tool = 'eraser'

                # 🆕 NEW SHAPES
                elif event.key == pygame.K_5:
                    tool = 'square'
                elif event.key == pygame.K_6:
                    tool = 'rtriangle'
                elif event.key == pygame.K_7:
                    tool = 'etriangle'
                elif event.key == pygame.K_8:
                    tool = 'rhombus'

                # Color selection
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

            # Mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            # Mouse released (draw shapes permanently)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos

                    # OLD shapes
                    if tool == 'rectangle':
                        rect = pygame.Rect(
                            start_pos[0],
                            start_pos[1],
                            end_pos[0] - start_pos[0],
                            end_pos[1] - start_pos[1]
                        )
                        pygame.draw.rect(canvas, color, rect, 2)

                    elif tool == 'circle':
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        radius_circle = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, radius_circle, 2)

                    # 🆕 NEW SHAPES

                    elif tool == 'square':
                        size = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                        rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                        pygame.draw.rect(canvas, color, rect, 2)

                    elif tool == 'rtriangle':
                        points = [
                            start_pos,
                            (end_pos[0], start_pos[1]),
                            end_pos
                        ]
                        pygame.draw.polygon(canvas, color, points, 2)

                    elif tool == 'etriangle':
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        base_mid = ((x1 + x2)//2, y1)
                        height = abs(x2 - x1) * (3**0.5) / 2
                        top = (base_mid[0], int(y1 - height))
                        pygame.draw.polygon(canvas, color, [start_pos, end_pos, top], 2)

                    elif tool == 'rhombus':
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        cx = (x1 + x2)//2
                        cy = (y1 + y2)//2
                        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                        pygame.draw.polygon(canvas, color, points, 2)

                    drawing = False

            # Mouse movement (brush / eraser)
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if tool == 'brush':
                        pygame.draw.circle(canvas, color, event.pos, radius)
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, eraser_radius)

        # Draw canvas
        screen.blit(canvas, (0, 0))

        # Preview shapes (OLD + NEW)
        if drawing and tool in ['rectangle', 'circle', 'square', 'rtriangle', 'etriangle', 'rhombus']:
            current_pos = pygame.mouse.get_pos()

            if tool == 'rectangle':
                rect = pygame.Rect(start_pos[0], start_pos[1],
                                   current_pos[0]-start_pos[0],
                                   current_pos[1]-start_pos[1])
                pygame.draw.rect(screen, color, rect, 1)

            elif tool == 'circle':
                dx = current_pos[0] - start_pos[0]
                dy = current_pos[1] - start_pos[1]
                radius_circle = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_circle, 1)

            # 🆕 Preview new shapes

            elif tool == 'square':
                size = min(abs(current_pos[0]-start_pos[0]), abs(current_pos[1]-start_pos[1]))
                rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                pygame.draw.rect(screen, color, rect, 1)

            elif tool == 'rtriangle':
                points = [start_pos, (current_pos[0], start_pos[1]), current_pos]
                pygame.draw.polygon(screen, color, points, 1)

            elif tool == 'etriangle':
                x1, y1 = start_pos
                x2, y2 = current_pos
                base_mid = ((x1 + x2)//2, y1)
                height = abs(x2 - x1) * (3**0.5) / 2
                top = (base_mid[0], int(y1 - height))
                pygame.draw.polygon(screen, color, [start_pos, current_pos, top], 1)

            elif tool == 'rhombus':
                x1, y1 = start_pos
                x2, y2 = current_pos
                cx = (x1 + x2)//2
                cy = (y1 + y2)//2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(screen, color, points, 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()