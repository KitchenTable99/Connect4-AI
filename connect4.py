# This script will just be a visual game of Connect 4
# Author: Caleb Bitting
# Date: 05/25/2021

import sys
import time
import math
import pygame
from functools import wraps
from helper_classes import GameState, AlphaBetaAnalyzer
from typing import Optional


# decorator to trace execution of recursive function
def trace(func):
    # cache func name, which will be used for trace print
    func_name = func.__name__
    # define the separator, which will indicate current recursion level (repeated N times)
    separator = '|  '

    # current recursion depth
    trace.recursion_depth = 0

    @wraps(func)
    def traced_func(*args, **kwargs):
        # repeat separator N times (where N is recursion depth)
        # `map(str, args)` prepares the iterable with str representation of positional arguments
        # `", ".join(map(str, args))` will generate comma-separated list of positional arguments
        # `"x"*5` will print `"xxxxx"` - so we can use multiplication operator to repeat separator
        print(f'{separator * trace.recursion_depth}|-- {func_name}({", ".join(map(str, args))})')
        # we're diving in
        trace.recursion_depth += 1
        result = func(*args, **kwargs)
        # going out of that level of recursion
        trace.recursion_depth -= 1
        # result is printed on the next level
        print(f'{separator * (trace.recursion_depth + 1)}|-- return {result}')

        return result

    return traced_func


# helper_classes.AlphaBetaAnalyzer.alpha_beta = trace(helper_classes.AlphaBetaAnalyzer.alpha_beta)


def draw_board(game_state: GameState, screen: pygame.display, first_draw: bool = False) -> None:
    """This function draws the game board

    Args:
        game_state (GameState): this object contains all the information needed to rebuild the game state
        screen (pygame.screen): the screen on which to draw the information
        first_draw (bool, optional): is this the first draw or not?
    """
    # draw an empty board if it is the first time
    if first_draw:
        for c in range(7):
            for r in range(6):
                # set up a rectangle
                rect = pygame.Rect(c * 100, r * 100, (c + 1) * 100, (r + 1) * 100)
                pygame.draw.rect(screen, [69, 69, 69], rect)
                # this is an ugly draw statement that draws a black circle in the middle of each square
                pygame.draw.circle(screen, [0, 0, 0], (int((c * 100) + 50), int((r * 100) + 50)), 45)

    # every time get the bitboards for each player
    bboard_1, bboard_2 = game_state.bitboards

    # draw the tokens for each player in the correct location if the corresponding bit is high
    for idx, position in enumerate(reversed(bboard_1.binary_array)):
        if position == 1:
            row = idx % 7  # modulo gets the row
            column = idx // 7  # integer division gets the column
            draw_token(screen, row, column, 1)

    for idx, position in enumerate(reversed(bboard_2.binary_array)):
        if position == 1:
            row = idx % 7  # modulo gets the row
            column = idx // 7  # integer division gets the column
            draw_token(screen, row, column, 2)


def draw_token(screen: pygame.display, row: int, column: int, player: int) -> None:
    """This function draws a player token.

    Args:
        screen (pygame.screen): the screen on which to draw
        row (int): the row in which to drop the token
        column (int): the column into which to drop the token
        player (int): the plays whose turn it is
    """
    # find the center of the circle
    x_center = 50 + 100 * column
    y_center = 50 + 100 * row

    # yellowish for player 1 and reddish for player 2
    color = [250, 255, 92] if player == 1 else [230, 69, 69]

    # draw the circle
    pygame.draw.circle(screen, color, (x_center, y_center), 45)


def read_board_string(board_info: str) -> Optional[GameState]:
    """This function reads in a string and return the gamestate corresponding to those moves

    Args:
        board_info (str): the string with column numbers

    Returns:
        GameState: the game state object or a NoneType object
    """
    to_return: GameState = GameState()
    for char in board_info:
        successful_drop: bool = to_return.drop(int(char))
        if not successful_drop:
            return None

    return to_return


def main():
    # set up pygame
    pygame.init()
    screen = pygame.display.set_mode((700, 600))

    # set up objects
    # game_state = GameState()
    # game_state = read_board_string('33333324102212200000411165656612665454')
    # game_state = read_board_string('3333332410221220000041116565')
    game_state = read_board_string('33333320')


    # draw the board
    draw_board(game_state, screen, first_draw=True)

    # run pygame
    game_over = False
    while not game_over:
        # check for events
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                sys.exit()

            # player clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # try to drop token
                if game_state.current_turn == 1:
                    drop_column = math.trunc(event.pos[0] / 100)
                    dropped = game_state.drop(drop_column)

                    if dropped:
                        # redraw the player tokens
                        draw_board(game_state, screen)
                        # check for game end
                        end = game_state.end()
                        if end == 1:  # player one victory
                            print('Player 1 won!')
                            game_over = True
                        elif end == 2:  # player two victory
                            print('Player 2 won!')
                            game_over = True
                        elif end == 0:  # draw
                            print('Draw...')
                            game_over = True
                        else:  # game not over
                            pass
                            # print(f'if player 1: {game_state.bboard_1.win_this_move(game_state.top_row_by_column)}\nif player 2: {game_state.bboard_2.win_this_move(game_state.top_row_by_column)}')
        if game_state.current_turn == 2:
            ab_analyzer = AlphaBetaAnalyzer(game_state)
            ai_col = ab_analyzer.best_column()
            # print(f'{ai_col = }')
            game_state.drop(ai_col)
            draw_board(game_state, screen)
            end = game_state.end()
            if end == 1:  # player one victory
                print('Player 1 won!')
                game_over = True
            elif end == 2:  # player two victory
                print('Player 2 won!')
                game_over = True
            elif end == 0:  # draw
                print('Draw...')
                game_over = True
            else:  # game not over
                pass

        pygame.display.flip()  # update display
    # once game over sleep for a bit then quit
    time.sleep(1)
    sys.exit()


if __name__ == '__main__':
    main()
