import time

import pygame
import random

from Board import Board
from Piece import Piece

# Initialize Pygame
pygame.init()

# TODO: Add to github
# TODO: Show next shape in the corner
# TODO: Change colors to lighter colors (same as jstris)
# TODO: Have a temp storage you can swap with
# TODO: Show the highlight at the bottom (optional)

# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
PADDING = 50

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Set up the clock
clock = pygame.time.Clock()

# Define the shapes of the Tetris pieces
shapes = [
    [[1, 1, 1], [0, 1, 0]],
    [[2, 2], [2, 2]],
    [[3, 3, 0], [0, 3, 3]],
    [[0, 4, 4], [4, 4, 0]],
    [[5, 5, 5, 5]],
    [[6, 6, 6], [0, 0, 6]],
    [[7, 7, 7], [7, 0, 0]],
]

# Load the music file
pygame.mixer.music.load('Tetris.mp3')

# Play the music
pygame.mixer.music.play(-1)

# Create an instance of the Board class
board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, PADDING)

# Create a list to hold the current piece and the next piece
pieces = [Piece(random.choice(shapes), board),
          Piece(random.choice(shapes), board)]
placed_pieces = []
pieces[0].update_shape(board.grid)

# Main game loop
game_over = False
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)


def replace_current_piece(current_piece):
    pieces[0], pieces[1] = pieces[1], Piece(random.choice(shapes),
                                            board)
    placed_pieces.append(current_piece)
    current_piece = pieces[0]
    # Check if the piece overrides any other pieces, if so, game over
    if not current_piece.check_move():
        board.game_over = True
    current_piece.update_shape(board.grid)

while not game_over:
    current_piece = pieces[0]

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Handles key presses
    if keys[pygame.K_DOWN]:
        # Moves the current piece down and if collision occurs
        # places the piece and creates a new one
        if current_piece.move(0, 1) == False:
            replace_current_piece(current_piece)

        # Resets the timer event
        pygame.time.set_timer(timer_event, 1000)
        time.sleep(0.1)
    if keys[pygame.K_LEFT]:
        # Moves the current piece left
        current_piece.move(-1, 0)
        time.sleep(0.1)
    if keys[pygame.K_RIGHT]:
        # Moves the current piece right
        current_piece.move(1, 0)
        time.sleep(0.1)

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_over = True
        # Handles the timer where a block will be moved down every second
        if event.type == timer_event:
            if current_piece.move(0, 1) == False:
                replace_current_piece(current_piece)
        elif event.type == pygame.KEYDOWN:
            # Rotate the current piece
            if event.key == pygame.K_UP:
                current_piece.rotate_shape()
            if event.key == pygame.K_SPACE:
                while current_piece.move(0, 1):
                    pass
                replace_current_piece(current_piece)

    board.draw(screen)

    # Set the speed of the game
    clock.tick(60)

    # Update the display
    pygame.display.update()
