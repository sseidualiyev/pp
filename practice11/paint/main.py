import pygame, math

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Paint")

canvas = pygame.Surface(screen.get_size())
canvas.fill((255,255,255))

color = (0,0,0)
tool = 'brush'
start_pos = None
drawing = False

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: tool='brush'
            if event.key == pygame.K_2: tool='square'
            if event.key == pygame.K_3: tool='rtriangle'
            if event.key == pygame.K_4: tool='etriangle'
            if event.key == pygame.K_5: tool='rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end = event.pos

            # Square
            if tool == 'square':
                size = min(abs(end[0]-start_pos[0]), abs(end[1]-start_pos[1]))
                pygame.draw.rect(canvas, color, (*start_pos, size, size), 2)

            # Right triangle
            elif tool == 'rtriangle':
                pygame.draw.polygon(canvas, color, [start_pos, end, (start_pos[0], end[1])], 2)

            # Equilateral triangle
            elif tool == 'etriangle':
                x1,y1 = start_pos
                x2,y2 = end
                third = ((x1+x2)//2, y1 - abs(x2-x1)//2)
                pygame.draw.polygon(canvas, color, [start_pos, end, third], 2)

            # Rhombus
            elif tool == 'rhombus':
                x1,y1 = start_pos
                x2,y2 = end
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                pygame.draw.polygon(canvas, color, [(cx,y1),(x2,cy),(cx,y2),(x1,cy)], 2)

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == 'brush':
                pygame.draw.circle(canvas, color, event.pos, 3)

    screen.blit(canvas,(0,0))
    pygame.display.flip()
    clock.tick(60)