import pygame
import tools


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    tool = "brush"
    color = (0, 0, 255)

    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None

    # TEXT
    typing = False
    text = ""
    text_pos = None
    font = pygame.font.SysFont("Arial", 24)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # =========================
            # KEYBOARD
            # =========================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                # TOOLS
                elif event.key == pygame.K_q:
                    tool = "brush"
                elif event.key == pygame.K_w:
                    tool = "line"
                elif event.key == pygame.K_e:
                    tool = "rectangle"
                elif event.key == pygame.K_r:
                    tool = "circle"
                elif event.key == pygame.K_t:
                    tool = "square"
                elif event.key == pygame.K_y:
                    tool = "rtriangle"
                elif event.key == pygame.K_u:
                    tool = "etriangle"
                elif event.key == pygame.K_i:
                    tool = "rhombus"
                elif event.key == pygame.K_o:
                    tool = "fill"
                elif event.key == pygame.K_p:
                    tool = "text"
                elif event.key == pygame.K_l:
                    tool = "eraser"

                # BRUSH SIZE
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                # COLORS
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

                # SAVE
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    tools.save_canvas(canvas)

                # TEXT INPUT
                if typing:
                    if event.key == pygame.K_RETURN:
                        tools.render_text(canvas, text, font, color, text_pos)
                        typing = False
                        text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    else:
                        text += event.unicode

            # =========================
            # MOUSE DOWN
            # =========================
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                    # FLOOD FILL
                    if tool == "fill":
                        target = canvas.get_at(event.pos)
                        tools.flood_fill(canvas, event.pos[0], event.pos[1], target, color)

                    # TEXT
                    elif tool == "text":
                        text_pos = event.pos
                        typing = True
                        text = ""

            # =========================
            # MOUSE UP
            # =========================
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1 and drawing:

                    end_pos = event.pos

                    # SHAPES
                    if tool == "line":
                        tools.draw_line(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "rectangle":
                        tools.draw_rectangle(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "circle":
                        tools.draw_circle(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "square":
                        tools.draw_square(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "rtriangle":
                        tools.draw_rtriangle(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "etriangle":
                        tools.draw_etriangle(canvas, color, start_pos, end_pos, brush_size)

                    elif tool == "rhombus":
                        tools.draw_rhombus(canvas, color, start_pos, end_pos, brush_size)

                    preview_pos = None
                    drawing = False

            # =========================
            # MOUSE MOVE
            # =========================
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    preview_pos = event.pos
                    if tool == "brush":
                        tools.draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                        last_pos = event.pos

                    if tool == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, brush_size)

        # =========================
        # DRAW
        # =========================
        screen.blit(canvas, (0, 0))

        if drawing and preview_pos is not None:

            if tool == "line":
                pygame.draw.line(screen, color, start_pos, preview_pos, brush_size)

            elif tool == "rectangle":
                rect = pygame.Rect(
                    start_pos[0],
                    start_pos[1],
                    preview_pos[0] - start_pos[0],
                    preview_pos[1] - start_pos[1]
                )
                pygame.draw.rect(screen, color, rect, brush_size)

            elif tool == "circle":
                dx = preview_pos[0] - start_pos[0]
                dy = preview_pos[1] - start_pos[1]
                radius = int((dx*2 + dy*2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, brush_size)

            elif tool == "square":
                size = min(abs(preview_pos[0]-start_pos[0]),
                        abs(preview_pos[1]-start_pos[1]))
                rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                pygame.draw.rect(screen, color, rect, brush_size)

            elif tool == "rtriangle":
                points = [start_pos, (preview_pos[0], start_pos[1]), preview_pos]
                pygame.draw.polygon(screen, color, points, brush_size)

            elif tool == "etriangle":
                x1, y1 = start_pos
                x2, y2 = preview_pos
                base_mid = ((x1 + x2)//2, y1)
                height = abs(x2 - x1) * (3 ** 0.5) / 2
                top = (base_mid[0], int(y1 - height))
                pygame.draw.polygon(screen, color, [start_pos, preview_pos, top], brush_size)

            elif tool == "rhombus":
                x1, y1 = start_pos
                x2, y2 = preview_pos
                cx = (x1 + x2)//2
                cy = (y1 + y2)//2
                points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                pygame.draw.polygon(screen, color, points, brush_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()