# this script will house the evaluation function so that it can be cythonized
# the basic idea of the evaluation is to count the number of possible 4's for each side and subtract them.
# a positive score indicates that player one is winning while a negative indicates that player 2 is winning
# zero represents equality between the players while numbers whose absolute values are larger than 100 represents a win for the corresponding side
# Author: Caleb Bitting
# Date: 05/28/21

import numpy as np

def evaluate(array):
    '''This function takes in an array and returns the evaluation
    
    Args:
        array (np.array): the board state to be evalueated
    
    Returns:
        int: the evaluation
    '''
    p1_count = 0
    p2_count = 0
    # find the number of possible horizonal wins
    # the following code is rather difficult to read becuase list comprehensions are vectorized in python, so I wanted to use them for the speed boost
    # the ending section of each comprension sets out all of the starting rows and columns like a nested for loop
    # the actual meat of the algorithm is just incrimenting either the row or the column by the correct amount which is handled by the variable k
    hor_segs = [np.array([array[row, column+k] for k in range(4)]) for row in range(6) for column in range(4)]
    # find vertical
    vert_segs = [np.array([array[row+k, column] for k in range(4)]) for row in range(3) for column in range(7)]
    # find left diagonal
    left_diagonal_segs = [np.array([array[row - k, column + k] for k in range(4)]) for row in range(3, 6) for column in range(4)]
    # find right diagonal
    right_diagonal_segs = [np.array([array[row - k, column - k] for k in range(4)]) for row in range(3, 6) for column in range(3, 7)]

    # for each section of four, count the possible wins for each side
    for seg_list in [hor_segs, vert_segs, left_diagonal_segs, right_diagonal_segs]:
        p1, p2 = count_4s(seg_list)
        p1_count += p1
        p2_count += p2

    # actually evaluate the board
    return p1_count - p2_count

def count_4s(segments):
    '''This function does the heavy lifting of counting all of the possible wins
    
    Args:
        segments (list of np.array): the segments to check for win potentials
    
    Returns:
        tuple (int, int): the wins for p1 and p2
    '''
    p1 = 0
    p2 = 0
    for seg in segments:
        seg_sum = seg.sum()            # this quantity will be very useful. 0 indicates empty. 4 and only ones indicates player 1 win. 8 and only twos indicates player 2 win.
        if seg_sum == 0:               # both players could win here
            p1 += 1
            p2 += 1
        elif 1 in seg:
            if 2 not in seg:
                p1 += 100 if seg_sum == 4 else 1              # add 100 if all four entries are ones otherwise just add 1
        else:                                                   # only happens when segment is not empty and doesn't have a one. i.e. the only number present is a 2
            p2 += 100 if seg_sum == 8 else 1                  # add 100 if all four entreis are twos otherwise just add 1
    return (p1, p2)

def test():
    pass

if __name__ == '__main__':
    test()