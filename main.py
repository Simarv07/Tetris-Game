import time
import database
import pygame
import random

from Board import Board
from Piece import Piece

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
PADDING = 160
HOLD_SLEEP_TIME = 0.1
INTREVAL_TIME = 1000

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
pieces[0].update_shape(board.grid)

# Main game loop
game_over = False
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, INTREVAL_TIME)


def replace_current_piece():
    pieces[0], pieces[1] = pieces[1], Piece(random.choice(shapes),
                                            board)
    current_piece = pieces[0]
    board.next_piece = pieces[1]
    # Check if the piece overrides any other pieces, if so, game over
    if not current_piece.check_move():
        board.game_over = True
    current_piece.update_shape(board.grid)
    board.hold_piece_used = False


def hold_piece():
    current_piece = pieces[0]
    current_piece.delete_shape()
    if board.hold_piece is not None and board.hold_piece_used is False:
        current_piece.y = 0
        current_piece.x = board.board_width // 2 - len(current_piece.shape[0]) // 2
        pieces[0] = board.hold_piece
        board.hold_piece = current_piece
        pieces[0].update_shape(board.grid)
        board.hold_piece_used = True
    elif board.hold_piece is None and board.hold_piece_used is False:
        current_piece.y = 0
        current_piece.x = board.board_width // 2 - len(current_piece.shape[0]) // 2
        board.hold_piece = current_piece
        replace_current_piece()
        board.hold_piece_used = True
    else:
        current_piece.update_shape(board.grid)


def handle_key_presses():
    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Handles key presses
    if keys[pygame.K_DOWN]:
        # Moves the current piece down and if collision occurs
        # places the piece and creates a new one
        if not current_piece.move(0, 1):
            replace_current_piece()

        # Resets the timer event
        pygame.time.set_timer(timer_event, INTREVAL_TIME)
        time.sleep(HOLD_SLEEP_TIME)
    if keys[pygame.K_LEFT]:
        # Moves the current piece left
        current_piece.move(-1, 0)
        time.sleep(HOLD_SLEEP_TIME)
    if keys[pygame.K_RIGHT]:
        # Moves the current piece right
        current_piece.move(1, 0)
        time.sleep(HOLD_SLEEP_TIME)


def insert_score(score):
    leaderboard = database.return_top_ten_scores()
    if score > leaderboard[-1]:
        database.insert_new_score(board.score)
        return True
    else:
        return False


# Main Game loop
while not game_over:
    current_piece = pieces[0]
    board.next_piece = pieces[1]

    if not board.game_over:
        handle_key_presses()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # Handles the timer where a block will be moved down every second
            if event.type == timer_event:
                if not current_piece.move(0, 1):
                    replace_current_piece()
                if INTREVAL_TIME > 100:
                    INTREVAL_TIME -= 5
            elif event.type == pygame.KEYDOWN:
                # Rotate the current piece
                if event.key == pygame.K_UP:
                    current_piece.rotate_shape()
                if event.key == pygame.K_c:
                    hold_piece()
                if event.key == pygame.K_SPACE:
                    while current_piece.move(0, 1):
                        pass
                    replace_current_piece()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                insert_score(board.score)
                game_over = True

    board.draw(screen)

    # Set the speed of the game
    clock.tick(60)

    # Update the display
    pygame.display.update()
