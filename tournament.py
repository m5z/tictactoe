import random
import threading
import time

import pygame

from tictactoe import Renderer, Game


class Player:
    def __init__(self, id, move_function):
        self.id = id
        self.move_function = move_function
        self.score = 0


class Tournament:
    def __init__(self, player_1_move_function, player_2_move_function):
        self._player_1 = Player(1, player_1_move_function)
        self._player_2 = Player(2, player_2_move_function)
        self._game = Game()

    def run(self):
        current_black = self._player_1
        current_white = self._player_2
        while True:
            if self._game.turn == Game.BLACK:
                i, j = current_black.move_function(self._game.board)
            else:
                i, j = current_white.move_function(self._game.board)
            moved = self._game.move(i, j)
            if moved:
                # time.sleep(0.25)
                winner = self._game.get_winner()
                if winner:
                    if winner == Game.BLACK:
                        current_black.score += 3
                    elif winner == Game.WHITE:
                        current_white.score += 3
                    else:
                        current_black.score += 1
                        current_white.score += 1
                    current_black, current_white = current_white, current_black
                    print(f"Player 1 score: {self._player_1.score}, Player 2 score: {self._player_2.score}")
                    self._game = Game()

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
        if last_update != tournament._game.last_update:
            last_update = tournament._game.last_update
            renderer.draw(tournament._game)


def random_moves(game: Game):
    return random.randint(0, 2), random.randint(0, 2)


def main():
    headless = Tournament(random_moves, random_moves)
    headless.start()
    display(headless)


if __name__ == "__main__":
    main()