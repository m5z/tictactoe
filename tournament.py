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
    def __init__(self, player_1_move_function, player_2_move_function):
        self.player_1 = Player(1, player_1_move_function)
        self.player_2 = Player(2, player_2_move_function)
        self.game = Game()

    def run(self):
        current_black = self.player_1
        current_white = self.player_2
        while True:
            if self.game.turn == Game.BLACK:
                i, j = current_black.move_function(self.game)
            else:
                i, j = current_white.move_function(self.game)
            moved = self.game.move(i, j)
            if moved:
                # time.sleep(0.1)
                winner = self.game.get_winner()
                if winner:
                    if winner == Game.BLACK:
                        current_black.score += 3
                    elif winner == Game.WHITE:
                        current_white.score += 3
                    else:
                        current_black.score += 1
                        current_white.score += 1
                    current_black, current_white = current_white, current_black
                    print(f"Player 1 score: {self.player_1.score}, Player 2 score: {self.player_2.score}")
                    self.game = Game()

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()


def display(tournament: Tournament):
    renderer = Renderer()

    clock = pygame.time.Clock()

    running = True
    last_update = 0.0

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if last_update != tournament.game.last_update:
            last_update = tournament.game.last_update
            renderer.draw(tournament.game)


def random_moves(game: Game):
    return random.randint(0, 2), random.randint(0, 2)


def q_learning_table(game: Game):
    with open('learning/Q.pickle', 'rb') as f:
        Q = pickle.load(f)
    state = get_state(game)
    if state in Q:
        action = np.argmax(Q[state])
    else:
        action = random.randint(0, 8)

    i = action // Game.BOARD_HEIGHT
    j = action % Game.BOARD_WIDTH

    return i, j


def main():
    headless = Tournament(random_moves, q_learning_table)
    headless.start()
    display(headless)


if __name__ == "__main__":
    main()
