# Define some colors
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colors = {
    0: (0, 0, 0),
    1: (0, 0, 255),
    2: (255, 0, 0),
    3: (0, 255, 0),
    4: (160, 32, 240),
    5: (255, 165, 0),
    6: (255, 255, 0),
    7: (0, 100, 100)
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

    def game_over_screen(self, screen):
        # Set up font
        font = pygame.font.SysFont('Calibri', 50, True, False)

        # Set up title text
        title_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        rectangle_width = 300
        rectangle_height = 150
        rectangle_left = (self.window_board_width - rectangle_width) // 2
        rectangle_top = (self.window_board_height - rectangle_height) // 2
        rectangle = pygame.Rect(rectangle_left, rectangle_top, rectangle_width,
                                rectangle_height)

        # Draw the rectangle
        pygame.draw.rect(screen, BLACK, rectangle)

        # Draw the title text
        title_text_rect = title_text.get_rect()
        title_text_rect.center = rectangle.center
        title_text_rect.y -= 30
        screen.blit(title_text, title_text_rect)

        # Draw the score text
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (rectangle.centerx, rectangle.centery + 30)
        screen.blit(score_text, score_text_rect)

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
        # Draw the game board
        for y in range(0, self.board_height):
            for x in range(0, self.board_width):
                pygame.draw.rect(screen, colors[self.grid[y][x]], (
                    x * self.cell_size, y * self.cell_size, self.cell_size,
                    self.cell_size))

        # Draw the gridlines
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

        # Draw the score number
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.fill(BLACK, (50, self.window_board_height, text.get_width(), text.get_height()))
        screen.blit(text, [50, self.window_board_height])

        if self.game_over:
            self.game_over_screen(screen)

