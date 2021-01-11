from learning.q_table_learning import get_state
from tictactoe import Game


def test_get_state_start_game():
    game = Game()

    assert get_state(game) == 1


def test_get_state_one_move():
    game = Game()

    game.move(2, 2)

    assert get_state(game) == 2 + 3 ** 9
