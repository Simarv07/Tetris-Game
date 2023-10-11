# Define some colors
import pygame
import database

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colors = {
    0: (0, 0, 0),
    1: (174,41,138),
    2: (226,159,2),
    3: (89,176,1),
    4: (215,15,54),
    5: (15,155,214),
    6: (33,65,197),
    7: (226,91,2)
}


class Board:
    def __init__(self, window_width, window_height, padding):
        self.board_width = 10
        self.board_height = 20
        self.grid = [[0 for x in range(self.board_width)] for y in
                     range(self.board_height)]
        self.window_width = window_width
        self.window_height = window_height - padding
        self.window_board_width = window_width - padding
        self.window_board_height = window_height - padding
        self.padding = padding
        self.cell_size = (self.window_width - padding) // self.board_width
        self.score = 0
        self.game_over = False
        self.next_piece = None
        self.hold_piece = None
        self.hold_piece_used = False
        self.top_ten_scores = database.return_top_ten_scores()

    def remove_row(self, row):
        # Shift the remaining arrays to the right
        for i in range(row - 1, -1, -1):
            self.grid[i + 1] = self.grid[i]

        # Add a new row at the top
        self.grid[0] = [0 for x in range(self.board_width)]

    def check_rows(self):
        row_deleted_count = 0
        for x in range(0, len(self.grid)):
            if 0 not in self.grid[x]:
                self.remove_row(x)
                row_deleted_count += 1

        if row_deleted_count == 1:
            self.score += 40
        elif row_deleted_count == 2:
            self.score += 100
        elif row_deleted_count == 3:
            self.score += 300
        elif row_deleted_count == 4:
            self.score += 1200

    def draw(self, screen):
        # Set up font
        font = pygame.font.SysFont('Calibri', 25, True, False)

        # Draw the game board
        self.__draw_game_board(screen)

        # Draw the gridlines
        self.__draw_grid_lines(screen)

        # Draw the score number
        self.__draw_score(screen, font)

        # Draw the next piece
        self.__draw_next_piece(screen, font)

        # Draw the hold piece
        self.__draw_hold_piece(screen, font)

        if self.game_over:
            self.__draw_game_over_screen(screen)

    def __draw_game_board(self, screen):
        for y in range(0, self.board_height):
            for x in range(0, self.board_width):
                pygame.draw.rect(screen, colors[self.grid[y][x]], (
                    x * self.cell_size, y * self.cell_size, self.cell_size,
                    self.cell_size))

    def __draw_grid_lines(self, screen):
        for x in range(self.window_height - self.window_board_height,
                       self.window_board_width,
                       self.cell_size):
            pygame.draw.line(screen, GRAY, (x, 0),
                             (x, self.cell_size * self.board_height))
        for y in range(0, self.board_height):
            pygame.draw.line(screen, GRAY, (
                self.window_height - self.window_board_height,
                y * self.cell_size),
                             (self.window_board_width, y * self.cell_size))
        pygame.draw.line(screen, GRAY, (self.window_board_width, 0),
                         (self.window_board_width,
                          self.cell_size * self.board_height))
        pygame.draw.line(screen, GRAY, (
            self.window_height - self.window_board_height,
            self.cell_size * self.board_height),
                         (self.window_board_width,
                          self.cell_size * self.board_height))

    def __draw_score(self, screen, font):
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.fill(BLACK, (50, self.window_board_height+80, text.get_width(), text.get_height()))
        screen.blit(text, [50, self.window_board_height+80])

    def __draw_next_piece(self, screen, font):
        text = font.render(f"Next Piece", True, WHITE)
        screen.fill(BLACK, (self.window_board_width + 20, 50, text.get_width(), text.get_height()))
        screen.blit(text, [self.window_board_width + 20, 50])

        if self.next_piece:
            screen.fill(BLACK, (self.window_board_width + 20, 100, 150, 150))
            for y in range(0, len(self.next_piece.shape)):
                for x in range(0, len(self.next_piece.shape[y])):
                    pygame.draw.rect(screen, colors[self.next_piece.shape[y][x]], (
                        (x * self.cell_size) + self.window_board_width + 20, (y * self.cell_size) + 100, self.cell_size,
                        self.cell_size))


    def __draw_hold_piece(self, screen, font):
        text = font.render(f"Hold Piece", True, WHITE)
        screen.fill(BLACK, (
        self.window_board_width + 20, 200, text.get_width(), text.get_height()))
        screen.blit(text, [self.window_board_width + 20, 200])

        if self.hold_piece:
            screen.fill(BLACK, (self.window_board_width + 20, 250, 150, 150))
            for y in range(0, len(self.hold_piece.shape)):
                for x in range(0, len(self.hold_piece.shape[y])):
                    pygame.draw.rect(screen,
                                     colors[self.hold_piece.shape[y][x]], (
                                         (x * self.cell_size) + self.window_board_width + 20,
                                         (y * self.cell_size) + 250,
                                         self.cell_size,
                                         self.cell_size))

    def __draw_game_over_screen(self, screen):
        # Set up font
        font = pygame.font.SysFont('Calibri', 50, True, False)

        # Set up title text
        title_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        rectangle_width = 300
        rectangle_height = 550
        rectangle_left = (self.window_board_width - rectangle_width) // 2
        rectangle_top = (self.window_board_height - rectangle_height) // 2
        rectangle = pygame.Rect(rectangle_left, rectangle_top, rectangle_width,
                                rectangle_height)

        # Draw the rectangle
        pygame.draw.rect(screen, BLACK, rectangle)

        # Draw the title text
        title_text_rect = title_text.get_rect()
        title_text_rect.center = rectangle.center
        title_text_rect.y -= 200
        screen.blit(title_text, title_text_rect)

        # Draw the score text
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (rectangle.centerx, rectangle.centery + 30)
        score_text_rect.y -= 175
        screen.blit(score_text, score_text_rect)

        # Draw the leaderboard
        leaderboard_font = pygame.font.SysFont('Calibri', 30, True, False)
        leaderboard_text = leaderboard_font.render("Previous Top Scores", True, WHITE)
        leaderboard_text_rect = leaderboard_text.get_rect(
            center=(self.window_board_width // 2, title_text_rect.bottom + 30))
        leaderboard_text_rect.y += 50
        screen.blit(leaderboard_text, leaderboard_text_rect)

        for i, score in enumerate(self.top_ten_scores):
            leaderboard_entry = f"{i  + 1:2}. {score:5}"
            entry_text = leaderboard_font.render(leaderboard_entry, True, WHITE)
            entry_rect = entry_text.get_rect(
                center=(self.window_board_width // 2, leaderboard_text_rect.bottom + (i + 1) * 30))
            screen.blit(entry_text, entry_rect)
