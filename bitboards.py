# this is the python file for bitboards

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
    print(bboard)

if __name__ == '__main__':
    test()