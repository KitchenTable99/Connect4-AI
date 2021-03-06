# this is the python file for bitboards
import sys
from typing import List, Tuple, Optional, Dict
from collections import Counter
import pickle

dump_game_states = []


def dump_game_state(f):
    def wrapper(*args, **kwargs):
        # write args[-1]
        dump_game_states.append(args[-1])
        if len(dump_game_states) >= 500:
            with open('game_states.pickle', 'wb') as fp:
                pickle.dump(dump_game_states, fp)
            sys.exit()
        return f(*args, **kwargs)

    return wrapper


class BitBoard:
    internal: int

    def __init__(self):
        self.internal = 0

    @property
    def binary_array(self) -> List[int]:
        """This function returns an 49-bit representation of the number of the bitboard in binary as an array

        Returns:
            list: [0/1, 0/1, ... , 0/1]
        """
        binary_string = format(self.internal, '049b')
        return [int(num) for num in binary_string]

    @property
    def num_tokens_dropped(self) -> int:
        """This function uses Brian Kernighan's algorithm to return the number of set bits in the internal field.
        This represents the number of dropped tokens

        Returns:
            int: the number of dropped tokens
        """
        # set up variables for Brian Kernighan's algorithm
        internal_copy: int = self.internal
        set_bits: int = 0
        while internal_copy != 0:
            internal_copy = internal_copy & (internal_copy - 1)
            set_bits += 1

        return set_bits

    def drop(self, row: int, column: int) -> None:
        """This function increments the internal counter by lighting up the bit that needs to be high in order for
        the bitboard to hold the correct token. NOTE: this function does not check if the drop is possible by game
        rules. It just places the token.

        Args:
            row (int): the row into which to place the token
            column (int): the column into which to place the token
        """
        drop_idx = (7 * column) + row  # find the spot in grid
        drop_num = 2 ** drop_idx  # translate to number
        self.internal += drop_num

    def connected_check(self, shift_distance: int) -> bool:
        """This function will check to see if the bitboard contains a win given some directional shift.

        Args:
            shift_distance (int): the distance by which to shift
        """
        left_bboard: int = self.internal >> shift_distance  # shift left
        combined_left: int = self.internal & left_bboard  # combine shifted with original
        lefter_bboard: int = combined_left >> (2 * shift_distance)  # shift right

        return True if (lefter_bboard & combined_left) else False

    def check_win(self) -> bool:
        """This function checks for a win in all four directions

        Returns:
            bool: whether or not there is a win on this bitboard
        """
        for shift_distance in [1, 6, 7, 8]:
            win: bool = self.connected_check(shift_distance)
            if win:
                return True
        else:
            return False

    def win_this_move(self, rows: List[int]) -> Optional[int]:
        """This function will drop a token into each row and then check for a win.

        Args:
            rows (list): the row into which a token would be dropped by column

        Returns:
            bool: whether or not there is a win possible on this turn for the active player
        """
        # loop over each column dropping in the appropriate row
        for column, row in enumerate(rows):
            if row == -1:  # make sure a token can be dropped
                continue
            # drop the token
            drop_idx = (7 * column) + row
            drop_num = 2 ** drop_idx
            self.internal += drop_num

            # check for win and remove token
            win_present = self.check_win()
            self.internal -= drop_num
            if win_present:
                return column
        else:
            return None

    def clone(self) -> 'BitBoard':
        """This function clones the BitBoard

        Returns:
            to_return (BitBoard): the cloned object
        """
        to_return = BitBoard()
        to_return.internal = self.internal

        return to_return

    def __str__(self) -> str:
        # setup variables
        to_return: str = ''
        # reverse the order of the binary array
        normal_b_string = self.binary_array
        formatted_b_string = normal_b_string[::-1]

        # iterate across the rows in descending order
        for row in range(6, -1, -1):
            print_row = ''
            # iterate across the rows in ascending order
            for column in range(7):
                idx = row + (7 * column)
                print_row += str(formatted_b_string[idx])
                print_row += '  '
            to_return += print_row
            to_return += '\n'

        return to_return[:-1]  # don't return the last \n

    def __hash__(self) -> int:
        return hash(self.internal)

    def __eq__(self, other) -> bool:
        return self.internal == other.internal


class GameState:
    bboard_1: BitBoard
    bboard_2: BitBoard
    current_turn: int
    top_row_by_column: List[int]

    def __init__(self):
        # create the player boards
        self.bboard_1 = BitBoard()
        self.bboard_2 = BitBoard()
        # setup other constants
        self.current_turn = 1
        self.top_row_by_column = [5 for _ in range(7)]

    @property
    def bitboards(self) -> Tuple[BitBoard, BitBoard]:
        """This function is used to extract both bitboards from this object

        Returns:
            tuple: A tuple of bitboards (bboard_1, bboard_2)
        """
        return self.bboard_1, self.bboard_2

    @property
    def total_moves(self) -> int:
        return self.bboard_1.num_tokens_dropped + self.bboard_2.num_tokens_dropped

    @property
    def valid_columns(self) -> List[int]:
        return [idx for idx, value in enumerate(self.top_row_by_column) if value >= 0]

    @property
    def last_token(self) -> Optional[int]:
        c = Counter(self.top_row_by_column)
        if c[-1] != 6:
            raise Exception('last_column can only be called when there is one token left to place')
        else:
            keys_list: List[int] = list(c.keys())
            proper_row: int = keys_list[-1]
            return keys_list.index(proper_row)

    def valid_drop(self, column: int) -> bool:
        """Helper function so that this functionality is exposed for the minimax function

        Args:
            column (int): the column to check for validity

        Returns:
            bool: whether or not the column is a valid drop site
        """
        row = self.top_row_by_column[column]

        return False if row == -1 else True  # column full

    def drop(self, column: int) -> bool:
        """This function tries to update the game state with a dropped token

        Args:
            column (int): the column in which to try to drop the token

        Returns:
            bool: whether or not the drop was successful
        """
        # get proper row corresponding to column
        valid_column = self.valid_drop(column)
        if not valid_column:
            return False
        row = self.top_row_by_column[column]
        self.top_row_by_column[column] -= 1  # decrement row-column indices

        exec(f'self.bboard_{self.current_turn}.drop(row, column)')  # put correct token in correct place
        self.current_turn = 3 - self.current_turn  # switch the turns

        return True

    def end(self) -> int:
        """This function checks if it is the end of the game

        Returns:
            int: 1 -> player 1 victory
                 2 -> player 2 victory
                 0 -> draw
                -1 -> game continues
        """
        if self.bboard_1.check_win():
            return 1
        elif self.bboard_2.check_win():
            return 2
        elif self.total_moves == 42:
            return 0
        else:
            return -1

    def current_player_can_win(self) -> Optional[int]:
        """This function checks if the current player can win

        Returns:
            possible (bool): if the current player can win or not
        """
        if self.current_turn == 1:
            possible = self.bboard_1.win_this_move(self.top_row_by_column)
        else:
            possible = self.bboard_2.win_this_move(self.top_row_by_column)

        return possible

    def clone(self) -> 'GameState':
        """This function clones the GameState object

        Returns:
            to_return (GameState): the cloned object
        """
        to_return = GameState()
        to_return.bboard_1 = self.bboard_1.clone()
        to_return.bboard_2 = self.bboard_2.clone()
        to_return.current_turn = self.current_turn
        to_return.top_row_by_column = self.top_row_by_column[:]

        return to_return

    def __hash__(self) -> int:
        return hash((self.bboard_1, self.bboard_2, self.current_turn, tuple(self.top_row_by_column)))

    def __eq__(self, other: 'GameState') -> bool:
        if not isinstance(other, GameState):
            return False
        if self.bboard_1 != other.bboard_1:
            return False
        if self.bboard_2 != other.bboard_2:
            return False
        if self.current_turn != other.current_turn:
            return False
        if self.top_row_by_column != other.top_row_by_column:
            return False

        return True


class AlphaBetaAnalyzer:
    game_state: GameState
    alpha: int
    beta: int
    transposition_table: Dict[GameState, Tuple[int, int]]

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.alpha = -100
        self.beta = 100
        self.transposition_table = {}

    @dump_game_state
    def alpha_beta(self, game_state: GameState) -> Tuple[int, int]:
        """This function uses the mini-max algorithm to determine the best column

        Args:
            game_state (GameState): the current game state from which to begin the analysis

        Returns:
            value, column (Tuple[int, int]): the evaluation of the position and the column that results in the best column
        """
        # check for win next move
        p1_moves: int = game_state.bboard_1.num_tokens_dropped
        p2_moves: int = game_state.bboard_2.num_tokens_dropped
        nb_moves: int = p1_moves + p2_moves
        maximizing_player = True if game_state.current_turn == 1 else False
        if drop_col := game_state.current_player_can_win():
            if maximizing_player:
                evaluation: int = 21 - p1_moves
                self.transposition_table[game_state] = (evaluation, drop_col)
                return evaluation, drop_col
            else:
                evaluation: int = -1 * (21 - p1_moves)
                self.transposition_table[game_state] = (evaluation, drop_col)
                return evaluation, drop_col

        # check for draw next move
        if nb_moves == 41:
            evaluation: Tuple[int, int] = (0, game_state.last_token)
            self.transposition_table[game_state] = evaluation
            return evaluation

        # run for maximizing player
        if maximizing_player:
            value: int = -999999
            column: int = -1
            for drop_col in game_state.valid_columns:
                # clone game_state and test column
                child: GameState = game_state.clone()
                child.drop(drop_col)

                # check to see if node already evaluated
                if lookup := self.transposition_table.get(child):
                    ab_value, ab_column = lookup
                else:
                    ab_value, ab_column = self.alpha_beta(child)

                # deal with evaluation
                if ab_value > value:
                    value = ab_value
                    column = ab_column
                if value >= self.beta:
                    break  # beta cutoff
                self.alpha = max(self.alpha, value)

                # store in transposition table
                if not lookup:
                    self.transposition_table[game_state] = (value, column)
            return value, column
        else:
            value: int = 999999
            column: int = -1
            for drop_col in game_state.valid_columns:
                # duplicate game_state and check for valid drop
                child: GameState = game_state.clone()
                child.drop(drop_col)

                # get evaluation of node
                if lookup := self.transposition_table.get(child):
                    ab_value, ab_column = lookup
                else:
                    ab_value, ab_column = self.alpha_beta(child)

                # deal with evaluation
                if ab_value < value:
                    value = ab_value
                    column = ab_column
                if value <= self.alpha:
                    break  # alpha cutoff
                self.beta = min(self.beta, value)

                # store
                if not lookup:
                    self.transposition_table[game_state] = (value, column)
            return value, column

    def best_column(self) -> int:
        """This function uses the mini-max algorithm to determine the best column

        Returns:
            column (int): the evaluation of the position and the column that results in the best column
        """
        # check for win on current move
        if column := self.game_state.current_player_can_win():
            return column

        # check for opponent win on next move
        throwaway: GameState = self.game_state.clone()
        throwaway.current_turn = 3 - throwaway.current_turn
        if column := throwaway.current_player_can_win():
            return column

        # then run alpha_beta
        _, column = self.alpha_beta(self.game_state)
        return column


def test():
    bboard = BitBoard()
    bboard.drop(0, 0)
    bboard.drop(1, 0)
    bboard.drop(2, 0)
    game_state = GameState()
    # print(f'{bboard.win_this_move([3,5,5,5,5,5,5]) = }')


if __name__ == '__main__':
    test()
