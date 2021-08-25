# this is the python file for bitboards

class GameState():

    def __init__(self):
        # create the player boards
        self.bboard_1 = BitBoard()
        self.bboard_2 = BitBoard()
        # setup other constants
        self.current_turn = 1
        self.top_row_by_column = [5 for _ in range(7)]

    def bitboards(self):
        '''This function is used to extract both bitboards from this object
        
        Returns:
            tuple: A tuple of bitboards (bboard_1, bboard_2)
        '''
        return (self.bboard_1, self.bboard_2)
    
    def drop(self, column):
        '''This function tries to update the game state with a dropped token
        
        Args:
            column (int): the column in which to try to drop the token
        
        Returns:
            bool: whether or not the drop was successful
        '''
        # get proper row corresponding to column
        row = self.top_row_by_column[column]
        if row == -1:                               # column full, try again
            return False
        self.top_row_by_column[column] -= 1          # decrement row-column indices

        exec(f'self.bboard_{self.current_turn}.drop(row, column)')       # put correct token in correct place
        self.current_turn = 3 - self.current_turn                        # switch the turns

        return True

    def end(self):
        '''This function checks if it is the end of the game
        
        Returns:
            int: 1 -> player 1 victory
                 2 -> player 2 victory 
                 0 -> draw
                -1 -> game continues
        '''
        if self.bboard_1.check_win():
            return 1
        elif self.bboard_2.check_win():
            return 2
        elif (self.bboard_1.internal | self.bboard_2.internal) == 562949953421311:      # this bitwise or operation will light up the full 49 bits if there is a token everywhere
            return 0
        else:
            return -1

class BitBoard:

    def __init__(self):
         self.internal = 0

    def drop(self, row, column):
        '''This function incriments the internal counter by lighting up the bit that needs to be high in order for the bitboard to hold the correct token.
           NOTE: this function does not check if the drop is possible by game rules. It just places the token.
        
        Args:
            row (int): the row into which to place the token
            column (int): the column into which to place the token
        '''
        drop_idx = (7*column) + row	        # find the spot in grid
        drop_num = 2**drop_idx		        # translate to number
        self.internal += drop_num

    def binary_array(self):
        '''This function returns an 49-bit representation of the numnber of the bitboard in binary as an array
        
        Returns:
            list: [0/1, 0/1, ... , 0/1]
        '''
        binary_string = format(self.internal, '049b')
        return [int(num) for num in binary_string]

    def connected_check(self, shift_distance):
        '''This function will check to see if the bitboard contains a win given some directional shift.'''
        left_bboard = self.internal >> shift_distance                          # shift left
        combined_left = self.internal & left_bboard                            # combine shifted with original
        lefter_bboard = combined_left >> (2*shift_distance)                    # shift right

        return True if (lefter_bboard & combined_left) else False

    def check_win(self):
        '''This function checks for a win in all four directions
        
        Returns:
            bool: whether or not there is a win on this bitboard
        '''
        for shift_distance in [1, 6, 7, 8]:
            win = self.connected_check(shift_distance)
            if win:
                print(shift_distance)
                return True
        else:
            return False


    def __str__(self):
        # setup variables
        to_return = ''
        normal_b_string = self.binary_array()
        formatted_b_string = normal_b_string[::-1]

        # iterate across the rows in decending order
        for row in range(6,-1,-1):
            print_row = ''
            # iterate across the rows in acending order
            for column in range(7):
                idx = row+(7*column)
                print_row += str(formatted_b_string[idx])
                print_row += '  '
            to_return += print_row
            to_return += '\n'

        return to_return[:-1]   # don't return the last \n

def test():
    bboard = BitBoard()
    bboard.drop(0,1)
    bboard.drop(1,0)

if __name__ == '__main__':
    test()