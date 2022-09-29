import heapq
from collections import defaultdict
import math


class SudokuState:

    def __init__(self, grid, n=9):
        """
        Initialize sudoku state
        Throws Value error if duplicate values are found in same rows, cols or sub grid
        """
        self.n = n
        self.n_sq_root = math.sqrt(self.n)
        self.board = grid

        self.grid_to_cells = defaultdict(set)
        self.row_to_seen_vals = defaultdict(set)
        self.col_to_seen_vals = defaultdict(set)
        self.col_to_missing_rows = defaultdict(set)
        self.empty_cells = []

        self._initialize_state()

    def _initialize_state(self):
        """
        Helper method to initialize state instance variables
        """
        for row in range(self.n):
            for col in range(self.n):

                val = self.board[row][col]
                if val == 0:
                    self.col_to_missing_rows[col].add(row)
                    heapq.heappush(self.empty_cells, (row, col))
                else:
                    if self.is_unsolvable(row, col, val):
                        raise ValueError(f'Duplicate value found')
                    self.col_to_seen_vals[col].add(val)
                    self.row_to_seen_vals[row].add(val)
                    self.grid_to_cells[self._grid_key(row, col)].add(val)

    def is_unsolvable(self, row, col, val):
        """
        Returns True if this sudoku state can have a valid solution or False otherwise
        """
        return val in self.col_to_seen_vals[col] or val in self.row_to_seen_vals[row] or val in self.grid_to_cells[
            self._grid_key(row, col)]

    def is_goal_state(self):
        """This state is a goal state if the length of the empty cells is zero"""
        return len(self.empty_cells) == 0

    def place_digit(self, row, col, val):
        """
        Place digit value in the specified the (row, col) coordinate of the state's board
        :param row: row where digit should be placed
        :param col: col where digit should be placed
        :param val: digit to be placed
        """
        self.board[row][col] = val
        self.empty_cells.remove((row, col))
        # add the digit to the seen rows and cols
        self.row_to_seen_vals[row].add(val)
        self.col_to_seen_vals[col].add(val)
        self.grid_to_cells[self._grid_key(row, col)].add(val)

        self.col_to_missing_rows[col].discard(row)

    def revert_state(self, row, col, val: int):
        self.board[row][col] = 0
        heapq.heappush(self.empty_cells, (row, col))

        # remove the digit from the seen rows and cols
        self.row_to_seen_vals[row].discard(val)
        self.col_to_seen_vals[col].discard(val)
        self.grid_to_cells[self._grid_key(row, col)].discard(val)

        self.col_to_missing_rows[col].add(row)

    def _grid_key(self, row, col):
        return row // self.n_sq_root, col // self.n_sq_root

    def choose_cell(self):
        """
        Return the minimum (row,col) element based on the column with the minimum amount of empty cells
        """
        return heapq.nsmallest(1, self.empty_cells, key=lambda tpl: len(self.col_to_missing_rows[tpl[1]]))[0]


def sudoku_solver(sudoku):

    def depth_first_search(sudoku_state):
        if sudoku_state.is_goal_state():
            return sudoku_state

        row, col = sudoku_state.choose_cell()

        for digit in range(1, 10):
            # check if a val can be put in the cell. If not valid, backtrack
            if not sudoku_state.is_unsolvable(row, col, digit):
                sudoku_state.place_digit(row, col, digit)
                deep_state = depth_first_search(sudoku_state)
                if not deep_state:
                    # backtrack and move forward to next digit
                    sudoku_state.revert_state(row, col, digit)
                else:
                    return deep_state
        return None

    n = 9
    invalid_sudoku = [[-1] * n] * n

    try:
        initial_state = SudokuState(sudoku)
        goal_state = depth_first_search(initial_state)
        if not goal_state:
            raise ValueError('Goal state solution was never reached')
        return goal_state.board
    except ValueError as e:
        print(e)
        return invalid_sudoku
