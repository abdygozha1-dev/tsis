import pygame
import sys
import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

color = BLACK

clock = pygame.time.Clock()
tool = "pencil"
drawing = False
start_pos = None
prev_pos = None

brush_size = 2

font = pygame.font.SysFont("Arial", 24)
typing = False
text = ""
text_pos = (0, 0)

def flood_fill(surface, x, y, target_color, replacement_color):
    if target_color == replacement_color:
        return

    width, height = surface.get_size()
    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), replacement_color)

        queue.append((x+1, y))
        queue.append((x-1, y))
        queue.append((x, y+1))
        queue.append((x, y-1))

def save_canvas():
    filename = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)

running = True

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

            if event.key == pygame.K_p:
                tool = "pencil"
            if event.key == pygame.K_l:
                tool = "line"
            if event.key == pygame.K_f:
                tool = "fill"
            if event.key == pygame.K_t:
                tool = "text"

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text, True, color)
                    canvas.blit(img, text_pos)
                    typing = False
                    text = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text = ""

                else:
                    text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "pencil":
                drawing = True
                prev_pos = event.pos

            elif tool == "line":
                start_pos = event.pos
                drawing = True

            elif tool == "fill":
                x, y = event.pos
                target = canvas.get_at((x, y))
                flood_fill(canvas, x, y, target, color)

            elif tool == "text":
                text_pos = event.pos
                typing = True
                text = ""

        if event.type == pygame.MOUSEBUTTONUP:
            if tool == "pencil":
                drawing = False

            elif tool == "line":
                end_pos = event.pos
                pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)
                drawing = False

        if event.type == pygame.MOUSEMOTION:
            if tool == "pencil" and drawing:
                pygame.draw.line(canvas, color, prev_pos, event.pos, brush_size)
                prev_pos = event.pos

    if typing:
        screen.blit(font.render(text, True, color), text_pos)

    info = [
        "P-pencil L-line F-fill T-text",
        "1-2-3 brush size",
        "Ctrl+S save"
    ]

    y = 10
    for i in info:
        screen.blit(font.render(i, True, (50, 50, 50)), (10, y))
        y += 25

    pygame.display.update()
    clock.tick(120)

pygame.quit()
sys.exit()