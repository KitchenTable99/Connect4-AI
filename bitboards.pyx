# This is the Cython file to create the bitboards to represent the gamestate

import cython

cdef class BitBoard:
    cdef list internal

    def __init__(self):
        temp_array = [0] * 49
        self.internal = temp_array

    cdef char win(self):
        for Function function in [horizonal, vertical, diag1, diag2]:
            cdef char win = self.function()
            if win:
                break
        else:
            return 0
        return 1
