import pickle
import random
from collections import defaultdict
from multiprocessing.pool import Pool

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
    state = 0

    mul = 1
    for row in game.board:
        for color in row:
            state += encode(color) * mul
            mul *= 3

    return state


def get_reward(winner):
    if winner == Game.DRAW:
        return 0
    else:
        return 1


def move(Q, state, game, e, action_space):
    if random.random() < e:
        action = random.randint(0, action_space - 1)
        i, j = action // Game.BOARD_HEIGHT, action % Game.BOARD_WIDTH
        while not game.is_valid_move(i, j):
            action = random.randint(0, action_space - 1)
            i, j = action // Game.BOARD_HEIGHT, action % Game.BOARD_WIDTH
    else:
        action = np.argmax(Q[state])
        i, j = action // Game.BOARD_HEIGHT, action % Game.BOARD_WIDTH
        while not game.is_valid_move(i, j):
            Q[state][action] -= 10
            action = np.argmax(Q[state])
            i, j = action // Game.BOARD_HEIGHT, action % Game.BOARD_WIDTH
    game.move(i, j)
    return action


def train(lr=1.0, y=0.9, e=0.25, epochs=20000):
    action_space = Game.BOARD_WIDTH * Game.BOARD_HEIGHT

    Q = defaultdict(lambda: np.zeros(action_space))
    game = Game()

    for epoch in tqdm(range(epochs)):
    # for epoch in range(epochs):
        black_state = get_state(game)
        white_state = white_action = None

        while True:
            black_action = move(Q, black_state, game, e, action_space)
            new_white_state = get_state(game)

            winner = game.get_winner()
            if winner:
                if winner == Game.DRAW:
                    white_reward = black_reward = 0
                else:
                    black_reward = 1
                    white_reward = -1
                Q[black_state][black_action] += lr * (
                        black_reward + y * np.max(Q[new_white_state]) - Q[black_state][black_action])
                Q[white_state][white_action] += lr * (
                        white_reward + y * np.max(Q[new_white_state]) - Q[white_state][white_action])
                game.reset()
                break
            else:
                if white_state is not None:
                    Q[white_state][white_action] += lr * (y * np.max(Q[new_white_state]) - Q[white_state][white_action])
                white_state = new_white_state

            white_action = move(Q, white_state, game, e, action_space)
            new_black_state = get_state(game)

            winner = game.get_winner()
            if winner:
                if winner == Game.DRAW:
                    white_reward = black_reward = 0
                else:
                    white_reward = 1
                    black_reward = -1
                Q[white_state][white_action] += lr * (
                        white_reward + y * np.max(Q[new_black_state]) - Q[white_state][white_action])
                Q[black_state][black_action] += lr * (
                        black_reward + y * np.max(Q[new_black_state]) - Q[black_state][black_action])
                game.reset()
                break
            else:
                Q[black_state][black_action] += lr * (y * np.max(Q[new_black_state]) - Q[black_state][black_action])
                black_state = new_black_state

    score = validate(Q)

    with open(f'Q_{score}_{lr}_{y}_{e}_{epochs}.pickle', 'wb') as file:
        pickle.dump(dict(Q), file)

    print(f"lr={lr}, y={y}, e={e}, epochs={epochs}, score={score}")


def validate(Q):
    import tournament
    t = tournament.Tournament(tournament.random_moves, tournament.QLearningTable(Q).move, limit=100000, display=False)
    score, _ = t.start()
    return score


if __name__ == '__main__':
    args = []
    # for lr in (0.4, 0.6, 0.8):
    #     for y in (0.2, 0.4, 0.6, 0.8):
    #         for e in (0.25,):
    #             args.append((lr, y, e, 100000))
    # with Pool(4) as p:
    #     p.starmap(train, args)

    train(0.4, 0.8, 0.25, 50000)
    # train(0.8, 1.0, 0.25, 50000)
    # train(0.6, 0.4, 0.25, 50000)
