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

