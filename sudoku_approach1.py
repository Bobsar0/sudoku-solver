from collections import defaultdict
from typing import List
import math


class SudokuState:

    def __init__(self, board: List[List[int]], n=9):

        """
        Initialize sudoku state
        Throws Value error if duplicate values are found in same rows, cols or sub grid.

        Parameters
        ----------
        board : List[List[int]]
            The sudoku board.
        n : int, optional
            The size of the sudoku board (default is None). This is used so the sudoku can be extended for other suitable board sizes.
        """
        self.n = n
        self.n_sq_root = math.sqrt(self.n)
        self.board = board

        self.row_to_seen_vals, self.col_to_seen_vals, self.sub_grid = defaultdict(set), defaultdict(set), defaultdict(
            set)
        self.empty_cells = []

        self._initialize_state()

    def _initialize_state(self):
        """
        Helper method to initialize state instance variables.

        Raises
        ------
        ValueError
            If duplicate value is found either in row, column or sub grid.
        """
        for row in range(self.n):
            for col in range(self.n):
                val = self.board[row][col]
                if val == 0:
                    self.empty_cells.append((row, col))
                else:
                    if self.is_unsolvable(row, col, val):
                        raise ValueError(f'Duplicate value found')
                    self.col_to_seen_vals[col].add(val)
                    self.row_to_seen_vals[row].add(val)
                    self.sub_grid[self._grid_key(row, col)].add(val)

    def is_unsolvable(self, row, col, val):
        """
        Returns True if this sudoku state can have a valid solution or False otherwise
        :param row: row to check for
        :param col: column to check for
        :param val: value which we want to determine if it can be placed in the (row, col) cell
        :return: True if the value is seen in column, row or sub grid. False otherwise
        """
        return val in self.col_to_seen_vals[col] or val in self.row_to_seen_vals[row] or val in self.sub_grid[
            self._grid_key(row, col)]

    def is_goal_state(self):
        """This state is a goal state if the length of the empty cells is zero
        :return: True if there are no more cells that are empty or False otherwise
        """
        return len(self.empty_cells) == 0

    def place_digit(self, row, col, val):
        """
        Place digit value in the specified the (row, col) coordinate of the state's board
        :param row: row where digit should be placed
        :param col: col where digit should be placed
        :param val: digit to be placed
        """
        self.board[row][col] = val
        # remove the last cell
        self.empty_cells.pop()

        # update the seen values in the rows and cols
        self.row_to_seen_vals[row].add(val)
        self.col_to_seen_vals[col].add(val)
        self.sub_grid[self._grid_key(row, col)].add(val)

    def revert_state(self, row, col, val: int):
        """
        Revert the state of the sudoku during backtracking
        :param row: row to be reverted
        :param col: column to be reverted
        :param val: digit in the (row, col) cell to be reverted
        """
        self.empty_cells.append((row, col))

        # remove the values previously added to the data structures when the digit was placed
        self.row_to_seen_vals[row].discard(val)
        self.col_to_seen_vals[col].discard(val)
        self.sub_grid[self._grid_key(row, col)].discard(val)

    def _grid_key(self, row, col):
        """
        Get key for the subgrid that contains the (row, col) cell
        :param row: The row contained in the grid
        :param col: The column contained in the grid
        :return: The key of the grid that contains the (row, col) cell
        """
        return row // self.n_sq_root, col // self.n_sq_root

    def choose_cell(self):
        """
        Choose the next (row, col) cell to place digit in.
        The last empty cell is chosen so that digit can be placed and discarded as necessary with O(1) time complexity
        :return: (row, col) tuple
        """
        return self.empty_cells[-1]


def sudoku_solver(sudoku):
    def depth_first_search(sudoku_state):
        if sudoku_state.is_goal_state():
            return sudoku_state

        row, col = sudoku_state.choose_cell()

        for digit in range(1, 10):
            # check if a digit can be put in the cell. If not valid, backtrack
            if not sudoku_state.is_unsolvable(row, col, digit):
                sudoku_state.place_digit(row, col, digit)
                deep_state = depth_first_search(sudoku_state)
                if not deep_state:
                    # backtrack and move forward to next val
                    sudoku_state.revert_state(row, col, digit)
                else:
                    return deep_state
        return None

    invalid_sudoku = [[-1] * 9] * 9

    try:
        initial_state = SudokuState(sudoku)
        goal_state = depth_first_search(initial_state)
        if not goal_state:
            raise ValueError('Goal state solution was never reached')
        return goal_state.board
    except ValueError as e:
        print(e)
        return invalid_sudoku
