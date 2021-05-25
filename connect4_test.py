# This is the unittest script for the board and basic game functionality
# Author: Caleb Bitting
# Date: 05/25/2021

import unittest
from connect4 import *

class TestBoardStates(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_drop_success(self):
        # success
        self.assertEqual(self.board.drop(0, 1), 0)

    def test_drop_failure(self):
        # fill up row
        for _ in range(6):
            self.board.drop(0, 1)
        self.assertEqual(self.board.drop(0, 1), -1)

    def test_win_vertical(self):
        # for each valid starting point
        for row in range(3):
            for column in range(7):
                start = (row*7) + column
                zeros = [0 for _ in range(42)]
                # fill in the winning four
                for k in range(4):
                    zeros[start + 7*k] = 1
                board = Board.from_list(zeros)
                # make sure that algorithm marks a win
                expected = board.won(row, column, 1)        # all of these should be a win
                self.assertEqual(expected, 1, f'Board:\n{board}')

    def test_win_horizontal(self):
        # for each valid starting point
        for row in range(6):
            for column in range(4):
                start = (row*7) + column
                zeros = [0 for _ in range(42)]
                # fill in the winning four
                for k in range(start, start+4):
                    zeros[k] = 1
                board = Board.from_list(zeros)
                # make sure that algorithm marks a win
                expected = board.won(row, column, 1)        # all of these should be a win
                self.assertEqual(expected, 1, f'Board:\n{board}')

    def test_win_left_diagonal(self):
        # for each valid starting point
        for row in range(3, 6):
            for column in range(4):
                start = (row*7) + column
                zeros = [0 for _ in range(42)]
                # fill in the winning four
                for k in range(4):
                    zeros[start - 6*k] = 1
                board = Board.from_list(zeros)
                # make sure that algorithm marks a win
                expected = board.won(row, column, 1)        # all of these should be a win
                self.assertEqual(expected, 1, f'Board:\n{board}')

    def test_win_right_diagonal(self):
        # for each valid starting point
        for row in range(3, 6):
            for column in range(3, 7):
                start = (row*7) + column
                zeros = [0 for _ in range(42)]
                # fill in the winning four
                for k in range(4):
                    zeros[start - 8*k] = 1
                board = Board.from_list(zeros)
                # make sure that algorithm marks a win
                expected = board.won(row, column, 1)        # all of these should be a win
                self.assertEqual(expected, 1, f'Board:\n{board}')


if __name__ == '__main__':
    unittest.main()