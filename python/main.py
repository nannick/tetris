#!/usr/bin/env python3
import pygame
from tetris import *
from constants import COLOURS, BLACK, X, Y, IN_PLAY, ANIT_CLOCKWISE, FLIP, CLOCKWISE

if __name__ == "__main__":

    pygame.init()

    num_rows = 20
    num_columns = 15

    pixel_size = 40

    display = pygame.display.set_mode((
        pixel_size * num_columns, pixel_size * num_rows))

    done = False

    tetris = Tetris(num_rows, num_columns)
    tetris.assign_new_piece([num_columns >> 1, num_rows - 1], [[0, 0]])

    MOVE_DOWN = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_DOWN, 1000)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
            if event.type == MOVE_DOWN:
                tetris.move_piece_down()

                if tetris.need_new_piece:

                    # Is temporary once machine learning model is created, generator will create the pieces
                    # Make another algo to put it in a default position
                    tetris.assign_new_piece(
                        [num_columns >> 1, num_rows - 1], [[0, 0], [1, 0], [2, 0], [0, 1])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    tetris.rotate_piece(ANIT_CLOCKWISE)
                if event.key == pygame.K_2:
                    tetris.rotate_piece(FLIP)
                if event.key == pygame.K_3:
                    tetris.rotate_piece(CLOCKWISE)
                if event.key == pygame.K_DOWN:
                    tetris.move_piece_down()
                if event.key == pygame.K_RIGHT:
                    tetris.move_piece_side(1)
                if event.key == pygame.K_LEFT:
                    tetris.move_piece_side(-1)

        display.fill(COLOURS[BLACK])

        if not tetris.game_over:

            for r in range(num_rows):
                row_pos = (num_rows - r - 1) * pixel_size
                row = tetris.board[r]
                for c in range(num_columns):
                    col_pos = c * pixel_size

                    colour = COLOURS[row[c]]

                    pygame.draw.rect(display, colour, [
                        col_pos, row_pos, pixel_size, pixel_size])

            origin_x = tetris.rotation_point[X]
            origin_y = tetris.rotation_point[Y]

            for part in tetris.piece_parts:
                new_x = origin_x + part[X]
                new_y = origin_y + part[Y]
                row_pos = (num_rows - new_y - 1) * pixel_size
                col_pos = new_x * pixel_size
                pygame.draw.rect(display, COLOURS[IN_PLAY], [
                    col_pos, row_pos, pixel_size, pixel_size])
        else:
            print("Game over loser")
            # Restart game here

        pygame.display.update()
