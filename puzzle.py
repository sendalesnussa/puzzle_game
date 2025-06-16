import pygame
import sys
import random
import os
import time

pygame.init()

WINDOW_SIZE = 600
MAX_LEVEL = 6
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# ==== GAMBAR BOARD ====
def draw_board(board, tiles, grid_size, level, selected_pos, time_left):
    screen.fill((255, 255, 255))
    tile_size = WINDOW_SIZE // grid_size
    for y in range(grid_size):
        for x in range(grid_size):
            n = board[y][x]
            pos = (x, y)
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            screen.blit(tiles[n], rect.topleft)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if selected_pos == pos:
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)

# ==== MAIN ====
show_opening_screen()

level = 1
grid_size, tiles, board, start_time, duration = start_level(level)
running = True
win = False
selected = None

while running:
    current_time = time.time()
    time_left = duration - (current_time - start_time)

    if time_left <= 0 and not win:
        show_game_over()
        break
z
    draw_board(board, tiles, grid_size, level, selected, time_left)
    pygame.display.flip()

    if is_solved(board):
        if level < MAX_LEVEL:
            pygame.time.wait(1000)
            level += 1
            grid_size, tiles, board, start_time, duration = start_level(level)
            selected = None
        else:
            pygame.display.set_caption("🎉 Semua Level Selesai!")
            win = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not win:
            mx, my = pygame.mouse.get_pos()
            tx, ty = mx // (WINDOW_SIZE // grid_size), my // (WINDOW_SIZE // grid_size)
            if selected is None:
                selected = (tx, ty)
            else:
                if is_adjacent(selected, (tx, ty)):
                    sx, sy = selected
                    board[sy][sx], board[ty][tx] = board[ty][tx], board[sy][sx]
                    selected = None
                else:
                    selected = (tx, ty)

    clock.tick(30)

pygame.quit()
sys.exit()