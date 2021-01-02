import pygame

from tictactoe import Game

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

GRID_SIZE = 3

CELL_WIDTH = SCREEN_WIDTH / GRID_SIZE
CELL_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._font = pygame.font.SysFont("monospace", 64)

    def draw(self, game: Game):
        self.draw_board()
        for i, row in enumerate(game.board):
            for j, value in enumerate(row):
                if value == Game.BLACK:
                    self.draw_o(i, j)
                elif value == Game.WHITE:
                    self.draw_x(i, j)

        winner = game.get_winner()
        if winner:
            if winner == Game.BLACK:
                text = "O Wins"
            elif winner == Game.WHITE:
                text = "X Wins"
            else:
                text = "Draw"
            rendered_text = self._font.render(text, True, BLACK, WHITE)
            pos_x = (SCREEN_WIDTH - rendered_text.get_width()) / 2
            pos_y = (SCREEN_HEIGHT - rendered_text.get_height()) / 2
            self._screen.blit(rendered_text, (pos_x, pos_y))

        pygame.display.flip()

    def draw_board(self):
        self._screen.fill((255, 255, 255))
        pygame.draw.line(self._screen, BLACK, (CELL_WIDTH, 0), (CELL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(self._screen, BLACK, (2 * CELL_WIDTH, 0), (2 * CELL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(self._screen, BLACK, (0, CELL_HEIGHT), (SCREEN_WIDTH, CELL_HEIGHT))
        pygame.draw.line(self._screen, BLACK, (0, 2 * CELL_HEIGHT), (SCREEN_WIDTH, 2 * CELL_HEIGHT))

    def draw_o(self, row, col):
        pygame.draw.circle(
            self._screen,
            BLACK,
            (
                (row * CELL_WIDTH) + CELL_WIDTH / 2,
                (col * CELL_HEIGHT) + CELL_HEIGHT / 2,
            ),
            CELL_WIDTH / 2,
            1,
        )

    def draw_x(self, row, col):
        pygame.draw.line(
            self._screen,
            BLACK,
            (row * CELL_WIDTH, col * CELL_HEIGHT),
            ((row + 1) * CELL_WIDTH, (col + 1) * CELL_HEIGHT),
        )
        pygame.draw.line(
            self._screen,
            BLACK,
            ((row + 1) * CELL_WIDTH, col * CELL_HEIGHT),
            (row * CELL_WIDTH, (col + 1) * CELL_HEIGHT),
        )

    def convert_coords(self, x, y):
        return int(x // CELL_WIDTH), int(y // CELL_HEIGHT)
