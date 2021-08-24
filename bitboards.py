# this is the python file for bitboards

class BitBoard:

    def __init__(self):
         self.internal = 0

    def drop(self, row, column):
        drop_idx = (7*column) + row	# find the spot in grid
        drop_num = 2**drop_idx		# translate to number
        self.internal += drop_num

    def binary_string(self):
        binary_string = format(self.internal, '049b')
        return [num for num in binary_string]

    def print_self(self):
        normal_b_string = self.binary_string()
        formatted_b_string = normal_b_string[::-1]
        for row in range(6,-1,-1):
            print_row = ''
            for column in range(7):
                idx = row+(7*column)
                print_row += formatted_b_string[idx]
                print_row += '  '
            print(print_row)

def test():
    b = BitBoard()
    b.drop(0,1)
    b.drop(1,0)
    b.print_self()

if __name__ == '__main__':
    test()
