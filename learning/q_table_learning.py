import pickle
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from tictactoe import Game


def encode(color):
    if color == Game.EMPTY:
        return 0
    if color == Game.BLACK:
        return 1
    if color == Game.WHITE:
        return 2
    raise ValueError()


def get_state(game):
    state = encode(game.turn)

    mul = 3
    for row in game.board:
        for color in row:
            state += encode(color) * mul
            mul *= 3

    return state


def get_reward(game):
    winner = game.get_winner()
    if not winner:
        return 0
    if winner == Game.DRAW:
        return 0.25
    else:
        return 1


def get_actions():
    return [0.0] * (Game.BOARD_WIDTH * Game.BOARD_HEIGHT)


def train():
    action_space = Game.BOARD_WIDTH * Game.BOARD_HEIGHT

    Q = defaultdict(get_actions)
    game = Game()

    lr = 0.8
    y = 0.95

    epochs = 100000
    for epoch in tqdm(range(epochs)):
        state = get_state(game)

        while True:
            action = np.argmax(Q[state] + np.random.randn(1, action_space))
            i = action // Game.BOARD_HEIGHT
            j = action % Game.BOARD_WIDTH
            move = game.move(i, j)

            new_state = get_state(game)
            reward = get_reward(game)

            Q[state][action] = float(Q[state][action] + lr * (reward + y * np.max(Q[new_state]) - Q[state][action]))
            state = new_state

            if reward > 0:
                game.reset()
                break

    with open('Q.pickle', 'wb') as file:
        pickle.dump(dict(Q), file)


if __name__ == '__main__':
    train()
