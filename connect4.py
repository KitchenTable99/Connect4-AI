# This script will just be a visual game of Connect 4
# Author: Caleb Bitting
# Date: 05/25/2021

import numpy as np
from collections import namedtuple
StartingCoords = namedtuple('StartingCoords', ['row', 'column'])

class Board():

    def __init__(self):
        self.internal = np.zeros((6, 7))
        self.drop_idx = [5 for _ in range(7)]           # this is used to "simulate gravity"

    def __str__(self): return str(self.internal)

    def drop(self, column, player):
        '''This is the function that actually drops the piece
        
        Args:
            column (int): the column into which to drop the piece
            player (int): the value of the player 1 == red and 2 == yellow
        
        Returns:
            int: 0 if drop successful, -1 if outside of board, 1 if this drop caused a winning state
        '''
        # readability
        row = self.drop_idx[column]
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
            int: 1 for win and 0 for not
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
        return 0

    @classmethod
    def from_list(cls, l):
        '''This fucntion takes in a list and returns a Board object whos internal array represents the reshaped list
        
        Args:
            l (list): the list to be reshaped
        
        Returns:
            Board: the board object
        '''
        to_return = cls()
        to_return.internal = np.array(l).reshape(6,7)
        return to_return

def turn(board, player):
    '''This function is the exposed drop feature
    
    Args:
        board (Board): the board to play on
        player (int): the value to drop
    '''
    valid_column = False
    while not valid_column:
        drop_column = input(f'What column do you want to drop in? Player: {player} ')
        try:
            drop_column = int(drop_column)
        except:
            continue
        if drop_column >= 0 and drop_column <= 6:
            valid_column = True

    return board.drop(drop_column, player)

def play():
    board = Board()
    no_win = True
    while no_win:
        play = -1
        print(board)
        while play == -1:
            play = turn(board, 1)
        if play == 1:
            no_win = False
            print('PLAYER 1 WINS!!')
            break
        play = -1
        print(board)
        while play == -1:
            play = turn(board, 2)
        if play == 1:
            no_win = False
            print('PLAYER 2 WINS!!')


def main():
    play()

if __name__ == '__main__':
    main()