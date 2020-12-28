import pygame
from tictactoe import Game

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

GRID_SIZE = 3

CELL_WIDTH = SCREEN_WIDTH / GRID_SIZE
CELL_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

BLACK = (0, 0, 0)


def main():
    pygame.init()
    pygame.display.set_caption('TicTacToe')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    new_game = True
    wait_for_new_game = False

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    running = True
    while running:
        clock.tick(60)
        if new_game:
            game = Game()
            draw_board(screen)
            new_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if wait_for_new_game:
                    new_game = True
                    wait_for_new_game = False
                else:
                    x, y = pygame.mouse.get_pos()
                    row, col = convert_coords(x, y)
                    turn = game.turn
                    if game.move(row, col):
                        if turn == Game.BLACK:
                            draw_o(screen, row, col)
                        else:
                            draw_x(screen, row, col)
                        winner = game.get_winner()
                        if winner:
                            if winner == Game.BLACK:
                                text = "O Wins"
                            elif winner == Game.WHITE:
                                text = "X Wins"
                            else:
                                text = "Draw"
                            rendered_text = font.render(text, True, BLACK)
                            screen.blit(rendered_text, (10, 10))
                            wait_for_new_game = True

        pygame.display.flip()


def convert_coords(x, y):
    return int(x // CELL_WIDTH), int(y // CELL_HEIGHT)


def draw_board(screen):
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, BLACK, (CELL_WIDTH, 0), (CELL_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(screen, BLACK, (2 * CELL_WIDTH, 0), (2 * CELL_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, CELL_HEIGHT), (SCREEN_WIDTH, CELL_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, 2 * CELL_HEIGHT), (SCREEN_WIDTH, 2 * CELL_HEIGHT))


def draw_x(screen, row, col):
    pygame.draw.line(
        screen,
        BLACK,
        (row * CELL_WIDTH, col * CELL_HEIGHT),
        ((row + 1) * CELL_WIDTH, (col + 1) * CELL_HEIGHT)
    )
    pygame.draw.line(
        screen,
        BLACK,
        ((row + 1) * CELL_WIDTH, col * CELL_HEIGHT),
        (row * CELL_WIDTH, (col + 1) * CELL_HEIGHT)
    )


def draw_o(screen, row, col):
    pygame.draw.circle(
        screen,
        BLACK,
        ((row * CELL_WIDTH) + CELL_WIDTH / 2, (col * CELL_HEIGHT) + CELL_HEIGHT / 2),
        CELL_WIDTH / 2,
        1
    )


if __name__ == '__main__':
    main()
