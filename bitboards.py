# this is the python file for bitboards

class BitBoard:

    def __init__(self):
         self.internal = 0

    def drop(self, column, row):
        drop_idx = (7*column) + row	# find the spot in grid
        drop_num = 2**drop_idx		# translate to number
        self.internal += drop_num

    def return_binary(self):
        binary_string = format(self.internal, 'b')
        return [num for num in binary_string]
        
