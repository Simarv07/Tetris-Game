# Define a class for the Tetris game pieces
import pygame


class Piece:
    def __init__(self, shape, board):
        self.board = board
        self.shape = shape
        self.x = board.board_width // 2 - len(shape[0]) // 2
        self.y = 0

    # Moves the piece given the change in x and y
    def move(self, dx, dy):
        # Check bounds of the screen and move then move the piece
        if self.check_bounds(dx) and self.board.game_over is False:

            # Delete previous instance of the piece
            self.delete_shape()

            # Update the position of the piece
            self.y += dy
            self.x += dx

            # Check if it collides with another piece
            if self.check_move():
                self.update_shape(self.board.grid)
                return True
            else:
                self.y -= dy
                self.x -= dx
                self.update_shape(self.board.grid)
                self.board.check_rows()
                return False

    # Checks if the current state of the piece is valid
    def check_move(self):
        for y in range(0, len(self.shape)):
            for x in range(0, len(self.shape[y])):
                if self.y + y > 19:
                    return False
                if self.board.grid[self.y + y][self.x + x] != 0 \
                        and self.shape[y][x] != 0:
                    return False
        return True

    # Checks if the piece is within the bounds of the screen
    def check_bounds(self, dx=0):
        for y in range(0, len(self.shape)):
            for x in range(0, len(self.shape[y])):
                if 9 < self.x + x + dx or self.x + dx < 0:
                    if self.shape[y][x] != 0:
                        return False
        return True

    # Rotates the piece
    def rotate_shape(self):
        # Delete previous instance of the piece
        self.delete_shape()

        # Transpose the shape
        old_shape = self.shape
        rotated_shape = list(map(list, zip(*self.shape)))
        # Reverse each row to flip it horizontally
        rotated_shape = [list(reversed(row)) for row in rotated_shape]
        self.shape = rotated_shape

        try:
            demo_grid = [row.copy() for row in self.board.grid]
            self.update_shape(demo_grid)
        except IndexError:
            self.shape = old_shape
        finally:
            if self.check_move():
                self.update_shape(self.board.grid)
            else:
                self.shape = old_shape
                self.update_shape(self.board.grid)

    # Updates the grid with the current instance of the piece
    def update_shape(self, grid):
        for y in range(0, len(self.shape)):
            for x in range(0, len(self.shape[y])):
                if self.shape[y][x] != 0:
                    grid[self.y + y][self.x + x] = self.shape[y][x]

    # Deletes the current instance of the piece
    def delete_shape(self):
        for y in range(0, len(self.shape)):
            for x in range(0, len(self.shape[y])):
                if self.shape[y][x] != 0:
                    self.board.grid[self.y + y][self.x + x] = 0