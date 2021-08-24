# this is the python file for bitboards

class GameState():

    def __init__(self):
        # create the player boards
        bboard_1 = BitBoard()
        bboard_2 = BitBoard()
        # setup other constants
        current_turn = 1
        top_row_by_column = [5 for _ in range(7)]
    
    def drop(self, column):
        # get proper row corresponding to column
        row = self.top_row_by_column[column]
        if row == -1:                               # column full, try again
            return False
        self.top_row_by_column[column] -=1          # decrement row-column indices

        exec(f'bboard_{self.current_turn}.drop(row, column)')       # put correct token in correct place
        self.current_turn = 3 - current_turn                        # switch the turns

        return True

class BitBoard:

    def __init__(self):
         self.internal = 0

    def drop(self, row, column):
        drop_idx = (7*column) + row	# find the spot in grid
        drop_num = 2**drop_idx		# translate to number
        self.internal += drop_num

    def binary_array(self):
        binary_string = format(self.internal, '049b')
        return [num for num in binary_string]

    def connected_check(self, shift_distance):
        '''This function will check to see if the bitboard contains a win in the horizontal direction.'''
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
                print_row += formatted_b_string[idx]
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