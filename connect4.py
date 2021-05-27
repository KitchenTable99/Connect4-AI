# This script will just be a visual game of Connect 4
# Author: Caleb Bitting
# Date: 05/25/2021

import sys
import time
import math
import pygame
import numpy as np
from collections import namedtuple
StartingCoords = namedtuple('StartingCoords', ['row', 'column'])

class Board():

    def __init__(self, screen):
        self.internal = np.zeros((6, 7))
        self.drop_idx = [5 for _ in range(7)]           # this is used to "simulate gravity"
        self.screen = screen
        self.most_recent_drop = None

    def __str__(self): return str(self.internal)

    def drop(self, column, player):
        '''This is the function that actually drops the piece
        
        Args:
            column (int): the column into which to drop the piece
            player (int): the value of the player 1 == red and 2 == yellow
        
        Returns:
            int: 0 if drop successful, -1 if outside of board, 1 if this drop caused a winning state, 2 if this caused a drawn state
        '''
        # readability
        row = self.drop_idx[column]
        self.most_recent_drop = (row, column)
        # make sure that we aren't trying to drop the token above the board
        if row < 0:
            return -1                                      # did not drop token
        # update the board state
        self.drop_idx[column] -= 1
        self.internal[row, column] = player
        return self.won(row, column, player)               # dropped token or win

    def won(self, row, column, player):
        '''This function checks to see if the most recently dropped token resulted in a win
        
        Args:
            column (int): the column into which the most recently dropped token was dropped
            row (int): the row into which the most recently dropped token was dropped
            player (int): the player who dropped the most recently dropped token
        
        Returns:
            int: 0 for not, 1 for win, and 2 for draw
        '''
        # check row
        in_a_row = 0
        for token in self.internal[row]:
            if token != player:
                in_a_row = 0            # reset count if not player token
            else:
                in_a_row += 1           # increment count and check for win
                if in_a_row >= 4:
                    return 1
        # check column
        in_a_row = 0
        for temp_row in range(6):
            token = self.internal[temp_row, column]
            if token != player:
                in_a_row = 0            # reset count if not player token
            else:
                in_a_row += 1           # increment count and check for win
                if in_a_row == 4:
                    return 1
        # check diagonals from bottom to top
        # left
        in_a_row = 0
        diag1 = StartingCoords(row + min((5-row), column), column - min((5-row), column))           # will always find the bottom left coordinate as one coordinate is zero by definition
        for r, c in zip(range(diag1.row, -1, -1), range(diag1.column, 7)):
            token = self.internal[r, c]
            if token != player:
                in_a_row = 0            # reset count if not player token
            else:
                in_a_row += 1           # increment count and check for win
                if in_a_row == 4:
                    return 1

        # right
        in_a_row = 0
        diag2 = StartingCoords(row + min((5-row), (6-column)), column + min((5-row), (6-column)))         # find the lower right corner of the x
        for r, c in zip(range(diag2.row, -1, -1), range(diag2.column, -1, -1)):
            token = self.internal[r, c]
            if token != player:
                in_a_row = 0            # reset count if not player token
            else:
                in_a_row += 1           # increment count and check for win
                if in_a_row == 4:
                    return 1

        # make sure board is not drawn
        if np.all(self.internal):           # if all things are filled and no winning state, return 2 because drawn
            return 2
        return 0

    def display_most_recent_token(self, player):
        '''This function displays the most recently dropped token
        
        Args:
            player (int): the player number 1 or 2
        '''
        # find the center of the circle
        x_center = 50 + 100*self.most_recent_drop[1]
        y_center = 50 + 100*self.most_recent_drop[0]
        # yellowish for player 1 and reddish for player 2
        color = [250, 255, 92] if player == 1 else [230, 69, 69]
        # draw the circle
        pygame.draw.circle(self.screen, color, (x_center, y_center), 45)


    @classmethod
    def from_list(cls, l, screen):
        '''This fucntion takes in a list and returns a Board object whos internal array represents the reshaped list
        
        Args:
            l (list): the list to be reshaped
        
        Returns:
            Board: the board object
        '''
        to_return = cls(screen)
        to_return.internal = np.array(l).reshape(6,7)
        return to_return

def turn(board, player, screen):
    '''This function is the exposed drop feature
    
    Args:
        board (Board): the board to play on
        player (int): the value to drop
        screen (pygame.Screen): the screen to draw on
    
    Returns:
        int: the value returned by the drop funciton. used to determine the game state
    '''

    return board.drop(drop_column, player)


def draw_board(rows, columns, square_size, screen):
    '''This function draws the connect4 board to set up the game
    
    Args:
        rows (int): the number of rows to draw
        columns (int): the number of columns to draw
        square_size (int): the size of a square
        screen (pygame.Screen): a pygame screen
    '''
    # draw the matrix
    for c in range(columns):
        for r in range(rows):
            # set up a rectange
            rect = pygame.Rect(c*square_size, r*square_size, (c+1)*square_size, (r+1)*square_size)
            pygame.draw.rect(screen, [69, 69, 69], rect)
            # this is an ugly draw statement that draws a black circle in the middle of each square
            pygame.draw.circle(screen, [0, 0, 0], (int((c*square_size) + (square_size/2)), int((r*square_size) + (square_size/2))), (square_size/2 - 5))

def main():
    # setting up constants and pygame
    pygame.init()

    total = 3 # used to toggle between players
    square_size = 100
    columns = 7
    rows = 6
    size = (columns*square_size, rows*square_size)
    screen = pygame.display.set_mode(size)
    board = Board(screen)

    # draw the board
    draw_board(rows, columns, square_size, screen)

    # run pygame
    player = 1
    game_over = False
    while not game_over:
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # try to drop token
                board_state = -1
                drop_column = math.trunc(event.pos[0]/100)
                board_state = board.drop(drop_column, player)
                # if the token dropped
                if board_state != -1:
                    board.display_most_recent_token(player)
                # check for win
                if board_state == 1:
                    print(f'Player {player} won!')
                    game_over = True
                if board_state == 2:
                    print(f'Drawn')
                    game_over = True
                player = total - player                         # if 1, 3-1 -> 2 and if 2 then 3-2 -> 1

        pygame.display.flip()           # update display
    # once game over sleep for a bit then quit
    time.sleep(2)
    sys.exit()

if __name__ == '__main__':
    main()