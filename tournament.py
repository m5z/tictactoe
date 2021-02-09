import pickle
import random
import threading
import time
import numpy as np
import pygame

from learning.q_table_learning import get_state
from tictactoe import Renderer, Game


class Player:
    def __init__(self, id, move_function):
        self.id = id
        self.move_function = move_function
        self.score = 0


class Tournament:
    def __init__(self, player_1_move_function, player_2_move_function, limit=10000, display=True):
        self.player_1 = Player(1, player_1_move_function)
        self.player_2 = Player(2, player_2_move_function)
        self.limit = limit
        self.display = display
        self.game = Game()

    def run(self):
        current_black = self.player_1
        current_white = self.player_2
        played = 0
        while played < self.limit:
            self.move(current_black, current_white)

            # time.sleep(0.1)
            winner = self.game.get_winner()
            if winner:
                if winner == Game.BLACK:
                    current_black.score += 1
                elif winner == Game.WHITE:
                    current_white.score += 1
                # else:
                #     current_black.score += 1
                #     current_white.score += 1
                current_black, current_white = current_white, current_black
                if self.display:
                    print(f"Player 1 score: {self.player_1.score}, Player 2 score: {self.player_2.score}")
                self.game = Game()
                played += 1
        return self.player_1.score, self.player_2.score

    def move(self, current_black, current_white):
        for _ in range(10):
            if self.game.turn == Game.BLACK:
                i, j = current_black.move_function(self.game)
            else:
                i, j = current_white.move_function(self.game)
            if self.game.move(i, j):
                return

        while True:
            if self.game.move(random.randint(0, 2), random.randint(0, 2)):
                return

    def start(self):
        if self.display:
            thread = threading.Thread(target=self.run, daemon=True)
            thread.start()
        else:
            return self.run()


last_click = 0
row, col = -1, -1


def display(tournament: Tournament):
    global last_click, row, col

    renderer = Renderer()

    clock = pygame.time.Clock()

    running = True
    last_update = 0.0

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                last_click = time.time()
                x, y = pygame.mouse.get_pos()
                row, col = renderer.convert_coords(x, y)
        if last_update != tournament.game.last_update:
            last_update = tournament.game.last_update
            renderer.draw(tournament.game)


def random_moves(game: Game):
    return random.randint(0, 2), random.randint(0, 2)


class QLearningTable:
    def __init__(self, Q):
        if isinstance(Q, str):
            with open('learning/Q.pickle', 'rb') as f:
                Q = pickle.load(f)
        self.Q = Q

    def move(self, game: Game):
        state = get_state(game)
        if state in self.Q:
            action = np.argmax(self.Q[state])
        else:
            action = random.randint(0, 8)

        i = action // Game.BOARD_HEIGHT
        j = action % Game.BOARD_WIDTH

        return i, j


class Human:
    def __init__(self):
        self.last_move = 0

    def move(self, game: Game):
        while True:
            if last_click > self.last_move:
                self.last_move = last_click
                return row, col
            time.sleep(0.1)


def main():
    # headless = Tournament(Human().move, QLearningTable('learning/Q_0_0.6_0.4_0.25_100000.pickle').move)
    headless = Tournament(random_moves, QLearningTable('learning/Q_0_0.6_0.4_0.25_100000.pickle').move)
    headless.start()
    display(headless)


if __name__ == "__main__":
    main()
