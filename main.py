import pygame
from tictactoe import Game, Renderer


def main():
    renderer = Renderer()

    clock = pygame.time.Clock()

    new_game = True
    wait_for_new_game = False
    running = True

    while running:
        clock.tick(60)
        if new_game:
            game = Game()
            new_game = False
            renderer.draw(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if wait_for_new_game:
                    new_game = True
                    wait_for_new_game = False
                else:
                    x, y = pygame.mouse.get_pos()
                    row, col = renderer.convert_coords(x, y)
                    if game.move(row, col):
                        if game.get_winner():
                            wait_for_new_game = True
                renderer.draw(game)


if __name__ == "__main__":
    main()
