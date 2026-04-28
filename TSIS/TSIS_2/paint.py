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

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # =========================
            # KEY CONTROLS
            # =========================
            if event.type == pygame.KEYDOWN:

                # EXIT
                if event.key == pygame.K_ESCAPE:
                    if typing:
                        typing = False
                        text = ""
                    else:
                        running = False

                # TOOLS
                if event.key == pygame.K_1:
                    tool = "brush"
                elif event.key == pygame.K_2:
                    tool = "line"
                elif event.key == pygame.K_3:
                    tool = "eraser"
                elif event.key == pygame.K_4:
                    tool = "fill"
                elif event.key == pygame.K_5:
                    tool = "text"

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

                    # TEXT TOOL
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

                    if tool == "line":
                        tools.draw_line(canvas, color, start_pos, end_pos, brush_size)

                    drawing = False

            # =========================
            # MOUSE MOVE
            # =========================
            if event.type == pygame.MOUSEMOTION:

                if drawing:

                    if tool == "brush":
                        tools.draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                        last_pos = event.pos

                    elif tool == "eraser":
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, eraser_size)

        # =========================
        # RENDER
        # =========================
        screen.blit(canvas, (0, 0))

        # LINE PREVIEW
        if drawing and tool == "line":
            pygame.draw.line(screen, color, start_pos, pygame.mouse.get_pos(), brush_size)

        # TEXT PREVIEW
        if typing:
            preview = font.render(text, True, color)
            screen.blit(preview, text_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()