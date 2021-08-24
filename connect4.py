# This script will just be a visual game of Connect 4
# Author: Caleb Bitting
# Date: 05/25/2021

import sys
import time
import math
import pygame


from bitboards import BitBoard, GameState

def draw_board(game_state, screen, first_draw=False):
    # draw an empty board
    if first_draw:
        for c in range(7):
            for r in range(6):
                # set up a rectange
                rect = pygame.Rect(c*100, r*100, (c+1)*100, (r+1)*100)
                pygame.draw.rect(screen, [69, 69, 69], rect)
                # this is an ugly draw statement that draws a black circle in the middle of each square
                pygame.draw.circle(screen, [0, 0, 0], (int((c*100) + 50), int((r*100) + 50)),  45)

    bboard_1, bboard_2 = game_state.bitboards()

    for idx, position in enumerate(reversed(bboard_1.binary_array())):
        if int(position) == 1:
            print("triggered")
            row = idx % 7               # modulo gets the row
            column = idx // 7           # integer division gets the column
            draw_token(screen, row, column, 1)

    for idx, position in enumerate(reversed(bboard_2.binary_array())):
        if int(position) == 1:
            print("triggered")
            row = idx % 7               # modulo gets the row
            column = idx // 7           # integer division gets the column
            draw_token(screen, row, column, 2)

def draw_token(screen, row, column, player):
    '''This function serves as an intermediary between the game loop and the board object.
    
    Args:
        board (Board): the Board object on which the game is being played
        column (int): the column into which to drop the token
        player (int): the plays whose turn it is
    
    Returns:
        int: the final board state. (-1 for failed drop. 0 for continue game and 1 for game over)
    '''
    print('draw token called')
    # find the center of the circle
    x_center = 50 + 100*column
    y_center = 50 + 100*row

    # yellowish for player 1 and reddish for player 2
    color = [250, 255, 92] if player == 1 else [230, 69, 69]

    # draw the circle
    pygame.draw.circle(screen, color, (x_center, y_center), 45)

def main():
    # set up pygame
    pygame.init()
    screen = pygame.display.set_mode((700, 600))

    # set up objects
    game_state = GameState()

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
                drop_column = math.trunc(event.pos[0]/100)
                dropped = game_state.drop(drop_column)
                if dropped:
                    draw_board(game_state, screen)
                    end = game_state.end()
                    if end == 1:
                        print('Player 1 won!')
                        game_over = True
                    elif end == 2:
                        print('Player 2 won!')
                        game_over = True
                    elif end == 0:
                        print('Draw...')
                        game_over = True
                    else:
                        pass
                

        pygame.display.flip()           # update display
    # once game over sleep for a bit then quit
    time.sleep(1)
    sys.exit()

if __name__ == '__main__':
    main()