# this script will house the evaluation function so that it can be cythonized
# the basic idea of the evaluation is to count the number of possible 4's for each side and subtract them.
# a positive score indicates that player one is winning while a negative indicates that player 2 is winning
# zero represents equality between the players while numbers whose absolute values are larger than 100 represents a win for the corresponding side
# Author: Caleb Bitting
# Date: 05/28/21

import numpy as np

def evaluate(array):
    p1_count = 0
    p2_count = 0
    # find the number of possible horizonal wins
    # find vertical
    # find left diagonal
    # find right diagonal
    for seg_list in seg_lists:
        p1, p2 = count_4s(seg_list)
        p1_count += p1
        p2_count += p2

def count_4s(segments):
    p1 = 0
    p2 = 0
    for seg in segments:
        if empty:
            p1 += 1
            p2 += 1
        elif 1 in seg:
            if 2 not in seg:
                p1 += 1
        else:                   # only happens when segment is not empty and doesn't have a one. i.e. the only number present is a 2
            p2 += 1
    return (p1, p2)

def test():
    pass

if __name__ == '__main__':
    test()