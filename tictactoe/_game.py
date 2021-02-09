import time


class Game:
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    DRAW = 3

    BOARD_WIDTH = 3
    BOARD_HEIGHT = 3
    WINNING_LINE_LENGTH = 3

    def __init__(self):
        self.board = [[Game.EMPTY, Game.EMPTY, Game.EMPTY] for _ in range(3)]
        self.turn = Game.BLACK
        self.last_update = time.time()

    def reset(self):
        for i in range(Game.BOARD_HEIGHT):
            for j in range(Game.BOARD_WIDTH):
                self.board[i][j] = Game.EMPTY
        self.turn = Game.BLACK
        self.last_update = time.time()

    def move(self, i, j):
        if self.board[i][j] == Game.EMPTY:
            self.board[i][j] = self.turn
            self._switch_turn()
            self.last_update = time.time()
            return True
        else:
            return False

    def is_valid_move(self, i, j):
        return self.board[i][j] == Game.EMPTY

    def _switch_turn(self):
        if self.turn == Game.BLACK:
            self.turn = Game.WHITE
        else:
            self.turn = Game.BLACK

    def get_available_moves(self):
        return [(i, j) for i, row in enumerate(self.board) for j, current in enumerate(row) if current == Game.EMPTY]

    def get_winner(self):
        placed = 0
        for i, row in enumerate(self.board):
            for j, current in enumerate(row):
                if current != Game.EMPTY:
                    placed += 1
                    if self._check_line(i, j, current):
                        return current
        if placed == Game.BOARD_WIDTH * Game.BOARD_HEIGHT:
            return Game.DRAW

    def _check_line(self, i, j, current):
        if i + Game.WINNING_LINE_LENGTH <= Game.BOARD_HEIGHT:
            if self._check_line_direction(i, j, current, 1, 0):
                return True
        if j + Game.WINNING_LINE_LENGTH <= Game.BOARD_WIDTH:
            if self._check_line_direction(i, j, current, 0, 1):
                return True
        if i + Game.WINNING_LINE_LENGTH <= Game.BOARD_HEIGHT and j + Game.WINNING_LINE_LENGTH <= Game.BOARD_WIDTH:
            if self._check_line_direction(i, j, current, 1, 1):
                return True
        if i + Game.WINNING_LINE_LENGTH <= Game.BOARD_HEIGHT and j - Game.WINNING_LINE_LENGTH >= -1:
            if self._check_line_direction(i, j, current, 1, -1):
                return True
        return False

    def _check_line_direction(self, i, j, current, dir_i, dir_j):
        win = True
        for k in range(1, Game.WINNING_LINE_LENGTH):
            if self.board[i + dir_i * k][j + dir_j * k] != current:
                win = False
                break
        return win
