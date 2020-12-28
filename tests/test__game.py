from tictactoe import Game


def test_back_diagonal():
    game = Game()

    game.move(0, 2)
    game.move(0, 1)
    game.move(1, 1)
    game.move(2, 1)
    game.move(2, 0)

    assert game.get_winner() == 1


def test_front_diagonal():
    game = Game()

    game.move(0, 2)
    game.move(0, 0)
    game.move(1, 2)
    game.move(1, 1)
    game.move(0, 1)
    game.move(2, 2)

    assert game.get_winner() == 2
